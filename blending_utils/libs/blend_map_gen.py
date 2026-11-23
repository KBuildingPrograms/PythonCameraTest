#  Imports
if __name__ == '__main__' or __name__ == 'blend_map_gen':
    import license_strings as lic
else:
    from . import license_strings as lic
import numpy as np
import os

# Module metadata
__copyright__ = lic.copyright_str
__author__ = lic.author
__status__ = lic.status
__doc__ = "DESCRIPTION: Blending Map definition library (API)"

#-------------------------------- Constants --------------------------------------#
A_H = 63
L_V = 32
L_H = 32
NormOffset = 100.00

def GetBlendMapConstants():
    """
    Description       : returns the HW-related BlendMap constants

    Input arguments:
    None

    Output arguments:
    A_H        : Number of horizontal samples in BlendMap
    L_V        : Number of vertical samples in BlendMap
    L_H        : Number of single data path horizontal samples in BlendMap
    NormOffset : Offset normalization range
    """
    return A_H, L_V, L_H, NormOffset

def GetGainValRange():
    """
    Description: returns the range of valid values for GAIN

    Input arguments:
    None

    Output arguments:
    MinVal : Minimum GAIN value allowed
    MaxVal : Maximum GAIN value allowed
    """
    MaxVal = 1 + ((1 << 12) - 1)/(1 << 12)
    MinVal = 0
    return MinVal, MaxVal

def GetOffsetValRange():
    """
    Description: returns the range of valid values for OFFSET

    Input arguments:
    None

    Output arguments:
    MinVal : Minimum OFFSET value allowed
    MaxVal : Maximum OFFSET value allowed
    """
    MaxVal = NormOffset
    MinVal = -1*NormOffset
    return MinVal, MaxVal

#-------------------------------- Define edge blending map class ----------------------------------#
class BlendMap_c:
    """
    Description: class representation of a BlendMap structure. The BlendMap encodes the user-defined photometric
    adjustments for a particular scenario. Information contained in the BlendMap includes:
    * DMD resolution
    * Horizontal control points: 1D array, 63 entries deep (A_H)
    * Vertical control points: 1D array, 32 entries deep (L_V)
    * RED GAIN: 2D array, 32x63 (L_V*L_H)
    * GREEN GAIN: 2D array, 32x63 (L_V*A_H)
    * BLUE GAIN: 2D array, 32x63 (L_V*A_H)
    * RED OFFSET: 2D array, 32x63 (L_V*A_H)
    * GREEN OFFSET: 2D array, 32x63 (L_V*A_H)
    * BLUE OFFSET: 2D array, 32x63 (L_V*A_H)
    """
    # Default constructor
    def __init__(self, name):
        # Name of instance
        self.name = name

        # Resolution
        self.Pixels: np.ushort
        self.Lines: np.ushort
        self.HalfPixels: np.ushort

        # Control points
        self.HorzCtrPoints = np.empty(A_H, dtype=int)
        self.VertCtrPoints = np.empty(L_V, dtype=int)

        # Gain
        self.GainRED = np.empty((L_V, A_H), dtype=float)
        self.GainGRN = np.empty((L_V, A_H), dtype=float)
        self.GainBLU = np.empty((L_V, A_H), dtype=float)

        # Offset
        self.OffsetRED = np.empty((L_V, A_H), dtype=float)
        self.OffsetGRN = np.empty((L_V, A_H), dtype=float)
        self.OffsetBLU = np.empty((L_V, A_H), dtype=float)

    #-----------------Initialization method -------------------#
    def Initialize(self, Pixels, Lines):
        """
        Description: self-initialization to a nominal BlendMap with a DMD resolution = Pixels x Lines

        Input arguments:
        Pixels: DMD horizontal resolution
        Lines : DMD vertical resolution

        Output arguments:
        None, modifies the class' instance
        """
        # DMD Resolution
        self.Pixels = Pixels
        self.Lines = Lines
        self.HalfPixels = int(np.floor(self.Pixels/2))

        # Horizontal control points
        HStep = (self.Pixels  - 1.0)/ (A_H - 1)
        for col in range(0, A_H, 1):
            HVal = np.floor(col*HStep + 0.5)
            self.HorzCtrPoints[col] = HVal
        self.HorzCtrPoints[0] = 0
        self.HorzCtrPoints[L_H - 1] = self.HalfPixels - 1
        self.HorzCtrPoints[A_H - 1] = self.Pixels - 1

        # Vertical control points
        VStep = (self.Lines  - 1.0)/ (L_V - 1)
        for row in range(0, L_V, 1):
            VVal = np.floor(row*VStep + 0.5)
            self.VertCtrPoints[row] = VVal
        self.VertCtrPoints[0] = 0
        self.VertCtrPoints[L_V - 1] = self.Lines - 1

        # Gain and offset
        for row in range(0, L_V, 1):
            for col in range(0, A_H, 1):
                self.GainRED[row][col] = 1.0
                self.GainGRN[row][col] = 1.0
                self.GainBLU[row][col] = 1.0
                self.OffsetRED[row][col] = 0.0
                self.OffsetGRN[row][col] = 0.0
                self.OffsetBLU[row][col] = 0.0

    #-----------------Self assertion methods -------------------#
    def Assert_Control_Points(self):
        """
        Description: self-assertion of horizontal and vertical control points. Looks for HW constraint violations

        Input arguments:
        None

        Output arguments:
        None, modifies class' instance
        """
        # Horizontal control point range
        # Precision is u12.0
        MaxVal = (1 << 12) - 1
        MinVal = 0
        for i in range(0, A_H, 1):
            Val = self.HorzCtrPoints[i]
            if ((Val < MinVal) or (Val > MaxVal)):
                print('Blending map assertion failed!')
                print('Horizontal control points out of range, index = ' + str(i) + ' value = ' + str(Val))
                return False

        # Vertical control point range
        # Precision is u12.0
        MaxVal = (1 << 12) - 1
        MinVal = 0
        for i in range(0, L_V, 1):
            Val = self.VertCtrPoints[i]
            if ((Val < MinVal) or (Val > MaxVal)):
                print('Blending map assertion failed!')
                print('Vertical control points out of range, index = ' + str(i) + ' value = ' + str(Val))
                return False

        # Horizontal control separation
        MinVal = 1
        for i in range(1, A_H, 1):
            Val = float(self.HorzCtrPoints[i]) - float(self.HorzCtrPoints[i - 1])
            if (Val < MinVal) :
                print('Blending map assertion failed!')
                print('Horizontal control minimum supported separation violation, index = ' + str(i) + ' value = ' + str(Val))
                return False

        # Vertical control separation
        MinVal = 1
        for i in range(1, L_V, 1):
            Val = float(self.VertCtrPoints[i]) - float(self.VertCtrPoints[i - 1])
            if (Val < MinVal) :
                print('Blending map assertion failed!')
                print('Vertical control minimum supported separation violation, index = ' + str(i) + ' value = ' + str(Val))
                return False

        # Control point boundary assertions
        # First
        Ind = 0
        Val = self.HorzCtrPoints[Ind]
        RefVal = 0
        if (Val != RefVal):
            print('Blending map assertion failed!')
            print('Horizontal control fixed boundary violation, index = ' + str(i) + ' value = ' + str(Val))
            return False

        # Middle
        Ind = L_H - 1
        Val = self.HorzCtrPoints[Ind]
        RefVal = self.HalfPixels - 1
        if (Val != RefVal):
            print('Blending map assertion failed!')
            print('Horizontal control fixed boundary violation, index = ' + str(i) + ' value = ' + str(Val))
            return False

        # Last
        Ind = A_H - 1
        Val = self.HorzCtrPoints[Ind]
        RefVal = self.Pixels - 1
        if (Val != RefVal):
            print('Blending map assertion failed!')
            print('Horizontal control fixed boundary violation, index = ' + str(i) + ' value = ' + str(Val))
            return False

        # First
        Ind = 0
        Val = self.VertCtrPoints[Ind]
        RefVal = 0
        if (Val != RefVal):
            print('Blending map assertion failed!')
            print('Vertical control fixed boundary violation, index = ' + str(i) + ' value = ' + str(Val))
            return False

        # Last
        Ind = L_V - 1
        Val = self.VertCtrPoints[Ind]
        RefVal = self.Lines - 1
        if (Val != RefVal):
            print('Blending map assertion failed!')
            print('Vertical control fixed boundary violation, index = ' + str(i) + ' value = ' + str(Val))
            return False

        
        # Assertion passed
        return True

    def Assert_Gain(self, start_row, end_row, start_col, end_col):
        """
        Description: self-assertion of GAIN points in a range

        Input arguments:
        start_row: starting row index in point range
        end_row  : ending row index in point range
        start_col: starting column index in point range
        end_col  : ending column index in point range

        Output arguments:
        Status  : boolean flag, (True = assertion passed, False = assertion failed)
        """
        # Assert the requested index range
        if ((start_row < 0) or (start_row > end_row) or (end_row >= L_V)):
            print('ERROR: requested row range is invalid!')
            return False
        if ((start_col < 0) or (start_col > end_col) or (end_col >= A_H)):
            print('ERROR: requested column index is out of range!')
            return False

        # Range
        # Precision is u1.12, this means that the supported range is 0 to 1.999755859375 or 1 + 4095/4096
        MaxVal = 1 + ((1 << 12) - 1)/(1 << 12)
        MinVal = 0
        for row in range(start_row, end_row + 1, 1):
            for col in range(start_col, end_col + 1, 1):
                # RED
                Val = self.GainRED[row][col]
                if ((Val < MinVal) or (Val > MaxVal)):
                    print('Blending map assertion failed!')
                    print('RED gain value out of range, row = ' + str(row)  +  ' col = ' + str(col) + ' value = ' + str(Val))
                    return False

                # GRN
                Val = self.GainGRN[row][col]
                if ((Val < MinVal) or (Val > MaxVal)):
                    print('Blending map assertion failed!')
                    print('GRN gain value out of range, row = ' + str(row)  +  ' col = ' + str(col) + ' value = ' + str(Val))
                    return False
                
                # BLU
                Val = self.GainBLU[row][col]
                if ((Val < MinVal) or (Val > MaxVal)):
                    print('Blending map assertion failed!')
                    print('BLU gain value out of range, row = ' + str(row)  +  ' col = ' + str(col) + ' value = ' + str(Val))
                    return False

        # Assertion passed
        return True

    def Assert_Offset(self, start_row, end_row, start_col, end_col):
        """
        Description: self-assertion of OFFSET points in a range

        Input arguments:
        start_row: starting row index in point range
        end_row  : ending row index in point range
        start_col: starting column index in point range
        end_col  : ending column index in point range

        Output arguments:
        Status  : boolean flag, (True = assertion passed, False = assertion failed)
        """
        # Assert the requested indices
        if ((start_row < 0) or (start_row > end_row) or (end_row >= L_V)):
            print('ERROR: requested row range is invalid!')
            return False
        if ((start_col < 0) or (start_col > end_col) or (end_col >= A_H)):
            print('ERROR: requested column index is out of range!')
            return False

        # Offset LUTs range
        # Precision is FPL s1m8e4, get the ranges. However, user exposed range is -100.00 to +100.00
        MaxVal = NormOffset
        MinVal = -1*NormOffset
        for row in range(start_row, end_row + 1, 1):
            for col in range(start_col, end_col + 1, 1):
                # RED
                Val = self.OffsetRED[row][col]
                if ((Val < MinVal) or (Val > MaxVal)):
                    print('Blending map assertion failed!')
                    print('RED offset value out of range, row = ' + str(row)  +  ' col = ' + str(col) + ' value = ' + str(Val))
                    return False

                # GRN
                Val = self.OffsetGRN[row][col]
                if ((Val < MinVal) or (Val > MaxVal)):
                    print('Blending map assertion failed!')
                    print('GRN offset value out of range, row = ' + str(row)  +  ' col = ' + str(col) + ' value = ' + str(Val))
                    return False

                # BLU
                Val = self.OffsetBLU[row][col]
                if ((Val < MinVal) or (Val > MaxVal)):
                    print('Blending map assertion failed!')
                    print('BLU offset value out of range, row = ' + str(row)  +  ' col = ' + str(col) + ' value = ' + str(Val))
                    return False

        # Assertion passed
        return True

    def Assert(self, AssertCtr):
        """
         Description: self-assertion of all BlendMap components

         Input arguments:
         AssertCtr: Assert (True) or not (False) the BlendMap control points

         Output arguments:
         Status  : boolean flag, (True = assertion passed, False = assertion failed)
         """
        # Control points
        if (True == AssertCtr):
            if (True != self.Assert_Control_Points()):
                return False
        
        # Gain
        if (True != self.Assert_Gain(0, L_V - 1, 0, A_H - 1)):
            return False

        # Offset 
        if (True != self.Assert_Offset(0, L_V - 1, 0, A_H - 1)):
            return False

        # Assertion passed
        return True

    # ----------------- Self-correction  -------------------#
    def AutoCorrect_Control_Points_Horz(self):
        """
        Description: self-corrects the horizontal control points if violations to HW constraints are encountered

        Input arguments:
        None

        Output arguments:
        Status  : boolean flag, (True = correction successful, False = correction failed)
        """
        # Fixed points
        self.HorzCtrPoints[0] = 0
        self.HorzCtrPoints[L_H - 1] = self.HalfPixels - 1
        self.HorzCtrPoints[A_H - 1] = self.Pixels - 1

        # Correct interior points
        for i in range(1, A_H - 1):
            # Skip center point
            if (i == L_H - 1):
                continue

            # Distances
            dist1 = self.HorzCtrPoints[i] - self.HorzCtrPoints[i - 1]
            dist2 = self.HorzCtrPoints[i + 1] - self.HorzCtrPoints[i]

            # If both distances are less than 1, something went really wrong
            if ((dist1 < 1) and (dist2 < 1)):
                # Invalid, we cannot recover from this
                print('ERROR: cannot perform control point self correction!')
                print('Please re-initialize the control point distribution...')
                return False

            # Correct if needed and possible
            if (dist1 < 1):
                # Push right
                self.HorzCtrPoints[i] += 1
            elif (dist2 < 1):
                # Push left
                self.HorzCtrPoints[i] -= 1

        # Done
        return True

    def AutoCorrect_Control_Points_Vert(self):
        """
        Description: self-corrects the vertical control points if violations to HW constraints are encountered

        Input arguments:
        None

        Output arguments:
        Status  : boolean flag, (True = correction successful, False = correction failed)
        """
        # Fixed points
        self.VertCtrPoints[0] = 0
        self.VertCtrPoints[L_V - 1] = self.Lines - 1

        # Correct interior points
        for i in range(1, L_V - 1):
            # Distances
            dist1 = self.VertCtrPoints[i] - self.VertCtrPoints[i - 1]
            dist2 = self.VertCtrPoints[i + 1] - self.VertCtrPoints[i]

            # If both distances are less than 1, something went really wrong
            if ((dist1 < 1) and (dist2 < 1)):
                # Invalid, we cannot recover from this
                print('ERROR: cannot perform control point self correction!')
                print('Please re-initialize the control point distribution...')
                return False

            # Correct if needed and possible
            if (dist1 < 1):
                # Push down
                self.VertCtrPoints[i] += 1
            elif (dist2 < 1):
                # Push up
                self.VertCtrPoints[i] -= 1

        # Done
        return True
    #----------------- TXT I/O -------------------#
    def SaveToTXT(self, MapFileName: str) ->bool:
        """
        Description: saves the current instance's contents to a text file; user defines the name of the file

        Input arguments:
        MapFileName : file name (user defined) of the TXT file in which the BlendMap will be saved (must include
            extension)

        Output arguments:
        Status : status flag (Pass/fail)
        """
         # Open the file for writing
        file1 = open(MapFileName, "w")

        # Write the map line by line
        # Display resolution
        file1.write(str(self.Pixels) + '\n')
        file1.write(str(self.Lines) + '\n')

        # Horizontal control points
        for col in range(0, A_H, 1):
            file1.write(str(self.HorzCtrPoints[col]) + '\n')

        # Vertical control points
        for row in range(0, L_V, 1):
            file1.write(str(self.VertCtrPoints[row]) + '\n')

        # Red GAIN
        for row in range(0, L_V, 1):
            for col in range(0, A_H, 1):
                file1.write("{:.4f}\n".format(self.GainRED[row][col]))

        # Green GAIN
        for row in range(0, L_V, 1):
            for col in range(0, A_H, 1):
                file1.write("{:.4f}\n".format(self.GainGRN[row][col]))

        # Blue GAIN
        for row in range(0, L_V, 1):
            for col in range(0, A_H, 1):
                file1.write("{:.4f}\n".format(self.GainBLU[row][col]))

        # Red OFFSET
        for row in range(0, L_V, 1):
            for col in range(0, A_H, 1):
                file1.write("{:.4f}\n".format(self.OffsetRED[row][col]))

        # Green OFFSET
        for row in range(0, L_V, 1):
            for col in range(0, A_H, 1):
                file1.write("{:.4f}\n".format(self.OffsetGRN[row][col]))

        # Blue OFFSET
        for row in range(0, L_V, 1):
            for col in range(0, A_H, 1):
                file1.write("{:.4f}\n".format(self.OffsetBLU[row][col]))

        # Close the file
        file1.close()

        # Done
        return True

    def LoadFromTXT(self, MapFileName: str) ->bool:
        """
            Description: populates the current BlendMap instance with the contents of a BlendMap's text file.
            NOTE: loaded file MUST be from a previous call to self.SaveToTXT function

            Input arguments:
            MapFileName : file name (user defined) of the TXT file in which the BlendMap will be saved (must include
            extension)

            Output arguments:
            Status : status flag (Pass/fail)
        """
        # Try to open the file
        if (True != os.path.isfile(MapFileName)):
            print('ERROR: could not open ' + MapFileName + '!')
            return False
        else:
            file1 = open(MapFileName, "r")

        # Tokenize the file
        Entries = file1.readlines()

        # Close the file
        file1.close()

        # Make sure we have enough entries
        NumEntries = 2 + A_H + L_V + 3*A_H*L_V + 3*A_H*L_V
        if (len(Entries) < NumEntries):
            print('ERROR: not enough entries in ' + MapFileName + '!')
            return False
        

        # Load display resolution
        Ind = 0
        Pixels = int(Entries[Ind])
        Ind += 1
        Lines = int(Entries[Ind])
        Ind += 1

        # Initialize the map
        self.Initialize(Pixels, Lines)

        # Populate the control points
        for col in range(0, A_H, 1):
            self.HorzCtrPoints[col] = int(Entries[Ind])
            Ind += 1
        
        for row in range(0, L_V, 1):
            self.VertCtrPoints[row] = int(Entries[Ind])
            Ind += 1

        # Populate the gain arrays
        for row in range(0, L_V, 1):
            for col in range(0, A_H, 1):
                self.GainRED[row][col] = float(Entries[Ind])
                Ind += 1
        for row in range(0, L_V, 1):
            for col in range(0, A_H, 1):
                self.GainGRN[row][col] = float(Entries[Ind])
                Ind += 1
        for row in range(0, L_V, 1):
            for col in range(0, A_H, 1):
                self.GainBLU[row][col] = float(Entries[Ind])
                Ind += 1

        # Populate the offset arrays
        for row in range(0, L_V, 1):
            for col in range(0, A_H, 1):
                self.OffsetRED[row][col] = float(Entries[Ind])
                Ind += 1
        for row in range(0, L_V, 1):
            for col in range(0, A_H, 1):
                self.OffsetGRN[row][col] = float(Entries[Ind])
                Ind += 1
        for row in range(0, L_V, 1):
            for col in range(0, A_H, 1):
                self.OffsetBLU[row][col] = float(Entries[Ind])
                Ind += 1

        # Validate the map
        if (True != self.Assert(True)):
            print('ERROR: map assertion failed!')
            print('Could not load map data from ' + MapFileName + '...')
            return False

        # Done
        return True
