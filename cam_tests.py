import camfunctions
import cv2 as cv

try:
    cam = cv.VideoCapture(0)
except:
    print("camera's not connected")
    cam = cv.VideoCapture(1)


def cameraCheck(cam):
    print("Press q to exit")
    while True:
        ret, frame = cam.read()

        cv.imshow('Camera',frame)

        if cv.waitKey(1) == ord('q'):
            break

