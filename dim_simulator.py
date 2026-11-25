"""Drag-and-drop dimming simulator for the projector.

On a pop-out window, drag shapes around a canvas that represents the projected image.
Wherever a shape sits, the projector's (EBF) gain is dimmed so that region of the real projection goes dark.

Run:
    python dim_simulator.py                 # connect to the projector
    python dim_simulator.py --no-projector  # preview only
    python dim_simulator.py --fast-usb      # experimental: skip USB write acknowledgements (faster)

Controls:
    Toolbar buttons    add a shape
    Left-drag          move a shape
    Mouse wheel / + -  resize the shape under the mouse (or the selected one)
    R                  rotate the selected shape 15 degrees
    Right-click / Del  delete a shape
    Edge fade slider   how far (% of image height) the dimming fades out around each shape; 0 = hard edge
    G                  toggle the control-point grid
    O                  toggle shape outlines
    F                  toggle full screen (for mirroring the window onto a projector)
    Esc                leave full screen
"""

import math
import sys
import threading
import time
import tkinter as tk
from pathlib import Path

import cv2 as cv
import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

# Blend map hardware constants (from blending_utils/libs/blend_map_gen.py)
A_H = 63  # control points across
L_V = 32  # control points down
L_H = 32  # control points per half (DLPC754x splits the image into two halves)
DEFAULT_RESOLUTION = (3840, 2160)
GAIN_MAX = 1 + 4095 / 4096  # largest gain the hardware accepts

CANVAS_SIZE = (
    3840,
    2160,
)  # starting window size of the drawing area (16:9 like the projector)
BASE_BRIGHTNESS = 245  # how bright the projected image looks in the preview

"""
Control Points: The projector's blend map has a fixed number of control points, but the projector's
resolution can vary. This function returns the pixel coordinates of the control points, which are evenly 
spaced across the image, with the halfway column pinned to the center of the image. 
The first and last control points are pinned to the edges of the image.
"""


def control_points(pixels, lines):
    """Same layout BlendMap_c.Initialize() uses. Evenly spaced, with the halfway column pinned."""
    hstep = (pixels - 1.0) / (A_H - 1)
    horz = np.floor(np.arange(A_H) * hstep + 0.5).astype(int)
    horz[0], horz[L_H - 1], horz[A_H - 1] = 0, pixels // 2 - 1, pixels - 1
    vstep = (lines - 1.0) / (L_V - 1)
    vert = np.floor(np.arange(L_V) * vstep + 0.5).astype(int)
    vert[0], vert[L_V - 1] = 0, lines - 1
    return horz, vert


"""
Shapes: each shape is a list of polygons in unit coordinates (about -1..1), y pointing down
"""


def _circle(n=48, r=1.0):
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    return np.c_[r * np.cos(t), r * np.sin(t)]


def _apple():
    t = np.linspace(-np.pi, np.pi, 90, endpoint=False)
    top = np.angle(
        np.exp(1j * (t + np.pi / 2))
    )  # angle away from the top (screen y points down)
    bottom = np.angle(np.exp(1j * (t - np.pi / 2)))
    r = 1 - 0.22 * np.exp(-((top / 0.38) ** 2)) - 0.07 * np.exp(-((bottom / 0.3) ** 2))
    body = np.c_[1.08 * r * np.cos(t), 0.1 + 0.95 * r * np.sin(t)]
    stem = np.array([[-0.05, -0.68], [0.05, -0.68], [0.12, -1.05], [0.03, -1.07]])
    a = np.radians(-30)
    leaf = _circle(24) * [0.28, 0.11]
    leaf = leaf @ np.array([[np.cos(a), np.sin(a)], [-np.sin(a), np.cos(a)]]) + [
        0.36,
        -0.95,
    ]
    return [body, stem, leaf]


def _star():
    t = np.linspace(-np.pi / 2, 3 * np.pi / 2, 10, endpoint=False)
    r = np.where(np.arange(10) % 2 == 0, 1.0, 0.45)
    return np.c_[r * np.cos(t), r * np.sin(t)]


SHAPES = {  # each shape is a list of polygons in unit coordinates (about -1..1), y pointing down
    "Triangle": [np.array([[0, -1], [0.866, 0.5], [-0.866, 0.5]])],
    "Square": [np.array([[-0.8, -0.8], [0.8, -0.8], [0.8, 0.8], [-0.8, 0.8]])],
    "Rectangle": [np.array([[-1.3, -0.6], [1.3, -0.6], [1.3, 0.6], [-1.3, 0.6]])],
    "Circle": [_circle()],
    "Star": [_star()],
    "Apple": _apple(),
}
COLORS = ["#e63946", "#2a9d8f", "#e9c46a", "#457b9d", "#f4a261", "#8338ec"]


class Shape:
    def __init__(self, kind, color):
        self.kind = kind
        self.color = color
        self.cx, self.cy = 0.5, 0.5  # center, as a fraction of the canvas width/height
        self.size = 0.12  # radius, as a fraction of the canvas height
        self.angle = 0.0  # degrees

    def polygons(self, w, h):
        """Polygons in canvas pixel coordinates."""
        a = math.radians(self.angle)
        rot = np.array([[math.cos(a), math.sin(a)], [-math.sin(a), math.cos(a)]])
        return [
            (p @ rot) * (self.size * h) + [self.cx * w, self.cy * h]
            for p in SHAPES[self.kind]
        ]

    def contains(self, x, y, w, h):
        return any(
            cv.pointPolygonTest(p.astype(np.float32), (float(x), float(y)), False) >= 0
            for p in self.polygons(w, h)
        )


"""
Mask: a 2D array of values 0 or 1, where 1 indicates where any shape is present.
The projector's gain is dimmed wherever the mask is 1.
"""


def shapes_mask(shapes, w, h):
    mask = np.zeros((h, w), np.uint8)
    for s in shapes:
        for p in s.polygons(w, h):
            cv.fillPoly(mask, [np.round(p).astype(np.int32)], 1)
    return mask


"""
Gain for every control point.

Core: The projector blends gain linearly between control points, so a grid cell is only fully dark if
all four of its corner points are dimmed. Any point touching a cell that contains part of a shape is
therefore set to dim_gain, which guarantees the whole shape is dark.

Fade: points outside the core ramp back up to full brightness over fade_px (canvas pixels), following
a smoothstep curve of their distance to the nearest core point. fade_px = 0 gives the hard edge.
hx, vy: control point positions in canvas pixels.
"""


def gain_grid(mask, hx, vy, dim_gain, fade_px=0.0):

    h, w = mask.shape
    xe = np.clip(np.round(hx).astype(int), 0, w - 1)
    ye = np.clip(np.round(vy).astype(int), 0, h - 1)
    S = cv.integral(mask)  # S[y, x] = sum of mask[:y, :x]
    x0, x1 = xe[:-1], xe[1:] + 1
    y0, y1 = ye[:-1], ye[1:] + 1
    cell_sum = (
        S[np.ix_(y1, x1)] - S[np.ix_(y0, x1)] - S[np.ix_(y1, x0)] + S[np.ix_(y0, x0)]
    )
    hit = np.pad(cell_sum > 0, 1)  # (L_V+1, A_H+1) after padding
    dark = hit[:-1, :-1] | hit[:-1, 1:] | hit[1:, :-1] | hit[1:, 1:]
    if fade_px <= 0 or not dark.any():
        return np.where(dark, dim_gain, 1.0)

    # distance from every control point to the nearest dark (core) point, in canvas pixels
    seeds = np.ones((h, w), np.uint8)
    rows, cols = np.nonzero(dark)
    seeds[ye[rows], xe[cols]] = 0
    dist = cv.distanceTransform(seeds, cv.DIST_L2, cv.DIST_MASK_PRECISE)[np.ix_(ye, xe)]
    t = np.clip(dist / fade_px, 0, 1)
    ramp = (
        t * t * (3 - 2 * t)
    )  # smoothstep: gentle start and end, no visible "corner" at either edge
    return dim_gain + (1 - dim_gain) * ramp


def _interp_weights(points, n):
    i = np.clip(
        np.searchsorted(points, np.arange(n), side="right") - 1, 0, len(points) - 2
    )
    f = np.clip((np.arange(n) - points[i]) / (points[i + 1] - points[i]), 0, 1)
    return i, f


def preview_image(gain, hx, vy, w, h):
    """What the projector would show. Bright image multiplied by the interpolated gain."""
    ix, fx = _interp_weights(hx, w)
    iy, fy = _interp_weights(vy, h)
    gx = gain[:, ix] * (1 - fx) + gain[:, ix + 1] * fx
    g = gx[iy, :] * (1 - fy)[:, None] + gx[iy + 1, :] * fy[:, None]
    gray = np.clip(BASE_BRIGHTNESS * g, 0, 255).astype(np.uint8)
    rgb = np.repeat(gray[:, :, None], 3, axis=2)
    return f"P6 {w} {h} 255 ".encode() + rgb.tobytes()


"""
Projector: talks to the DLPC754x through TI's blending_utils. Writes happen on a background thread so the
window never freezes; if updates come faster than USB can keep up, only the newest one is sent
"""


class Projector:
    def __init__(self, enabled=True, fast_usb=False):
        self.connected = False
        self.message = "preview only"
        self.resolution = DEFAULT_RESOLUTION
        self.last_write_ms = None
        self.error = None
        if not enabled:
            self.message = "preview only (--no-projector)"
            return
        try:
            # commands must be imported first: it adds the DLL folder to the path
            from blending_utils.libs.dlpc754x import commands as cmds
            from blending_utils.libs import usb_comms
            from blending_utils.libs import blend_map_gen as map_gen
            from blending_utils.libs import blend_map_luts as luts
        except Exception as e:  # macOS/Linux, or pythonnet / .NET missing
            self.message = (
                f"preview only (projector library unavailable: {type(e).__name__}: {e})"
            )
            return
        self.cmds, self.luts = cmds, luts

        if not usb_comms.Connect_USB():
            self.message = "preview only (no projector found on USB)"
            return
        self._usb = usb_comms

        summary, size = cmds.ReadDisplayImageSize()
        if summary.Successful:
            self.resolution = (
                int(size.DisplayAreaPixelsPerLine),
                int(size.DisplayAreaLinesPerFrame),
            )

        self.blend = map_gen.BlendMap_c("dim_simulator")
        self.blend.Initialize(*self.resolution)
        print(
            f"Projector {self.resolution[0]}x{self.resolution[1]}: writing a neutral blend map..."
        )
        t = time.perf_counter()
        if not luts.WriteBlendMapLUTs(self.blend):
            self.message = "preview only (could not write the blend map)"
            usb_comms.Disconnect_USB()
            return
        print(f"  done in {(time.perf_counter() - t) * 1000:.0f} ms")

        # Speed-ups (see _write): one "Broadcast" command per row instead of separate red/green/blue writes
        ch = cmds.DispfmtColorChannelSelectT
        self._rgb = [ch.Red, ch.Green, ch.Blue]
        self.channels = [ch.Broadcast] if self._broadcast_works() else self._rgb
        print(
            "  colour channels per write:",
            "1 (broadcast)" if len(self.channels) == 1 else "3 (R, G, B)",
        )
        if (
            fast_usb
        ):  # experimental: don't wait for an acknowledgement after every write command
            cmds.Command.CommInterface.CommandHeader.RequestACK = False
            print("  --fast-usb: write acknowledgements turned off")

        self.connected = True
        self.message = (
            f"projector connected ({self.resolution[0]}x{self.resolution[1]})"
        )
        self.last_commands = None
        self._current = np.ones((L_V, A_H))
        self._pending = self._current.copy()
        self._lock = threading.Lock()
        self._wake = threading.Event()
        self._stop = False
        self._thread = threading.Thread(target=self._worker, daemon=True)
        self._thread.start()

    @staticmethod
    def _to_fixed(gains):
        """Gain (0.0 to ~2.0) -> the projector's u1.12 fixed-point format, same rounding as TI's code."""
        return [int(v) for v in np.trunc(np.clip(gains, 0, GAIN_MAX) * 4096)]

    def _broadcast_works(self):
        """Write one test value with Broadcast and read it back on all three colors."""
        cmds = self.cmds
        ch = cmds.DispfmtColorChannelSelectT
        if not hasattr(ch, "Broadcast"):
            return False
        try:
            test = 4095
            ok = cmds.WriteBlendMapGainValues(
                False, ch.Broadcast, 0, 0, [test]
            ).Successful
            for c in self._rgb:
                summary, compressed, vals = cmds.ReadBlendMapGainValues(c, 0, 1)
                ok = (
                    ok
                    and summary.Successful
                    and len(vals) == 1
                    and int(vals[0]) == test
                )
        except Exception:
            ok = False
        for c in self._rgb:  # put the test point back to 1.0 either way
            cmds.WriteBlendMapGainValues(False, c, 0, 0, [4096])
        return ok

    def request(self, gain):
        if not self.connected:
            return
        with self._lock:
            self._pending = gain.copy()
        self._wake.set()

    def _write(self, target):
        """Send only what changed: for each changed row, one command covering just its changed columns,
        then a single 'apply'. (TI's WriteBlendMapLUTs_Gain rewrites a whole rectangle on 3 channels and
        re-reads the blending state every time, which is several times more USB traffic.)
        """
        changed = target != self._current
        ok, n = True, 0
        for r in np.nonzero(changed.any(axis=1))[0]:
            cols = np.nonzero(changed[r])[0]
            c0, c1 = int(cols[0]), int(cols[-1])
            vals = self._to_fixed(target[r, c0 : c1 + 1])
            for ch in self.channels:
                ok &= self.cmds.WriteBlendMapGainValues(
                    False, ch, 0, A_H * int(r) + c0, vals
                ).Successful
                n += 1
            if ok:
                self._current[r, c0 : c1 + 1] = target[r, c0 : c1 + 1]
        ok &= self.cmds.WriteApplyBlendMap(True).Successful
        return ok, n + 1

    def _worker(self):
        while True:
            self._wake.wait()
            self._wake.clear()
            with self._lock:
                target = self._pending.copy()
            if (target != self._current).any():
                t = time.perf_counter()
                try:
                    ok, n = self._write(target)
                except Exception as e:
                    ok, n = False, 0
                    print("Projector write error:", e)
                self.last_write_ms = (time.perf_counter() - t) * 1000
                self.last_commands = n
                self.error = None if ok else "last write failed"
            if (
                self._stop and not self._wake.is_set()
            ):  # finish the final (restore) write before exiting
                return

    def close(self):
        """Put the gains back to 1.0 so the projector isn't left with dark patches."""
        if not self.connected:
            return
        self.request(np.ones((L_V, A_H)))
        self._stop = True
        self._wake.set()
        self._thread.join(timeout=10)
        self._usb.Disconnect_USB()


# ============================== the window ==============================
class App:
    def __init__(self, root, projector):
        self.root, self.proj = root, projector
        self.shapes, self.selected, self.drag = [], None, None
        self.show_grid, self.show_outlines, self.fullscreen = True, True, False
        self.hctrl, self.vctrl = control_points(*projector.resolution)
        self.gain = np.ones((L_V, A_H))
        self._photo = None
        self._last_preview_key = None

        root.title("Projector dimming simulator")
        self.bar = tk.Frame(root, padx=6, pady=4)
        self.bar.pack(side=tk.TOP, fill=tk.X)
        for kind in SHAPES:
            tk.Button(
                self.bar, text=kind, command=lambda k=kind: self.add_shape(k)
            ).pack(side=tk.LEFT, padx=2)
        tk.Button(self.bar, text="Clear", command=self.clear).pack(
            side=tk.LEFT, padx=(12, 2)
        )
        tk.Label(self.bar, text="  Brightness in shape %").pack(side=tk.LEFT)
        self.level = tk.Scale(
            self.bar,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            length=120,
            command=lambda _: self.update(),
        )
        self.level.pack(side=tk.LEFT)
        tk.Label(self.bar, text="  Edge fade %").pack(side=tk.LEFT)
        self.fade = tk.Scale(
            self.bar,
            from_=0,
            to=25,
            orient=tk.HORIZONTAL,
            length=100,
            command=lambda _: self.update(),
        )
        self.fade.set(10)
        self.fade.pack(side=tk.LEFT)
        self.live = tk.BooleanVar(value=True)
        tk.Checkbutton(self.bar, text="Update while dragging", variable=self.live).pack(
            side=tk.LEFT, padx=6
        )

        self.canvas = tk.Canvas(
            root,
            width=CANVAS_SIZE[0],
            height=CANVAS_SIZE[1],
            bg="black",
            highlightthickness=0,
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.status = tk.Label(root, anchor="w", padx=6)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

        c = self.canvas
        c.bind("<ButtonPress-1>", self.on_press)
        c.bind("<B1-Motion>", self.on_drag)
        c.bind("<ButtonRelease-1>", self.on_release)
        for b in (
            "<Button-2>",
            "<Button-3>",
        ):  # right-click is Button-2 on macOS, Button-3 elsewhere
            c.bind(b, self.on_delete_click)
        c.bind("<MouseWheel>", self.on_wheel)  # Windows / macOS
        c.bind("<Button-4>", lambda e: self.resize_at(e, 1.1))  # Linux
        c.bind("<Button-5>", lambda e: self.resize_at(e, 1 / 1.1))
        c.bind("<Configure>", lambda e: self.update(force_preview=True))
        root.bind("<Key>", self.on_key)
        root.protocol("WM_DELETE_WINDOW", self.quit)
        self.poll_status()

    """
    Geometry: canvas area, mouse position, control point positions
    """

    def area(self):
        """The projector-shaped (16:9) rectangle inside the canvas: x offset, y offset, width, height."""
        cw, ch = max(self.canvas.winfo_width(), 2), max(self.canvas.winfo_height(), 2)
        px, ln = self.proj.resolution
        aw = min(cw, ch * px / ln)
        ah = aw * ln / px
        return int((cw - aw) / 2), int((ch - ah) / 2), max(int(aw), 2), max(int(ah), 2)

    def size(self):
        return self.area()[2:]

    def local(self, e):
        """Mouse position relative to the projector area."""
        ox, oy, _, _ = self.area()
        return e.x - ox, e.y - oy

    def ctrl_canvas(self):
        w, h = self.size()
        px, ln = self.proj.resolution
        return self.hctrl * (w - 1) / (px - 1), self.vctrl * (h - 1) / (ln - 1)

    def shape_at(self, x, y):
        w, h = self.size()
        for s in reversed(self.shapes):  # topmost first
            if s.contains(x, y, w, h):
                return s
        return None

    """
    Add / remove shapes, resize shapes
    """

    def add_shape(self, kind):
        s = Shape(kind, COLORS[len(self.shapes) % len(COLORS)])
        s.cx += 0.03 * (
            len(self.shapes) % 5
        )  # offset so new shapes don't stack exactly
        self.shapes.append(s)
        self.selected = s
        self.update()

    def clear(self):
        self.shapes, self.selected = [], None
        self.update()

    def delete(self, s):
        if s in self.shapes:
            self.shapes.remove(s)
        if self.selected is s:
            self.selected = None
        self.update()

    def resize_at(self, event, factor):
        s = self.shape_at(*self.local(event)) or self.selected
        if s:
            s.size = float(np.clip(s.size * factor, 0.02, 0.6))
            self.selected = s
            self.update()

    """
    Mouse/keyboard events: select, drag, resize, rotate, delete, toggle grid/outlines/fullscreen
    """

    def on_press(self, e):
        x, y = self.local(e)
        s = self.shape_at(x, y)
        self.selected = s
        if s:
            self.shapes.remove(s)
            self.shapes.append(s)  # bring to front
            w, h = self.size()
            self.drag = (s, x - s.cx * w, y - s.cy * h)
        self.update()

    def on_drag(self, e):
        if not self.drag:
            return
        s, dx, dy = self.drag
        x, y = self.local(e)
        w, h = self.size()
        s.cx = float(np.clip((x - dx) / w, 0, 1))
        s.cy = float(np.clip((y - dy) / h, 0, 1))
        self.update(send=self.live.get())

    def on_release(self, e):
        if self.drag:
            self.drag = None
            self.update()

    def on_delete_click(self, e):
        s = self.shape_at(*self.local(e))
        if s:
            self.delete(s)

    def on_wheel(self, e):
        self.resize_at(e, 1.1 if e.delta > 0 else 1 / 1.1)

    def on_key(self, e):
        k = e.keysym.lower()
        if k in ("delete", "backspace") and self.selected:
            self.delete(self.selected)
        elif k == "r" and self.selected:
            self.selected.angle = (self.selected.angle + 15) % 360
            self.update()
        elif k in ("plus", "equal", "minus", "underscore") and self.selected:
            self.selected.size = float(
                np.clip(
                    self.selected.size * (1.1 if k in ("plus", "equal") else 1 / 1.1),
                    0.02,
                    0.6,
                )
            )
            self.update()
        elif k == "g":
            self.show_grid = not self.show_grid
            self.update(force_preview=True)
        elif k == "o":
            self.show_outlines = not self.show_outlines
            self.update(force_preview=True)
        elif k == "f" or (k == "escape" and self.fullscreen):
            self.fullscreen = not self.fullscreen if k == "f" else False
            self.root.attributes("-fullscreen", self.fullscreen)
            if self.fullscreen:
                self.bar.pack_forget()
                self.status.pack_forget()
            else:
                self.status.pack(side=tk.BOTTOM, fill=tk.X)
                self.bar.pack(side=tk.TOP, fill=tk.X, before=self.canvas)

    """
    Update projector and redraw the canvas. The projector's gain is dimmed wherever a shape is present, 
    and fades back to full brightness over fade_px pixels.
    """

    def update(self, send=True, force_preview=False):
        w, h = self.size()
        hx, vy = self.ctrl_canvas()
        fade_px = self.fade.get() / 100.0 * h  # fade width as a % of the image height
        self.gain = gain_grid(
            shapes_mask(self.shapes, w, h), hx, vy, self.level.get() / 100.0, fade_px
        )
        if send:
            self.proj.request(self.gain)
        self.redraw(hx, vy, force_preview)

    def redraw(self, hx, vy, force_preview):
        c = self.canvas
        ox, oy, w, h = self.area()
        key = (w, h, self.gain.tobytes())
        if (
            force_preview or key != self._last_preview_key
        ):  # rebuilding the image is the slow part
            self._photo = tk.PhotoImage(
                data=preview_image(self.gain, hx, vy, w, h), format="PPM"
            )
            self._last_preview_key = key
        c.delete("all")
        c.create_image(ox, oy, image=self._photo, anchor="nw")
        if self.show_grid:
            for x in hx:
                c.create_line(ox + x, oy, ox + x, oy + h, fill="#c8c8c8")
            for y in vy:
                c.create_line(ox, oy + y, ox + w, oy + y, fill="#c8c8c8")
        if self.show_outlines:
            for s in self.shapes:
                width = 3 if s is self.selected else 2
                for p in s.polygons(w, h):
                    c.create_polygon(
                        *(p + [ox, oy]).ravel().tolist(),
                        outline=s.color,
                        fill="",
                        width=width,
                    )

    def poll_status(self):
        n = int((self.gain < 1).sum())
        parts = [
            self.proj.message,
            f"{len(self.shapes)} shape(s)",
            f"{n} of {A_H * L_V} control points dimmed",
        ]
        if self.proj.last_write_ms is not None:
            parts.append(
                f"last projector write {self.proj.last_commands} commands, {self.proj.last_write_ms:.0f} ms"
            )
        if self.proj.error:
            parts.append(self.proj.error)
        self.status.config(text="   |   ".join(parts))
        self.root.after(200, self.poll_status)

    def quit(self):
        self.status.config(text="Restoring projector brightness...")
        self.root.update_idletasks()
        self.proj.close()
        self.root.destroy()


def main():
    projector = Projector(
        enabled="--no-projector" not in sys.argv, fast_usb="--fast-usb" in sys.argv
    )
    print(projector.message)
    root = tk.Tk()
    App(root, projector)
    root.mainloop()


if __name__ == "__main__":
    main()
