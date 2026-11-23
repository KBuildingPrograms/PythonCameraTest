# Imports
if __name__ == '__main__' or __name__ == 'blend_map_edit':
    import blend_map_gen as map_gen
    import math_functions_lib as math_funcs
    import license_strings as lic
else:
    from . import blend_map_gen as map_gen
    from . import math_functions_lib as math_funcs
    from . import license_strings as lic
import numpy as np

# Module metadata
__copyright__ = lic.copyright_str
__author__ = lic.author
__status__ = lic.status
__doc__ = "DESCRIPTION: Blending Map editing library (API)"

# -------------------------------- Control Point Editing -------------------------------------- #
def SetHorzControlPointsArray(BlendMap: map_gen.BlendMap_c, Points, verbose=False):
    """
    Description: populates a BlendMap's horizontal control points array with a user-defined array

    Input arguments:
    BlendMap : a BlendMap structure
    Points   : a user-defined array with horizontal control points (must be 63 entries deep)
    verbose  : True = print msgs to console, (default = False)

    Output arguments:
    BlendMap : a modified BlendMap structure
    Status   : status flag (boolean)
    """
    # Constants
    A_H, L_V, L_H, NormOffset = map_gen.GetBlendMapConstants()

    # Validate the length of the input array
    if (len(Points) != A_H):
        if (True == verbose):
            print("ERROR: invalid control points array length!")
        return BlendMap, False

    # Assert the points
    if ((Points[0] != 0) or (Points[L_H - 1] != BlendMap.HalfPixels - 1) or (Points[A_H - 1] != BlendMap.Pixels - 1)):
        if (True == verbose):
            print("ERROR: invalid control points array!")
        return BlendMap, False

    for col in range(1, A_H, 1):
       if ((Points[col] - Points[col - 1]) < 1):
           if (True == verbose):
               print("ERROR: invalid control points array!")
           return BlendMap, False

    # Copy the points
    for col in range(0, A_H, 1):
        BlendMap.HorzCtrPoints[col] = int(Points[col])

    # Done
    return BlendMap, True


def SetVertControlPointsArray(BlendMap: map_gen.BlendMap_c, Points, verbose=False):
    """
    Description: populates a BlendMap's vertical control points array with a user-defined array

    Input arguments:
    BlendMap : a BlendMap structure
    Points   : a user-defined array with vertical control points (must be 32 entries deep)
    verbose  : True = print msgs to console, (default = False)

    Output arguments:
    BlendMap : a modified BlendMap structure
    Status   : status flag (boolean)
    """

    # Constants
    A_H, L_V, L_H, NormOffset = map_gen.GetBlendMapConstants()

    # Validate the length of the input array
    if (len(Points) != L_V):
        if (True == verbose):
            print("ERROR: invalid control points array length!")
        return BlendMap, False

    # Assert the points
    if ((Points[0] != 0) or (Points[L_V - 1] != BlendMap.Lines - 1)):
        if (True == verbose):
            print("ERROR: invalid control points array!")
        return BlendMap, False

    for row in range(1, L_V, 1):
        if ((Points[row] - Points[row - 1]) < 1):
            if (True == verbose):
                print("ERROR: invalid control points array!")
            return BlendMap, False

    # Copy the points
    for row in range(0, L_V, 1):
        BlendMap.VertCtrPoints[row] = int(Points[row])

    # Done
    return BlendMap, True

def EditHorzControlPoint(BlendMap: map_gen.BlendMap_c, col: int, ReqPos: int, compress: bool, verbose=False):
    """
    Description: edit a BlendMap's horizontal control point position

    Input arguments:
    BlendMap : a BlendMap structure
    col      : column index of the point to be edited
    ReqPos   : requested pixel position of the point to be edited
    compress : Enable or disable control point compression
    verbose  : True = print msgs to console, (default = False)

    Output arguments:
    BlendMap : a modified BlendMap structure
    Status   : status flag (boolean)
    NewCol   : column index of the current selected point (changes if a jump-over occurred)
    """

    # Constants
    A_H, L_V, L_H, NormOffset = map_gen.GetBlendMapConstants()
    NewCol = col

    # If the point is not editable, do nothing
    if ((col <= 0) or (col == L_H - 1) or (col >= A_H - 1)):
        if (True == verbose):
            print('ERROR: requested column index is static (position cannot be edited)!')
        return BlendMap, False, NewCol

    # Get current and neighbor positions
    PrvInd = col - 1
    CurInd = col
    NxtInd = col + 1
    PrvPos = BlendMap.HorzCtrPoints[PrvInd]
    CurPos = BlendMap.HorzCtrPoints[CurInd]
    NxtPos = BlendMap.HorzCtrPoints[NxtInd]

    # Update position
    if (True == verbose):
        print('Current x position = ' + str(CurPos), ' requested new x position = ' + str(ReqPos))

    # Make sure the new position is valid
    DiffPrv = float(ReqPos) - float(PrvPos)
    DiffNxt = float(NxtPos) - float(ReqPos)

    # Only write if valid
    OutOfBounds = True
    if ((DiffPrv >= 1) and (DiffNxt >= 1)):
        BlendMap.HorzCtrPoints[col] = ReqPos
        OutOfBounds = False
    elif ((DiffPrv < 1) and (True == compress)):
        # Try to push towards previous
        if ((PrvInd > 0) and (PrvInd != (L_H - 1))):
            # Try to compress the previous points
            if (CurInd < L_H - 1):
                # Current point is on the left side
                StartInd = 0
                EndInd = PrvInd
            else:
                # Current point is on the right side
                StartInd = L_H - 1
                EndInd = PrvInd

            # Number of pixels available for redistribution
            Pixels = ReqPos - 1 - BlendMap.HorzCtrPoints[StartInd]
            N = PrvInd - StartInd + 1
            MinPixels = N - 1

            # Can we compress?
            if (Pixels < MinPixels):
                # No, jump over
                NewCol = PrvInd
            else:
                # Try to compress
                BlendMap.HorzCtrPoints[col] = ReqPos
                Delta = np.floor(Pixels/(N - 1))
                for Ind in range(StartInd + 1, EndInd + 1, 1):
                    BlendMap.HorzCtrPoints[Ind] = BlendMap.HorzCtrPoints[Ind - 1] + Delta

                # Auto-correct
                if (True == BlendMap.AutoCorrect_Control_Points_Horz()):
                    OutOfBounds = False
        else:
            # Jump over
            NewCol = PrvInd
    elif ((DiffNxt < 1) and (True == compress)):
        # Try to push towards previous
        if ((NxtInd < A_H - 1) and (NxtInd != (L_H - 1))):
            # Try to compress the previous points
            if (CurInd < L_H - 1):
                # Current point is on the left side
                StartInd = NxtInd
                EndInd = L_H - 1
            else:
                # Current point is on the right side
                StartInd = NxtInd
                EndInd = A_H - 1

            # Number of pixels available for redistribution
            Pixels = BlendMap.HorzCtrPoints[EndInd] - ReqPos - 1
            N = EndInd - NxtInd + 1
            MinPixels = N - 1

            # Can we compress?
            if (Pixels < MinPixels):
                # No, jump over
                NewCol = NxtInd
            else:
                # Try to compress
                BlendMap.HorzCtrPoints[col] = ReqPos
                Delta = np.floor(Pixels / (N - 1))
                for Ind in range(StartInd, EndInd, 1):
                    BlendMap.HorzCtrPoints[Ind] = BlendMap.HorzCtrPoints[Ind - 1] + Delta

                # Auto-correct
                if (True == BlendMap.AutoCorrect_Control_Points_Horz()):
                    OutOfBounds = False
        else:
            # Jump over
            NewCol = NxtInd

    # Is the point out of bounds?
    if (True == OutOfBounds):
        if (True == verbose):
            print('ERROR: requested position out of bounds!')
        return BlendMap, False, NewCol
    else:
        return BlendMap, True, NewCol

def EditVertControlPoint(BlendMap: map_gen.BlendMap_c, row: int, ReqPos: int, compress: bool, verbose=False):
    """
    Description: edit a BlendMap's vertical control point position

    Input arguments:
    BlendMap : a BlendMap structure
    row      : row index of the point to be edited
    ReqPos   : requested pixel position of the point to be edited
    compress : Enable or disable control point compression
    verbose  : True = print msgs to console, (default = False)

    Output arguments:
    BlendMap : a modified BlendMap structure
    Status   : status flag (boolean)
    NewRow   : row index of the current selected point (changes if a jump-over occurred)
    """
    # Constants
    A_H, L_V, L_H, NormOffset = map_gen.GetBlendMapConstants()
    NewRow = row

    # If the point is not editable, do nothing
    if ((row <= 0) or (row >= L_V - 1)):
        if (True == verbose):
            print('ERROR: requested row index is static (position cannot be edited)!')
        return BlendMap, False, NewRow

    # Get current and neighbor positions
    PrvInd = row - 1
    CurInd = row
    NxtInd = row + 1
    PrvPos = BlendMap.VertCtrPoints[PrvInd]
    CurPos = BlendMap.VertCtrPoints[CurInd]
    NxtPos = BlendMap.VertCtrPoints[NxtInd]

    # Update position
    if (True == verbose):
        print('Current y position = ' + str(CurPos), ' requested new y position = ' + str(ReqPos))

    # Make sure the new position is valid
    DiffPrv = float(ReqPos) - float(PrvPos)
    DiffNxt = float(NxtPos) - float(ReqPos)

    # Only write if valid
    OutOfBounds = True
    if ((DiffPrv >= 1) and (DiffNxt >= 1)):
        BlendMap.VertCtrPoints[row] = ReqPos
        OutOfBounds = False
    elif ((DiffPrv < 1) and (True == compress)):
        # Try to push towards previous
        if (PrvInd > 0) :
            # Try to compress the previous points
            StartInd = 0
            EndInd = PrvInd

            # Number of pixels available for redistribution
            Pixels = ReqPos - 1 - BlendMap.VertCtrPoints[StartInd]
            N = PrvInd - StartInd + 1
            MinPixels = N - 1

            # Can we compress?
            if (Pixels < MinPixels):
                # No, jump over
                NewRow = PrvInd
            else:
                # Try to compress
                BlendMap.VertCtrPoints[row] = ReqPos
                Delta = np.floor(Pixels / (N - 1))
                for Ind in range(StartInd + 1, EndInd + 1, 1):
                    BlendMap.VertCtrPoints[Ind] = BlendMap.VertCtrPoints[Ind - 1] + Delta

                # Auto-correct
                if (True == BlendMap.AutoCorrect_Control_Points_Vert()):
                    OutOfBounds = False
        else:
            # Jump over
            NewRow = PrvInd
    elif ((DiffNxt < 1) and (True == compress)):
        # Try to push towards previous
        if (NxtInd < L_V - 1):
            # Try to compress the next points
            StartInd = NxtInd
            EndInd = L_V - 1

            # Number of pixels available for redistribution
            Pixels = BlendMap.VertCtrPoints[EndInd] - ReqPos - 1
            N = EndInd - NxtInd + 1
            MinPixels = N - 1

            # Can we compress?
            if (Pixels < MinPixels):
                # No, jump over
                NewRow = NxtInd
            else:
                # Try to compress
                BlendMap.VertCtrPoints[row] = ReqPos
                Delta = np.floor(Pixels / (N - 1))
                for Ind in range(StartInd, EndInd, 1):
                    BlendMap.VertCtrPoints[Ind] = BlendMap.VertCtrPoints[Ind - 1] + Delta

                # Auto-correct
                if (True == BlendMap.AutoCorrect_Control_Points_Vert()):
                    OutOfBounds = False
        else:
            # Jump over
            NewRow = NxtInd

    # Is the point out of bounds?
    if (True == OutOfBounds):
        if (True == verbose):
            print('ERROR: requested position out of bounds!')
        return BlendMap, False, NewRow
    else:
        return BlendMap, True, NewRow

def EditHorzControlPoint_Delta(BlendMap: map_gen.BlendMap_c, col: int, Delta: int, compress: bool, verbose=False):
    """
    Description: applies a displacement (delta) in pixels to the blending map's current horizontal control point

    Input arguments:
    BlendMap : a BlendMap structure
    col      : column index of the point to be edited
    Delta    : desired displacement in pixels
    compress : Enable or disable control point compression
    verbose  : True = print msgs to console, (default = False)

    Output arguments:
    BlendMap : a modified BlendMap structure
    Status   : status flag (boolean)
    NewCol   : column index of the current selected point (changes if a jump-over occurred)
    """
    # Constants
    A_H, L_V, L_H, NormOffset = map_gen.GetBlendMapConstants()

    # If the point is not editable, do nothing
    if ((col <= 0) or (col == L_H - 1) or (col >= A_H - 1)):
        if (True == verbose):
            print('ERROR: requested column index is static (position cannot be edited)!')
        return BlendMap, False, col

    # Get current position
    CurPos = BlendMap.HorzCtrPoints[col]

    # Update position
    NewPos = CurPos + Delta

    # Try to update the map's control points
    return EditHorzControlPoint(BlendMap, col, NewPos, compress, verbose)

def EditVertControlPoint_Delta(BlendMap: map_gen.BlendMap_c, row: int, Delta: int, compress: bool, verbose=False):
    """
    Description: applies a displacement (delta) in pixels to the blending map's current vertical control point

    Input arguments:
    BlendMap : a BlendMap structure
    row      : row index of the point to be edited
    Delta    : desired displacement in pixels
    compress : Enable or disable control point compression
    verbose  : True = print msgs to console, (default = False)

    Output arguments:
    BlendMap : a modified BlendMap structure
    Status   : status flag (boolean)
    NewRow   : row index of the current selected point (changes if a jump-over occurred)
    """
    # Constants
    A_H, L_V, L_H, NormOffset = map_gen.GetBlendMapConstants()

    # If the point is not editable, do nothing
    if ((row <= 0) or (row >= L_V - 1)):
        if (True == verbose):
            print('ERROR: requested row index is static (position cannot be edited)!')
        return BlendMap, False, row

    # Get current position
    CurPos = BlendMap.VertCtrPoints[row]

    # Update position
    NewPos = CurPos + Delta

    # Try to update the map's control points
    return EditVertControlPoint(BlendMap, row, NewPos, compress, verbose)

def EditHorzControlPoints_Crowd(BlendMap: map_gen.BlendMap_c, start_pos:int, num_cols:int, separation:int, verbose=False):
    """
    Description: horizontal control point 'crowding', user selects a starting pixel position, number of columns in the
        group and separation (in pixels). The horizontal control points will be re-arranged to create an equidistant
        distribution of points. (starting at pixel position = start_pos, consisting of num_cols elements)

    Input arguments:
    BlendMap   : a BlendMap structure
    start_pos  : starting pixel position of the control point crowding group
    num_cols   : number of columns that will conform the crowding group
    separation : separation in pixels of contiguous points within the crowding group
    verbose    : True = print msgs to console, (default = False)

    Output arguments:
    BlendMap : a modified BlendMap structure
    Status   : status flag (boolean)
    """
    # Constants
    A_H, L_V, L_H, NormOffset = map_gen.GetBlendMapConstants()

    # Assert number of columns to be crowded
    if (num_cols < 2):
        if (True == verbose):
            print('WARNING: invalid number of columns!')
            print('Setting number of columns to 2...')
        num_cols = 2
    elif (num_cols > L_H - 2):
        if (True == verbose):
            print('WARNING: invalid number of columns!')
            print('Setting number of columns to {}...'.format(L_H - 2))
        num_cols = L_H - 2

    # Assert separation
    max_separation = np.floor(BlendMap.Pixels/(A_H - 1))
    if (separation < 1):
        if (True == verbose):
            print('WARNING: requested point separation is invalid!')
            print('Setting point separation to {}...'.format(1))
        separation = 1
    elif (separation > max_separation):
        if (True == verbose):
            print('WARNING: requested point separation is invalid!')
            print('Setting point separation to {}...'.format(max_separation))
        separation = max_separation

    # Find the closest position to the starting position
    min_dist = 10000
    start_col = 0
    for col in range(1, A_H - 1, 1):
        # Skip the center index
        if (col == (L_H - 1)):
            continue

        # Distance
        dist = abs(start_pos - BlendMap.HorzCtrPoints[col])
        if (dist < min_dist):
            min_dist = dist
            start_col = col

    # Move the starting point
    BlendMap.HorzCtrPoints[start_col] = start_pos
    if (start_col <= L_H - 1):
        lft_side = True
    else:
        lft_side = False

    # Crowd the points
    end_col = min(A_H, start_col + num_cols)
    for col in range(start_col, end_col, 1):
        if ((col == 0) or (col == A_H - 1)):
            continue
        elif (col == L_H -1):
            if (True == lft_side):
                break
        else:
            pos = BlendMap.HorzCtrPoints[col - 1] + separation
            BlendMap.HorzCtrPoints[col] = pos

    # Self-correct
    if (True != BlendMap.AutoCorrect_Control_Points_Horz()):
        return BlendMap, False

    # Done
    return BlendMap, True

def EditVertControlPoints_Crowd(BlendMap: map_gen.BlendMap_c, start_pos:int, num_rows:int, separation:int, verbose=False):
    """
    Description: vertical control point 'crowding', user selects a starting pixel position, number of rows in the
        group and separation (in pixels). The vertical control points will be re-arranged to create an equidistant
        distribution of points. (starting at pixel position = start_pos, consisting of num_cols elements)

    Input arguments:
    BlendMap   : a BlendMap structure
    start_pos  : starting pixel position of the control point crowding group
    num_rows   : number of rows that will conform the crowding group
    separation : separation in pixels of contiguous points within the crowding group
    verbose    : True = print msgs to console, (default = False)

    Output arguments:
    BlendMap : a modified BlendMap structure
    Status   : status flag (boolean)
    """
    # Constants
    A_H, L_V, L_H, NormOffset = map_gen.GetBlendMapConstants()

    # Assert number of columns to be crowded
    if (num_rows < 2):
        if (True == verbose):
            print('WARNING: invalid number of rows!')
            print('Setting number of columns to 2...')
        num_rows = 2
    elif (num_rows > L_V - 2):
        if (True == verbose):
            print('WARNING: invalid number of rows!')
            print('Setting number of columns to {}...'.format(L_V - 2))
        num_rows = L_V - 2

    # Assert separation
    max_separation = np.floor(BlendMap.Lines/(L_V - 1))
    if (separation < 1):
        if (True == verbose):
            print('WARNING: requested point separation is invalid!')
            print('Setting point separation to {}...'.format(1))
        separation = 1
    elif (separation > max_separation):
        if (True == verbose):
            print('WARNING: requested point separation is invalid!')
            print('Setting point separation to {}...'.format(max_separation))
        separation = max_separation

    # Find the closest position to the starting position
    min_dist = 10000
    start_row = 0
    for row in range(1, L_V - 1, 1):
        # Distance
        dist = abs(start_pos - BlendMap.VertCtrPoints[row])
        if (dist < min_dist):
            min_dist = dist
            start_row = row

    # Move the starting point
    BlendMap.VertCtrPoints[start_row] = start_pos

    # Crowd the points
    end_row = min(L_V, start_row + num_rows)
    for row in range(start_row, end_row, 1):
        if ((row == 0) or (row == L_V - 1)):
            continue
        else:
            pos = BlendMap.VertCtrPoints[row - 1] + separation
            BlendMap.VertCtrPoints[row] = pos

    # Self-correct
    if (True != BlendMap.AutoCorrect_Control_Points_Vert()):
        return BlendMap, False

    # Done
    return BlendMap, True

# -------------------------------- Gain Editing -------------------------------------- #
def EditGainPoint(BlendMap: map_gen.BlendMap_c, row: int, col:int, channel:int,  gain: float, verbose=False):
    """
    Description: sets the GAIN value to a point with index (row, col).
        Values are clipped automatically

    Input arguments:
    BlendMap : a BlendMap structure
    row      : row index of the currently selected point
    col      : column index of the currently selected point
    channel  : 0-RED, 1-GREEN, 2-BLUE or 3-all RGB channels
    gain     : GAIN value to be applied
    verbose  : True = print msgs to console, (default = False)

    Output arguments:
    BlendMap : a modified BlendMap structure
    Status   : status flag (boolean)
    """
    # Constants
    A_H, L_V, L_H, NormOffset = map_gen.GetBlendMapConstants()
    MinVal, MaxVal = map_gen.GetGainValRange()

    # Make sure the location is valid
    if ((row < 0) or (row > L_V - 1) or (col < 0) or (col > A_H - 1)):
        if (True == verbose):
            print('ERROR: invalid row/col index!')
        return BlendMap, False

    # Cap the value
    if (gain < MinVal):
        gain = MinVal
    elif (gain > MaxVal):
        gain = MaxVal

    # Set it
    if ((0 == channel) or (3 == channel)):
        BlendMap.GainRED[row][col] = gain
    elif ((1 == channel) or (3 == channel)):
        BlendMap.GainGRN[row][col] = gain
    elif ((2 == channel) or (3 == channel)):
        BlendMap.GainBLU[row][col] = gain
    else:
        if (True == verbose):
            print('ERROR: invalid channel index!')
        return BlendMap, False

    # Done
    return BlendMap, True


def EditGainRange(BlendMap: map_gen.BlendMap_c, StartRow: int, EndRow: int, StartCol: int, EndCol: int, channel: int,
                  gain: float, verbose=False):
    """
    Description: sets the GAIN value to a range of points.
        Values are clipped automatically

    Input arguments:
    BlendMap : a BlendMap structure
    StartRow : starting row index of the range
    EndRow   : ending row index of the range (inclusive)
    StartCol : starting column index of the range
    EndCol   : ending column index of the range (inclusive)
    channel  : 0-RED, 1-GREEN, 2-BLUE or 3-all RGB channels
    gain     : GAIN value to be applied to each point in the point range
    verbose  : True = print msgs to console, (default = False)

    Output arguments:
    BlendMap : a modified BlendMap structure
    Status   : status flag (boolean)
    """
    # Constants
    A_H, L_V, L_H, NormOffset = map_gen.GetBlendMapConstants()
    MinVal, MaxVal = map_gen.GetGainValRange()

    # Assert the requested channel
    if ((channel < 0) or (channel > 3)):
        if (True == verbose):
            print('ERROR: invalid channel index!')
        return BlendMap, False

    # Make sure the ranges are valid
    if ((StartRow < 0) or (StartRow > EndRow) or (EndRow > L_V - 1)):
        if (True == verbose):
            print('ERROR: invalid row range!')
        return BlendMap, False
    if ((StartCol < 0) or (StartCol > EndCol) or (EndCol > A_H - 1)):
        if (True == verbose):
            print('ERROR: invalid col range!')
        return BlendMap, False

    # Cap the value
    if (gain < MinVal):
        gain = MinVal
    elif (gain > MaxVal):
        gain = MaxVal

    # Set it
    for row in range(StartRow, EndRow + 1, 1):
        for col in range(StartCol, EndCol + 1, 1):
            if ((0 == channel) or (3 == channel)):
                BlendMap.GainRED[row][col] = gain
            if ((1 == channel) or (3 == channel)):
                BlendMap.GainGRN[row][col] = gain
            if ((2 == channel) or (3 == channel)):
                BlendMap.GainBLU[row][col] = gain
    # Done
    return BlendMap, True

def _InterpolateGainQuadrant(BlendMap: map_gen.BlendMap_c, StartRow:int, EndRow:int, StartCol:int, EndCol:int, channel:int):
    # Quadrant corners
    StartX = BlendMap.HorzCtrPoints[StartCol]
    EndX = BlendMap.HorzCtrPoints[EndCol]
    StartY = BlendMap.VertCtrPoints[StartRow]
    EndY = BlendMap.VertCtrPoints[EndRow]

    # Get the gain quadrants
    GainsRED = np.empty((4, 1), dtype=float)
    GainsGRN = np.empty((4, 1), dtype=float)
    GainsBLU = np.empty((4, 1), dtype=float)

    # Red gains
    GainsRED[0] = BlendMap.GainRED[StartRow][StartCol]
    GainsRED[1] = BlendMap.GainRED[StartRow][EndCol]
    GainsRED[2] = BlendMap.GainRED[EndRow][EndCol]
    GainsRED[3] = BlendMap.GainRED[EndRow][StartCol]

    # Green gains
    GainsGRN[0] = BlendMap.GainGRN[StartRow][StartCol]
    GainsGRN[1] = BlendMap.GainGRN[StartRow][EndCol]
    GainsGRN[2] = BlendMap.GainGRN[EndRow][EndCol]
    GainsGRN[3] = BlendMap.GainGRN[EndRow][StartCol]

    # Blue gains
    GainsBLU[0] = BlendMap.GainBLU[StartRow][StartCol]
    GainsBLU[1] = BlendMap.GainBLU[StartRow][EndCol]
    GainsBLU[2] = BlendMap.GainBLU[EndRow][EndCol]
    GainsBLU[3] = BlendMap.GainBLU[EndRow][StartCol]

    # Interpolate this quadrant
    for row in range(StartRow, EndRow + 1, 1):
        for col in range(StartCol, EndCol + 1, 1):
            # Input position
            InX = BlendMap.HorzCtrPoints[col]
            InY = BlendMap.VertCtrPoints[row]

            # Interpolated gain
            if ((0 == channel) or (3 == channel)):
                BlendMap.GainRED[row][col] = math_funcs.BilinearInterpolation_TransformSingle(InX, InY, StartX, EndX,
                                                                                   StartY, EndY, GainsRED)
            if ((1 == channel) or (3 == channel)):
                BlendMap.GainGRN[row][col] = math_funcs.BilinearInterpolation_TransformSingle(InX, InY, StartX, EndX,
                                                                                   StartY, EndY, GainsGRN)
            if ((2 == channel) or (3 == channel)):
                BlendMap.GainBLU[row][col] = math_funcs.BilinearInterpolation_TransformSingle(InX, InY, StartX, EndX,
                                                                                   StartY, EndY, GainsBLU)

    # Done
    return BlendMap

def EditGainPoint_Interpolate(BlendMap: map_gen.BlendMap_c, row: int, col:int, channel:int, gain: float, verbose=False):
    """
    Description: ets the GAIN value for a single point in the BlendMap (row, col), the rest of the points in the map
        are adjusted automatically through bi-linear interpolation.
        Interpolation occurs on a per-quadrant basis, with the currently selected point serving as a reference point.
        Values are clipped automatically

    Input arguments:
    BlendMap : a BlendMap structure
    row      : row index of the reference point
    col      : column index of the reference point
    channel  : 0-RED, 1-GREEN, 2-BLUE or 3-all RGB channels
    gain     : GAIN value to be applied to the reference point in the point range
    verbose  : True = print msgs to console, (default = False)

    Output arguments:
    BlendMap : a modified BlendMap structure
    Status   : status flag (boolean)
    """
    # Constants
    A_H, L_V, L_H, NormOffset = map_gen.GetBlendMapConstants()
    MinVal, MaxVal = map_gen.GetGainValRange()

    # Assert the requested channel
    if ((channel < 0) or (channel > 3)):
        if (True == verbose):
            print('ERROR: invalid channel index!')
        return BlendMap, False

    # Make sure the location is valid
    if ((row < 0) or (row > L_V - 1) or (col < 0) or (col > A_H - 1)):
        if (True == verbose):
            print('ERROR: invalid row/col index!')
        return BlendMap, False

    # Cap the gain
    if (gain < MinVal):
        gain = MinVal
    elif (gain > MaxVal):
        gain = MaxVal

    # Set the gain at the reference point
    if ((0 == channel) or (3 == channel)):
        BlendMap.GainRED[row][col] = gain
    if ((1 == channel) or (3 == channel)):
        BlendMap.GainGRN[row][col] = gain
    if ((2 == channel) or (3 == channel)):
        BlendMap.GainBLU[row][col] = gain

    # ----------------- Top left -----------------
    # Quadrant indices
    StartRow = 0
    EndRow = row
    StartCol = 0
    EndCol = col
    BlendMap = _InterpolateGainQuadrant(BlendMap, StartRow, EndRow, StartCol, EndCol, channel)

    # ----------------- Top right -----------------
    # Quadrant indices
    StartRow = 0
    EndRow = row
    StartCol = col
    EndCol = A_H - 1
    BlendMap = _InterpolateGainQuadrant(BlendMap, StartRow, EndRow, StartCol, EndCol, channel)

    # ----------------- Bottom right -----------------
    # Quadrant indices
    StartRow = row
    EndRow = L_V - 1
    StartCol = col
    EndCol = A_H - 1
    BlendMap = _InterpolateGainQuadrant(BlendMap, StartRow, EndRow, StartCol, EndCol, channel)

    # ----------------- Bottom left -----------------
    # Quadrant indices
    StartRow = row
    EndRow = L_V - 1
    StartCol = 0
    EndCol = col
    BlendMap = _InterpolateGainQuadrant(BlendMap, StartRow, EndRow, StartCol, EndCol, channel)

    # Done
    return BlendMap, True

# -------------------------------- Offset Editing -------------------------------------- #
def EditOffsetPoint(BlendMap: map_gen.BlendMap_c, row: int, col:int, channel:int,  offs: float, verbose=False):
    """
    Description: sets the OFFSET value to a point with index (row, col).
        Values are clipped automatically

    Input arguments:
    BlendMap : a BlendMap structure
    row      : row index of the currently selected point
    col      : column index of the currently selected point
    channel  : 0-RED, 1-GREEN, 2-BLUE or 3-all RGB channels
    offs     : OFFSET value to be applied
    verbose  : True = print msgs to console, (default = False)

    Output arguments:
    BlendMap : a modified BlendMap structure
    Status   : status flag (boolean)
    """
    # Constants
    A_H, L_V, L_H, NormOffset = map_gen.GetBlendMapConstants()
    MinVal, MaxVal = map_gen.GetOffsetValRange()

    # Make sure the location is valid
    if ((row < 0) or (row > L_V - 1) or (col < 0) or (col > A_H - 1)):
        if (True == verbose):
            print('ERROR: invalid row/col index!')
        return BlendMap, False

    # Cap the value
    if (offs < MinVal):
        offs = MinVal
    elif (offs > MaxVal):
        offs = MaxVal

    # Set it
    if ((0 == channel) or (3 == channel)):
        BlendMap.OffsetRED[row][col] = offs
    elif ((1 == channel) or (3 == channel)):
        BlendMap.OffsetGRN[row][col] = offs
    elif ((2 == channel) or (3 == channel)):
        BlendMap.OffsetBLU[row][col] = offs
    else:
        if (True == verbose):
            print('ERROR: invalid channel index!')
        return BlendMap, False

    # Done
    return BlendMap, True


def EditOffsetRange(BlendMap: map_gen.BlendMap_c, StartRow: int, EndRow: int, StartCol: int, EndCol: int, channel: int,
                    offs: float, verbose=False):
    """
    Description: sets the OFFSET value to a range of points.
        Values are clipped automatically

    Input arguments:
    BlendMap : a BlendMap structure
    StartRow : starting row index of the range
    EndRow   : ending row index of the range (inclusive)
    StartCol : starting column index of the range
    EndCol   : ending column index of the range (inclusive)
    channel  : 0-RED, 1-GREEN, 2-BLUE or 3-all RGB channels
    offs     : OFFSET value to be applied to each point in the point range
    verbose  : True = print msgs to console, (default = False)

    Output arguments:
    BlendMap : a modified BlendMap structure
    Status   : status flag (boolean)
    """
    # Constants
    A_H, L_V, L_H, NormOffset = map_gen.GetBlendMapConstants()
    MinVal, MaxVal = map_gen.GetOffsetValRange()

    # Assert the requested channel
    if ((channel < 0) or (channel > 3)):
        if (True == verbose):
            print('ERROR: invalid channel index!')
        return BlendMap, False

    # Make sure the ranges are valid
    if ((StartRow < 0) or (StartRow > EndRow) or (EndRow > L_V - 1)):
        if (True == verbose):
            print('ERROR: invalid row range!')
        return BlendMap, False
    if ((StartCol < 0) or (StartCol > EndCol) or (EndCol > A_H - 1)):
        if (True == verbose):
            print('ERROR: invalid col range!')
        return BlendMap, False

    # Cap the value
    if (offs < MinVal):
        offs = MinVal
    elif (offs > MaxVal):
        offs = MaxVal

    # Set it
    for row in range(StartRow, EndRow + 1, 1):
        for col in range(StartCol, EndCol + 1, 1):
            if ((0 == channel) or (3 == channel)):
                BlendMap.OffsetRED[row][col] = offs
            if ((1 == channel) or (3 == channel)):
                BlendMap.OffsetGRN[row][col] = offs
            if ((2 == channel) or (3 == channel)):
                BlendMap.OffsetBLU[row][col] = offs
    # Done
    return BlendMap, True

def _InterpolateOffsetQuadrant(BlendMap: map_gen.BlendMap_c, StartRow:int, EndRow:int, StartCol:int, EndCol:int, channel:int):
    # Quadrant corners
    StartX = BlendMap.HorzCtrPoints[StartCol]
    EndX = BlendMap.HorzCtrPoints[EndCol]
    StartY = BlendMap.VertCtrPoints[StartRow]
    EndY = BlendMap.VertCtrPoints[EndRow]

    # Get the gain quadrants
    OffsetsRED = np.empty((4, 1), dtype=float)
    OffsetsGRN = np.empty((4, 1), dtype=float)
    OffsetsBLU = np.empty((4, 1), dtype=float)

    # Red Offsets
    OffsetsRED[0] = BlendMap.OffsetRED[StartRow][StartCol]
    OffsetsRED[1] = BlendMap.OffsetRED[StartRow][EndCol]
    OffsetsRED[2] = BlendMap.OffsetRED[EndRow][EndCol]
    OffsetsRED[3] = BlendMap.OffsetRED[EndRow][StartCol]

    # Green Offsets
    OffsetsGRN[0] = BlendMap.OffsetGRN[StartRow][StartCol]
    OffsetsGRN[1] = BlendMap.OffsetGRN[StartRow][EndCol]
    OffsetsGRN[2] = BlendMap.OffsetGRN[EndRow][EndCol]
    OffsetsGRN[3] = BlendMap.OffsetGRN[EndRow][StartCol]

    # Blue Offsets
    OffsetsBLU[0] = BlendMap.OffsetBLU[StartRow][StartCol]
    OffsetsBLU[1] = BlendMap.OffsetBLU[StartRow][EndCol]
    OffsetsBLU[2] = BlendMap.OffsetBLU[EndRow][EndCol]
    OffsetsBLU[3] = BlendMap.OffsetBLU[EndRow][StartCol]

    # Interpolate this quadrant
    for row in range(StartRow, EndRow + 1, 1):
        for col in range(StartCol, EndCol + 1, 1):
            # Input position
            InX = BlendMap.HorzCtrPoints[col]
            InY = BlendMap.VertCtrPoints[row]

            # Interpolated gain
            if ((0 == channel) or (3 == channel)):
                BlendMap.OffsetRED[row][col] = math_funcs.BilinearInterpolation_TransformSingle(InX, InY, StartX, EndX,
                                                                                   StartY, EndY, OffsetsRED)
            if ((1 == channel) or (3 == channel)):
                BlendMap.OffsetGRN[row][col] = math_funcs.BilinearInterpolation_TransformSingle(InX, InY, StartX, EndX,
                                                                                   StartY, EndY, OffsetsGRN)
            if ((2 == channel) or (3 == channel)):
                BlendMap.OffsetBLU[row][col] = math_funcs.BilinearInterpolation_TransformSingle(InX, InY, StartX, EndX,
                                                                                   StartY, EndY, OffsetsBLU)

    # Done
    return BlendMap

def EditOffsetPoint_Interpolate(BlendMap: map_gen.BlendMap_c, row: int, col:int, channel:int,  offs: float, verbose=False):
    """
    Description: sets the OFFSET value for a single point in the BlendMap (row, col), the rest of the points in the map
        are adjusted automatically through bi-linear interpolation.
        Interpolation occurs on a per-quadrant basis, with the currently selected point serving as a reference point.
        Values are clipped automatically

    Input arguments:
    BlendMap : a BlendMap structure
    row      : row index of the reference point
    col      : column index of the reference point
    channel  : 0-RED, 1-GREEN, 2-BLUE or 3-all RGB channels
    offs     : OFFSET value to be applied to the reference point in the point range
    verbose  : True = print msgs to console, (default = False)

    Output arguments:
    BlendMap : a modified BlendMap structure
    Status   : status flag (boolean)
    """
    # Constants
    A_H, L_V, L_H, NormOffset = map_gen.GetBlendMapConstants()
    MinVal, MaxVal = map_gen.GetOffsetValRange()

    # Assert the requested channel
    if ((channel < 0) or (channel > 3)):
        if (True == verbose):
            print('ERROR: invalid channel index!')
        return BlendMap, False

    # Make sure the location is valid
    if ((row < 0) or (row > L_V - 1) or (col < 0) or (col > A_H - 1)):
        if (True == verbose):
            print('ERROR: invalid row/col index!')
        return BlendMap, False

    # Cap the gain
    if (offs < MinVal):
        offs = MinVal
    elif (offs > MaxVal):
        offs = MaxVal

    # Set the gain at the reference point
    if ((0 == channel) or (3 == channel)):
        BlendMap.OffsetRED[row][col] = offs
    if ((1 == channel) or (3 == channel)):
        BlendMap.OffsetGRN[row][col] = offs
    if ((2 == channel) or (3 == channel)):
        BlendMap.OffsetBLU[row][col] = offs

    # ----------------- Top left -----------------
    # Quadrant indices
    StartRow = 0
    EndRow = row
    StartCol = 0
    EndCol = col
    BlendMap = _InterpolateOffsetQuadrant(BlendMap, StartRow, EndRow, StartCol, EndCol, channel)

    # ----------------- Top right -----------------
    # Quadrant indices
    StartRow = 0
    EndRow = row
    StartCol = col
    EndCol = A_H - 1
    BlendMap = _InterpolateOffsetQuadrant(BlendMap, StartRow, EndRow, StartCol, EndCol, channel)

    # ----------------- Bottom right -----------------
    # Quadrant indices
    StartRow = row
    EndRow = L_V - 1
    StartCol = col
    EndCol = A_H - 1
    BlendMap = _InterpolateOffsetQuadrant(BlendMap, StartRow, EndRow, StartCol, EndCol, channel)

    # ----------------- Bottom left -----------------
    # Quadrant indices
    StartRow = row
    EndRow = L_V - 1
    StartCol = 0
    EndCol = col
    BlendMap = _InterpolateOffsetQuadrant(BlendMap, StartRow, EndRow, StartCol, EndCol, channel)

    # Done
    return BlendMap, True
