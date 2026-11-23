# Imports
if __name__ == '__main__' or __name__ == 'blend_map_luts':
    import license_strings as lic
    import dlpc754x.commands as cmds
    import blend_map_gen as map_gen
    import fpl_lib as fpl
else:
    from ..libs import license_strings as lic
    from ..libs.dlpc754x import commands as cmds
    from . import blend_map_gen as map_gen
    from . import fpl_lib as fpl
import numpy as np
from typing import Tuple

# Module metadata
__copyright__ = lic.copyright_str
__author__ = lic.author
__status__ = lic.status
__doc__ = "DESCRIPTION: Blending Map LUT Generation Library (API)"

#-------------------------------------------- Define EBF LUT class for CMD access--------------------------------------------#
class BlendMapLUT_c:
    """
            Description: class representation of a BlendMapLUT object in ASIC-friendly format, this class takes a
            BlendMap object and converts it into EBF (Edge Blending Function) HW LUT data that can be loaded to a
            7540 system via commands.
            Information contained in the BlendMapLUT includes:
            * DMD resolution
            * Horizontal control points: 1D array, 63 entries deep (A_H)
            * Vertical control points: 1D array, 32 entries deep (L_V)
            * RED GAIN: 2D array, 32x63 (L_V*A_H)
            * GREEN GAIN: 2D array, 32x63 (L_V*A_H)
            * BLUE GAIN: 2D array, 32x63 (L_V*A_H)
            * RED OFFSET: 2D array, 32x63 (L_V*A_H)
            * GREEN OFFSET: 2D array, 32x63 (L_V*A_H)
            * BLUE OFFSET: 2D array, 32x63 (L_V*A_H)
        """
    #--------------- Default constructor -------------#
    def __init__(self, name):
        # Name of instance
        self.name = name

        # Resolution
        self.Pixels : np.ushort
        self.Lines : np.ushort

        # CH0 LUTs
        self.HorzPts= np.empty(map_gen.A_H, dtype=np.uint32)
        self.VertPts = np.empty(map_gen.L_V, dtype=np.uint32)
        self.GainRED = np.empty((map_gen.L_V, map_gen.A_H), dtype=np.uint32)
        self.GainGRN = np.empty((map_gen.L_V, map_gen.A_H), dtype=np.uint32)
        self.GainBLU = np.empty((map_gen.L_V, map_gen.A_H), dtype=np.uint32)
        self.OffsetRED = np.empty((map_gen.L_V, map_gen.A_H), dtype=np.uint32)
        self.OffsetGRN = np.empty((map_gen.L_V, map_gen.A_H), dtype=np.uint32)
        self.OffsetBLU = np.empty((map_gen.L_V, map_gen.A_H), dtype=np.uint32)

    #--------------- Generate LUT data out of a blend map ---------------#
    def GenLUTs_Control_Points(self, BlendMap : map_gen.BlendMap_c):
        """
        Description: (self) computes and returns a BlendMap's control points LUT data

        Input arguments:
        BlendMap: a BlendMap object

        Output arguments:
        None
        """
        # Constants
        map_gen.A_H, map_gen.L_V, L_H, NormOffset = map_gen.GetBlendMapConstants()

        # Resolution
        self.Pixels = BlendMap.Pixels
        self.Lines = BlendMap.Lines

        # Assert the blending map contents
        if (True != BlendMap.Assert_Control_Points()):
            return False

        # Control points: split into two channels. Precision is u12.0, just round to nearest valid point.
        MaxVal = (1 << 12) - 1

        # Horizontal
        for i in range(0, map_gen.A_H, 1):
            self.HorzPts[i] = int(np.floor(BlendMap.HorzCtrPoints[i] + 0.5)) & MaxVal

        # Vertical
        for i in range(0, map_gen.L_V, 1):
            self.VertPts[i] = int(np.floor(BlendMap.VertCtrPoints[i] + 0.5)) & MaxVal

        # Done
        return  True
    
    def GenLUTs_GainAndOffset(self, BlendMap : map_gen.BlendMap_c, start_row, end_row, start_col, end_col):
        """
        Description: (self) computes a BlendMap's GAIN and OFFSET LUT data (populates this instance's
        internal arrays). Supports partial LUT generation (range of points)

        Input arguments:
        BlendMap  : a BlendMap object
        start_row : control point range starting row index
        end_row   : control point range ending row index (inclusive)
        start_col : control point range starting column index
        end_col   : control point range ending column index (inclusive)

        Output arguments:
        Status : pass/fail
        """
        # Constants
        map_gen.A_H, map_gen.L_V, L_H, NormOffset = map_gen.GetBlendMapConstants()

        # Assert the requested index range
        if ((start_row < 0) or (start_row > end_row) or (end_row >= map_gen.L_V)):
            print('ERROR: requested row range is invalid!')
            return False
        if ((start_col < 0) or (start_col > end_col) or (end_col >= map_gen.A_H)):
            print('ERROR: requested column index is out of range!')
            return False    

        # Initialize status to false
        Status = False

        # Assert the blending map contents (single point)

        if ((True != BlendMap.Assert_Gain(start_row, end_row, start_col, end_col)) or
            (True != BlendMap.Assert_Offset(start_row, end_row, start_col, end_col))):
            return Status

        # Gain LUTs: recision is u1.12, this means that the supported range is  0 to 1.999755859375 or 1 + 4095/4096
        DecimalPoints = 12
        MaxVal = 1 + ((1 << DecimalPoints) - 1)/(1 << DecimalPoints)
        MinVal = 0
        for row in range(start_row, end_row + 1, 1):
            for col in range(start_col, end_col + 1, 1):
                # Red
                Val = BlendMap.GainRED[row][col]
                if (Val < MinVal):
                    Val = MinVal
                elif (Val > MaxVal):
                    Val = MaxVal
                self.GainRED[row][col] = int(np.fix(Val*(1 << DecimalPoints))) 
                
                # Green
                Val = BlendMap.GainGRN[row][col]
                if (Val < MinVal):
                    Val = MinVal
                elif (Val > MaxVal):
                    Val = MaxVal
                self.GainGRN[row][col] = int(np.fix(Val*(1 << DecimalPoints)))

                # Blue
                Val = BlendMap.GainBLU[row][col]
                if (Val < MinVal):
                    Val = MinVal
                elif (Val > MaxVal):
                    Val = MaxVal
                self.GainBLU[row][col] = int(np.fix(Val*(1 << DecimalPoints)))

        # Offset LUTs: precision is s1m8e4, this means that the supported range is  -8372224 to 8372224
        min_p, max_p, min_n, max_n = fpl.get_range(1, 8, 4)
        MaxVal = max_p
        MinVal = max_n
        for row in range(start_row, end_row + 1, 1):
            for col in range(start_col, end_col + 1, 1):
                # Red
                Val = np.floor(MaxVal*BlendMap.OffsetRED[row][col]/NormOffset)
                if (Val < MinVal):
                    Val = MinVal
                elif (Val > MaxVal):
                    Val = MaxVal
                FixedVal = int(np.floor(Val + 0.5))
                self.OffsetRED[row][col] = fpl.fixed_to_float(FixedVal, 1, 8, 4)

                # Green
                Val = np.floor(MaxVal*BlendMap.OffsetGRN[row][col]/NormOffset)
                if (Val < MinVal):
                    Val = MinVal
                elif (Val > MaxVal):
                    Val = MaxVal
                FixedVal = int(np.floor(Val + 0.5))
                self.OffsetGRN[row][col] = fpl.fixed_to_float(FixedVal, 1, 8, 4)

                # Blue
                Val = np.floor(MaxVal*BlendMap.OffsetBLU[row][col]/NormOffset)
                if (Val < MinVal):
                    Val = MinVal
                elif (Val > MaxVal):
                    Val = MaxVal
                FixedVal = int(np.floor(Val + 0.5))
                self.OffsetBLU[row][col] = fpl.fixed_to_float(FixedVal, 1, 8, 4)

        # All right
        Status = True

        # Done
        return  Status

    def GenBlendMapLUTs(self, BlendMap : map_gen.BlendMap_c):
        """
        Description: generates a BlendMap's ALL LUT data (populates this instance's internal arrays). For all points
        in the BlendMap.

        Input arguments:
        BlendMap: a BlendMap object

        Output arguments:
        Status: pass/fail
        """
        # Constants
        map_gen.A_H, map_gen.L_V, L_H, NormOffset = map_gen.GetBlendMapConstants()

        # Create the control points LUT data (this function sets the blend lut class resolution data, and asserts the control points)
        Status = self.GenLUTs_Control_Points(BlendMap)
        if (True != Status):
            return False

        # Create the gain and offset LUT data (set the range to full)
        Status = self.GenLUTs_GainAndOffset(BlendMap, 0, map_gen.L_V - 1, 0, map_gen.A_H - 1)
        if (True != Status):
            return False

        # Done
        return True

#-------------------------------------------- Write Blend Map LUT data to system --------------------------------------------#
def WriteBlendMapLUTs_Control_Points(BlendMap: map_gen.BlendMap_c, BlendMapLUT: BlendMapLUT_c, ApplyMap: bool) -> bool:
    """
    Description: takes a BlendMap object, a BlendMapLUT object, writes it to a connected 7540
    system via command and applies the changes in HW.
    Requires a 7540 system connected to the host PC via USB.

    Input arguments:
    BlendMap    : a BlendMap object (containing blending map data)
    BlendMapLUT : a BlendMapLUT object (containing blending LUT data)
    ApplyMap    : True = immediately apply blending LUT data in HW

    Output arguments:
    Status : pass/fail
    """
    #------------- Constants -------------#
    map_gen.A_H, map_gen.L_V, L_H, NormOffset = map_gen.GetBlendMapConstants()

    #------------- Command success flag #-------------#
    Status = True

    #------------- Create the LUT data --------------#
    Status = BlendMapLUT.GenLUTs_Control_Points(BlendMap)
    if (Status != True):
        return False

    #------------- Write the LUT data --------------#
    Status &= cmds.WriteBlendMapControlPoints(BlendMap.Pixels, BlendMap.Lines, BlendMapLUT.HorzPts.tolist(), BlendMapLUT.VertPts.tolist()).Successful
    if (Status != True):
        return False

    #------------------ Should the map be applied? -------------------#
    if (True == ApplyMap):
        #------------- Is blending enabled? -------------#
        Summary, Enabled = cmds.ReadEnableEdgeBlending()
        Status &= Summary.Successful
        if not Enabled:
            Status &=cmds.WriteEnableEdgeBlending(True).Successful
        if (Status != True):
            return False

        #------------- Apply the map -------------#
        Status &= cmds.WriteApplyBlendMap(True).Successful
        if (Status != True):
            return False

    # Done
    return Status

def WriteBlendMapLUTs_Control_Points_SA(BlendMap: map_gen.BlendMap_c) -> bool:
    """
    Description: takes a BlendMap object, computes the control point's LUT data, writes it to a connected 7540
    system via command and applies the changes in HW.
    Requires a 7540 system connected to the host PC via USB.

    Input arguments:
    BlendMap : a BlendMap object (blending map data)

    Output arguments:
    Status : pass/fail
    """
    #-------------  Blend LUTs object -------------#
    BlendMapLUT = BlendMapLUT_c('SA Control Points LUT data')

    #------------- Call the base function and apply the map --------------#
    return WriteBlendMapLUTs_Control_Points(BlendMap, BlendMapLUT, True)
    
def WriteBlendMapLUTs_Gain(BlendMap: map_gen.BlendMap_c, BlendMapLUT: BlendMapLUT_c, start_row: int, end_row: int,
                           start_col: int, end_col: int, ApplyMap: bool) -> bool:
    """
    Description: takes a BlendMap object, a BlendMapLUT object, writes the GAIN LUT to a connected 7540
    system via command and applies the changes in HW (optional).
    Requires a 7540 system connected to the host PC via USB.
    Supports partial BlendMap LUT creation for speed purposes (only certain sectors of the BlendMap LUTs are
    updated)

    Input arguments:
    BlendMap    : a BlendMap object (containing blending map data)
    BlendMapLUT : a BlendMapLUT object (containing blending LUT data)
    start_row   : control point range starting row index
    end_row     : control point range ending row index (inclusive)
    start_col   : control point range starting column index
    end_col     : control point range ending column index (inclusive)
    ApplyMap    : True = immediately apply blending LUT data in HW

    Output arguments:
    Status : pass/fail
    """

    #------------- Constants -------------#
    map_gen.A_H, map_gen.L_V, L_H, NormOffset = map_gen.GetBlendMapConstants()

    #------------- Assert the requested index range-------------#
    if ((start_row < 0) or (start_row > end_row) or (end_row >= map_gen.L_V)):
        print('ERROR: requested row range is invalid!')
        return False
    if ((start_col < 0) or (start_col > end_col) or (end_col >= map_gen.A_H)):
        print('ERROR: requested column index is out of range!')
        return False

    #------------- Command success flag #-------------#
    Status = True

    #------------- Create the LUT data --------------#
    Status = BlendMapLUT.GenLUTs_GainAndOffset(BlendMap, start_row, end_row, start_col, end_col)
    if (True != Status):
        return False

    #------------- Write the LUTs data -------------#
    for row in range(start_row, end_row + 1, 1):
        # Starting LUT index
        LUTIndex = map_gen.A_H*row + start_col
        ValsR = []
        ValsG = []
        ValsB = []

        # Populate the row
        for col in range(start_col, end_col + 1, 1):
            ValsR.append(int(BlendMapLUT.GainRED[row][col]))
            ValsG.append(int(BlendMapLUT.GainGRN[row][col]))
            ValsB.append(int(BlendMapLUT.GainBLU[row][col]))

        # Write it
        Status &= cmds.WriteBlendMapGainValues(False, cmds.DispfmtColorChannelSelectT.Red, 0, LUTIndex, ValsR).Successful
        Status &= cmds.WriteBlendMapGainValues(False, cmds.DispfmtColorChannelSelectT.Green, 0, LUTIndex, ValsG).Successful
        Status &= cmds.WriteBlendMapGainValues(False, cmds.DispfmtColorChannelSelectT.Blue, 0, LUTIndex, ValsB).Successful
        if (Status != True):
            return False

    #------------------ Should the map be applied? -------------------#
    if (True == ApplyMap):
        #------------- Is blending enabled? -------------#
        Summary, Enabled = cmds.ReadEnableEdgeBlending()
        Status &= Summary.Successful
        if not Enabled:
            Status &=cmds.WriteEnableEdgeBlending(True).Successful
        if (Status != True):
            return False

        #------------- Apply the map -------------#
        Status &= cmds.WriteApplyBlendMap(True).Successful
        if (Status != True):
            return False

    # Done
    return Status

def WriteBlendMapLUTs_Gain_SA(BlendMap: map_gen.BlendMap_c, start_row: int, end_row: int, start_col: int, end_col: int) -> bool:
    """
    Description: takes a BlendMap object, computes the GAIN LUT data, writes it to a connected 7540
    system via command and applies the changes in HW (optional).
    Requires a 7540 system connected to the host PC via USB.
    Supports partial BlendMap LUT creation for speed purposes (only certain sectors of the BlendMap LUTs are
    updated)

    Input arguments:
    BlendMap    : a BlendMap object (containing blending map data)
    start_row   : control point range starting row index
    end_row     : control point range ending row index (inclusive)
    start_col   : control point range starting column index
    end_col     : control point range ending column index (inclusive)

    Output arguments:
    Status : pass/fail

    """
    #-------------  Blend LUTs object -------------#
    BlendMapLUT = BlendMapLUT_c('SA Gain LUT data')

    #------------- Call the base function and apply the map --------------#
    return WriteBlendMapLUTs_Gain(BlendMap, BlendMapLUT, start_row, end_row, start_col, end_col, True)

def WriteBlendMapLUTs_Offset(BlendMap: map_gen.BlendMap_c, BlendMapLUT: BlendMapLUT_c,
                             start_row: int, end_row: int, start_col: int, end_col: int, ApplyMap: bool) -> bool:
    """
    Description: takes a BlendMap object, a BlendMapLUT object,  writes the OFFSET to a connected 7540
    system via command and applies the changes in HW (optional).
    Requires a 7540 system connected to the host PC via USB.
    Supports partial BlendMap LUT creation for speed purposes (only certain sectors of the BlendMap LUTs are
    updated)

    Input arguments:
    BlendMap    : a BlendMap object (containing blending map data)
    BlendMapLUT : a BlendMapLUT object (containing blending LUT data)
    start_row   : control point range starting row index
    end_row     : control point range ending row index (inclusive)
    start_col   : control point range starting column index
    end_col     : control point range ending column index (inclusive)
    ApplyMap    : True = immediately apply blending LUT data in HW

    Output arguments:
    Status : pass/fail
    """
    #------------- Constants -------------#
    map_gen.A_H, map_gen.L_V, L_H, NormOffset = map_gen.GetBlendMapConstants()
    
    #------------- Assert the requested index range-------------#
    if ((start_row < 0) or (start_row > end_row) or (end_row >= map_gen.L_V)):
        print('ERROR: requested row range is invalid!')
        return False
    if ((start_col < 0) or (start_col > end_col) or (end_col >= map_gen.A_H)):
        print('ERROR: requested column index is out of range!')
        return False

    #------------- Command success flag #-------------#
    Status = True

    #------------- Create the LUT data --------------#
    Status = BlendMapLUT.GenLUTs_GainAndOffset(BlendMap, start_row, end_row, start_col, end_col)
    if (True != Status):
        print('failed!')
        return False

    #------------- Write the LUTs data -------------#
    for row in range(start_row, end_row + 1, 1):
        # Starting LUT index
        LUTIndex = map_gen.A_H*row + start_col
        ValsR = []
        ValsG = []
        ValsB = []

        # Populate the row
        for col in range(start_col, end_col + 1, 1):
            ValsR.append(int(BlendMapLUT.OffsetRED[row][col]))
            ValsG.append(int(BlendMapLUT.OffsetGRN[row][col]))
            ValsB.append(int(BlendMapLUT.OffsetBLU[row][col]))

        # Write it
        Status &= cmds.WriteBlendMapOffsetValues(False, cmds.DispfmtColorChannelSelectT.Red, 0, LUTIndex, ValsR).Successful
        Status &= cmds.WriteBlendMapOffsetValues(False, cmds.DispfmtColorChannelSelectT.Green, 0, LUTIndex, ValsG).Successful
        Status &= cmds.WriteBlendMapOffsetValues(False, cmds.DispfmtColorChannelSelectT.Blue, 0, LUTIndex, ValsB).Successful
        if (Status != True):
            return False

    #------------------ Should the map be applied? -------------------#
    if (True == ApplyMap):
        #------------- Is blending enabled? -------------#
        Summary, Enabled = cmds.ReadEnableEdgeBlending()
        Status &= Summary.Successful
        if not Enabled:
            Status &=cmds.WriteEnableEdgeBlending(True).Successful
        if (Status != True):
            return False

        #------------- Apply the map -------------#
        Status &= cmds.WriteApplyBlendMap(True).Successful
        if (Status != True):
            return False

    # Done
    return Status

def WriteBlendMapLUTs_Offset_SA(BlendMap: map_gen.BlendMap_c, start_row: int, end_row: int, start_col: int, end_col: int) -> bool:
    """
    Description: takes a BlendMap object, computes the OFFSET LUT data, writes it to a connected 7540
    system via command and applies the changes in HW (optional).
    Requires a 7540 system connected to the host PC via USB.
    Supports partial BlendMap LUT creation for speed purposes (only certain sectors of the BlendMap LUTs are
    updated)

    Input arguments:
    BlendMap    : a BlendMap object (containing blending map data)
    start_row   : control point range starting row index
    end_row     : control point range ending row index (inclusive)
    start_col   : control point range starting column index
    end_col     : control point range ending column index (inclusive)

    Output arguments:
    Status : pass/fail
    """
    #-------------  Blend LUTs object -------------#
    BlendMapLUT = BlendMapLUT_c('SA Offset LUT data')

    #------------- Call the base function and apply the map --------------#
    return WriteBlendMapLUTs_Offset(BlendMap, BlendMapLUT, start_row, end_row, start_col, end_col, True)

def WriteBlendMapLUTs(BlendMap: map_gen.BlendMap_c) -> bool:
    """
    Description: takes a BlendMap object, computes the ALL LUT data, writes it to a connected 7540
    system via command and applies the changes in HW (optional).
    Requires a 7540 system connected to the host PC via USB.
    Supports partial BlendMap LUT creation for speed purposes (only certain sectors of the BlendMap LUTs are
    updated)

    Input arguments:
    BlendMap    : a BlendMap object (containing blending map data)

    Output arguments:
    Status : pass/fail
    """
    #-------------  Blend LUTs object -------------#
    BlendMapLUT = BlendMapLUT_c('FULL LUT data')

    #------------- Constants -------------#
    map_gen.A_H, map_gen.L_V, L_H, NormOffset = map_gen.GetBlendMapConstants()

    #------------- Control points -------------#
    Status = WriteBlendMapLUTs_Control_Points(BlendMap, BlendMapLUT, False)
    if (True != Status):
        return False

    #------------- Gain points -------------#
    Status = WriteBlendMapLUTs_Gain(BlendMap, BlendMapLUT, 0, map_gen.L_V - 1, 0, map_gen.A_H - 1, False)
    if (True != Status):
        return False

    #------------- Offset points -------------#
    Status = WriteBlendMapLUTs_Offset(BlendMap, BlendMapLUT, 0, map_gen.L_V - 1, 0, map_gen.A_H - 1, False)
    if (True != Status):
        return False

    #------------- Is blending enabled? -------------#
    Summary, Enabled = cmds.ReadEnableEdgeBlending()
    Status &= Summary.Successful
    if not Enabled:
        Status &= cmds.WriteEnableEdgeBlending(True).Successful
    if (Status != True):
        return False

    #------------- Apply the map -------------#
    Status &= cmds.WriteApplyBlendMap(True).Successful
    if (Status != True):
        return False

    # Done
    return Status

#-------------------------------------------- Create a python script for control program  ----------------------------------#
def CreateBlendLUTsScript(BlendMap:map_gen.BlendMap_c, MapFileName: str):
    """
    Description: takes a BlendMap object, computes the BlendMap LUT data, creates a Python script compatible with
    DLP Control Program to load LUT data

    Input arguments:
    BlendMap    : a BlendMap object (containing blending map data)
    MapFileName : desired filename (.py)

    Output arguments:
    Status : pass/fail
    """
    # -------------  Blend LUTs object -------------#
    BlendMapLUT = BlendMapLUT_c('FULL LUT data')

    # ------------- Constants -------------#
    map_gen.A_H, map_gen.L_V, L_H, NormOffset = map_gen.GetBlendMapConstants()

    # ------------- Create the blending map LUT data ------------- #
    BlendMapLUT.GenBlendMapLUTs(BlendMap)

    # ------------- Open the file for writing ------------- #
    file1 = open(MapFileName, "w")

    # -------------- Write the header ---------------- #
    file1.write("from dlpc654x.commands import *\n\n")

    # ------------- Write disable blending ------------- #
    file1.write("# Disable the blending function\n")
    file1.write("Summary=cmds.WriteEnableEdgeBlending(False)\n\n")

    #-------------- Write the Control Points LUTs ---------------- #
    file1.write("# Write Blending Map Control Points\n")

    file1.write("HorizontalControlPoints = Array[UInt16]([ ")
    for col in range(0, map_gen.A_H, 1):
        if (col < map_gen.A_H - 1):
            file1.write("0x{0:x}, ".format(BlendMap.HorzCtrPoints[col]))
        else:
            file1.write("0x{0:x}".format(BlendMap.HorzCtrPoints[col]))
    file1.write(" ])\n")

    file1.write("VerticalControlPoints = Array[UInt16]([ ")
    for row in range(0, map_gen.L_V, 1):
        if (row < map_gen.L_V - 1):
            file1.write("0x{0:x}, ".format(BlendMap.VertCtrPoints[row]))
        else:
            file1.write("0x{0:x}".format(BlendMap.VertCtrPoints[row]))
    file1.write(" ])\n")

    file1.write("Summary = cmds.WriteBlendMapControlPoints({:d}, {:d}, ".format(BlendMap.Pixels, BlendMap.Lines))
    file1.write("HorizontalControlPoints, VerticalControlPoints)\n\n")

    # -------------- Write the GAIN LUTs ---------------- #
    file1.write("# Write GAIN points\n")
    for row in range(0, map_gen.L_V, 1):
        # Starting LUT index
        LUTIndex = map_gen.A_H*row
        file1.write("LUTIndex={:d}\n".format(LUTIndex))

        # Write the arrays
        file1.write("ValsR=[ ")
        for col in range(0, map_gen.A_H, 1):
            if (col < map_gen.A_H - 1):
                file1.write("{:d}, ".format(BlendMapLUT.GainRED[row][col]))
            else:
                file1.write("{:d}".format(BlendMapLUT.GainRED[row][col]))
        file1.write("]\n")

        file1.write("ValsG=[ ")
        for col in range(0, map_gen.A_H, 1):
            if (col < map_gen.A_H - 1):
                file1.write("{:d}, ".format(BlendMapLUT.GainGRN[row][col]))
            else:
                file1.write("{:d}".format(BlendMapLUT.GainGRN[row][col]))
        file1.write("]\n")

        file1.write("ValsB=[ ")
        for col in range(0, map_gen.A_H, 1):
            if (col < map_gen.A_H - 1):
                file1.write("{:d}, ".format(BlendMapLUT.GainBLU[row][col]))
            else:
                file1.write("{:d}".format(BlendMapLUT.GainBLU[row][col]))
        file1.write("]\n")

        file1.write("Summary = cmds.WriteBlendMapGainValues(False, cmds.DispfmtColorChannelSelectT.Red,   0, LUTIndex, ValsR)\n")
        file1.write("Summary = cmds.WriteBlendMapGainValues(False, cmds.DispfmtColorChannelSelectT.Green, 0, LUTIndex, ValsG)\n")
        file1.write("Summary = cmds.WriteBlendMapGainValues(False, cmds.DispfmtColorChannelSelectT.Blue,  0, LUTIndex, ValsB)\n\n")

    # -------------- Write the OFFSET LUTs ---------------- #
    file1.write("# Write OFFSET points\n")
    for row in range(0, map_gen.L_V, 1):
        # Starting LUT index
        LUTIndex = map_gen.A_H * row
        file1.write("LUTIndex={:d}\n".format(LUTIndex))

        # Write the arrays
        file1.write("ValsR=[ ")
        for col in range(0, map_gen.A_H, 1):
            if (col < map_gen.A_H - 1):
                file1.write("{:d}, ".format(BlendMapLUT.OffsetRED[row][col]))
            else:
                file1.write("{:d}".format(BlendMapLUT.OffsetRED[row][col]))
        file1.write("]\n")

        file1.write("ValsG=[ ")
        for col in range(0, map_gen.A_H, 1):
            if (col < map_gen.A_H - 1):
                file1.write("{:d}, ".format(BlendMapLUT.OffsetGRN[row][col]))
            else:
                file1.write("{:d}".format(BlendMapLUT.OffsetGRN[row][col]))
        file1.write("]\n")

        file1.write("ValsB=[ ")
        for col in range(0, map_gen.A_H, 1):
            if (col < map_gen.A_H - 1):
                file1.write("{:d}, ".format(BlendMapLUT.OffsetBLU[row][col]))
            else:
                file1.write("{:d}".format(BlendMapLUT.OffsetBLU[row][col]))
        file1.write("]\n")

        file1.write("Summary = cmds.WriteBlendMapOffsetValues(False, cmds.DispfmtColorChannelSelectT.Red,   0, LUTIndex, ValsR)\n")
        file1.write("Summary = cmds.WriteBlendMapOffsetValues(False, cmds.DispfmtColorChannelSelectT.Green, 0, LUTIndex, ValsG)\n")
        file1.write("Summary = cmds.WriteBlendMapOffsetValues(False, cmds.DispfmtColorChannelSelectT.Blue,  0, LUTIndex, ValsB)\n\n")

    # ------------- Write enable blending ------------- #
    file1.write("# Enable the blending function\n")
    file1.write("Summary=cmds.WriteEnableEdgeBlending(True)\n")
    file1.write("Summary=cmds.WriteApplyBlendMap(True)\n")


    # ------------- Close the file ------------- #
    file1.close()

    # Done
    return True

#-------------------------------------------- Read LUT data from system and generate a blending map blend map --------------------------------------------#
def ReadBlendMapLUTs(BlendMap: map_gen.BlendMap_c) -> Tuple[map_gen.BlendMap_c, bool]:
    """
    Description: reads the current Blend LUT contents from a 7540 system and returns a BlendMap object
    Requires a 7540 system connected to the host PC via USB.

    Input arguments:
    BlendMap    : a BlendMap object (containing blending map data)

    Output arguments:
    BlendMap : a populated BlendMap object
    Status   : pass/fail
    """
     #------------- Constants -------------#
    map_gen.A_H, map_gen.L_V, L_H, NormOffset = map_gen.GetBlendMapConstants()

    #-------------------  Initialize status -------------------#
    Status = True

    #-------------------  Read the control points -------------------#
    print('Reading control points...')
    Summary, HorizontalCtrlPointsLUT, VerticalCtrlPointsLUT = cmds.ReadBlendMapControlPoints()
    Status &= Summary.Successful
    if (True != Status):
        print('failed!')
        return BlendMap, Status

    # Populate the blend map resolution
    BlendMap.Pixels = HorizontalCtrlPointsLUT[map_gen.A_H - 1] + 1
    BlendMap.Lines  = VerticalCtrlPointsLUT[map_gen.L_V - 1] + 1
    BlendMap.HalfPixels = int(np.floor(BlendMap.Pixels/2))

    # Populate the blend map control points
    if (len(HorizontalCtrlPointsLUT) < map_gen.A_H):
        print('failed (Horizontal, wrong LUT size!')
        Status = False
        return BlendMap, Status
    for col in range(0, map_gen.A_H, 1):
        BlendMap.HorzCtrPoints[col] = HorizontalCtrlPointsLUT[col]

    if (len(VerticalCtrlPointsLUT) < map_gen.L_V):
        print('failed (Vertical, wrong LUT size!')
        Status = False
        return BlendMap, Status
    for row in range(0, map_gen.L_V, 1):
        BlendMap.VertCtrPoints[row] = VerticalCtrlPointsLUT[row]

    #-------------------  Read the gain points -------------------#
    print('Reading gain points...')
    for row in range(0, map_gen.L_V, 1):
        # LUT Index
        LUTIndex = row*map_gen.A_H

        # Red
        Summary, IsCompressionEnabled, GainLUT_RED = cmds.ReadBlendMapGainValues(cmds.DispfmtColorChannelSelectT.Red, LUTIndex, map_gen.A_H)
        Status &= Summary.Successful
        if (True != Status):
            print('failed (RED, could not read LUT)!')
            return BlendMap, Status
        if (True == IsCompressionEnabled):
            print('failed (RED, compression is enabled)!')
            return BlendMap, Status
        if (len(GainLUT_RED) != map_gen.A_H):
            print('failed (RED, wrong LUT size)!')
            return BlendMap, Status

        # Green
        Summary, IsCompressionEnabled, GainLUT_GRN = cmds.ReadBlendMapGainValues(cmds.DispfmtColorChannelSelectT.Green,
                                                                                 LUTIndex, map_gen.A_H)
        Status &= Summary.Successful
        if (True != Status):
            print('failed (GRN, could not read LUT)!')
            return BlendMap, Status
        if (True == IsCompressionEnabled):
            print('failed (GRN, compression is enabled)!')
            return BlendMap, Status
        if (len(GainLUT_GRN) != map_gen.A_H):
            print('failed (GRN, wrong LUT size)!')
            return BlendMap, Status
        
        # Blue
        Summary, IsCompressionEnabled, GainLUT_BLU = cmds.ReadBlendMapGainValues(cmds.DispfmtColorChannelSelectT.Blue, LUTIndex, map_gen.A_H)
        Status &= Summary.Successful
        if (True != Status):
            print('failed (BLU, could not read LUT)!')
            return BlendMap, Status
        if (True == IsCompressionEnabled):
            print('failed (BLU, compression is enabled)!')
            return BlendMap, Status
        if (len(GainLUT_BLU) != map_gen.A_H):
            print('failed (BLU, wrong LUT size)!')
            return BlendMap, Status

        # Populate blending map
        for col in range(0, map_gen.A_H, 1):
            BlendMap.GainRED[row][col] = float(GainLUT_RED[col] & 0x1FFF)/float(1 << 12)
            BlendMap.GainGRN[row][col] = float(GainLUT_GRN[col] & 0x1FFF)/float(1 << 12)
            BlendMap.GainBLU[row][col] = float(GainLUT_BLU[col] & 0x1FFF)/float(1 << 12)

    #-------------------  Read the offset points -------------------#
    # Precision is s1m8e4, this means that the supported range is  -8372224 to 8372224
    min_p, max_p, min_n, max_n = fpl.get_range(1, 8, 4)
    MaxVal = max_p
    print('Reading offset points...')
    for row in range(0, map_gen.L_V, 1):
        # LUT Index
        LUTIndex = row*map_gen.A_H

        # Red
        Summary, IsCompressionEnabled, OffsetLUT_RED = cmds.ReadBlendMapOffsetValues(cmds.DispfmtColorChannelSelectT.Red, LUTIndex, map_gen.A_H)
        Status &= Summary.Successful
        if (True != Status):
            print('failed (RED, could not read LUT)!')
            return BlendMap, Status
        if (True == IsCompressionEnabled):
            print('failed (RED, compression is enabled)!')
            return BlendMap, Status
        if (len(OffsetLUT_RED) != map_gen.A_H):
            print('failed (RED, wrong LUT size)!')
            return BlendMap, Status

        # Green
        Summary, IsCompressionEnabled, OffsetLUT_GRN = cmds.ReadBlendMapOffsetValues(cmds.DispfmtColorChannelSelectT.Green, LUTIndex, map_gen.A_H)
        Status &= Summary.Successful
        if (True != Status):
            print('failed (GRN, could not read LUT)!')
            return BlendMap, Status
        if (True == IsCompressionEnabled):
            print('failed (GRN, compression is enabled)!')
            return BlendMap, Status
        if (len(OffsetLUT_GRN) != map_gen.A_H):
            print('failed (GRN, wrong LUT size)!')
            return BlendMap, Status
        
        # Blue
        Summary, IsCompressionEnabled, OffsetLUT_BLU = cmds.ReadBlendMapOffsetValues(cmds.DispfmtColorChannelSelectT.Blue, LUTIndex, map_gen.A_H)
        Status &= Summary.Successful
        if (True != Status):
            print('failed (BLU, could not read LUT)!')
            return BlendMap, Status
        if (True == IsCompressionEnabled):
            print('failed (BLU, compression is enabled)!')
            return BlendMap, Status
        if (len(OffsetLUT_BLU) != map_gen.A_H):
            print('failed (BLU, wrong LUT size)!')
            return BlendMap, Status

        # Populate blending map
        for col in range(0, map_gen.A_H, 1):
            BlendMap.OffsetRED[row][col] = NormOffset*fpl.float_to_fixed(int(GainLUT_RED[col] & 0x1FFF), 1, 8, 4)/float(MaxVal)
            BlendMap.OffsetGRN[row][col] = NormOffset*fpl.float_to_fixed(int(GainLUT_GRN[col] & 0x1FFF), 1, 8, 4)/float(MaxVal)
            BlendMap.OffsetBLU[row][col] = NormOffset*fpl.float_to_fixed(int(GainLUT_BLU[col] & 0x1FFF), 1, 8, 4)/float(MaxVal)

    # Done
    return BlendMap, Status
