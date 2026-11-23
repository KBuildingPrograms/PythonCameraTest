import sys
import clr

if __name__ == '__main__' or __name__ == 'commands' or __name__ == 'blending_utils.libs.dlpc754x.commands':
    # Add dlls folder to path
    from pathlib import Path
    import os

    # Trim the path sequentially
    dll_path = str(Path(__file__).parent)
    pos = str(dll_path).rfind('\\')
    dll_path = str(dll_path)[0:pos]
    pos = str(dll_path).rfind('\\')
    dll_path = str(dll_path)[0:pos] + '\\dlls'

    # Search in the current system path
    Found = False
    for i in range(0, len(sys.path), 1):
        if (dll_path == sys.path[i]):
            Found = True
            break

    # If we have not found it, append it
    if (False == Found):
        print("Adding " + dll_path + " to system path...")
        sys.path.append(os.path.normpath(dll_path))


# Module metadata
__copyright__ = "(c) Copyright, Texas Instruments Incorporated, 2023-2024\nAll Rights Reserved."
__author__ = "Texas Instruments DLP"
__status__ = "TI Reference code\nCustomers/users own production SW."
__doc__ = "DESCRIPTION: DLPC754x commands library (DO NOT MODIFY THIS FILE!)"

clr.AddReference('DLPComposer.Commands.DLPC754x')
from System import *
from DLPComposer.Commands.DLPC754x import * 

def ReadMode() :
    Summary, AppMode, ControllerConfig = \
        Command.ReadMode(CmdModeT.Bootloader, CmdControllerConfigT.Single)
    return Summary, AppMode, ControllerConfig

def ReadVersion() :
    Summary, VersionObj = \
        Command.ReadVersion(Version())
    return Summary, VersionObj

def WriteSwitchMode(SwitchMode) :
    return Command.WriteSwitchMode(SwitchMode)

def ReadBootHoldReason() :
    Summary, ReasonCode = \
        Command.ReadBootHoldReason(0)
    return Summary, int(ReasonCode)

def ReadFlashInfo(ChipSelect) :
    Summary, ManfId, DevId, DevSize, SectorInfo, AvailableForProgramming = \
        Command.ReadFlashInfo(ChipSelect, 0, 0, 0, [], False)
    return Summary, int(ManfId), int(DevId), int(DevSize), list(SectorInfo), bool(AvailableForProgramming)

def ReadGetProgrammableFlashSectorInformation() :
    Summary, SectorInfo = \
        Command.ReadGetProgrammableFlashSectorInformation([])
    return Summary, list(SectorInfo)

def WriteUnlockFlashForUpdate(Unlock) :
    return Command.WriteUnlockFlashForUpdate(Unlock)

def ReadUnlockFlashForUpdate() :
    Summary, IsUnlocked = \
        Command.ReadUnlockFlashForUpdate(0)
    return Summary, int(IsUnlocked)

def WriteEraseSector(SectorAddress) :
    return Command.WriteEraseSector(SectorAddress)

def WriteInitializeFlashReadWriteSettings(StartAddress, NumBytes) :
    return Command.WriteInitializeFlashReadWriteSettings(StartAddress, NumBytes)

def WriteFlashWrite(Data) :
    Data = Array[Byte](Data)
    return Command.WriteFlashWrite(Data)

def ReadFlashWrite(NumBytesToRead) :
    Summary, Data = \
        Command.ReadFlashWrite(NumBytesToRead, bytearray())
    return Summary, bytearray(Data)

def ReadChecksum(StartAddress, NumBytes) :
    Summary, SimpleChecksum, SumofSumChecksum = \
        Command.ReadChecksum(StartAddress, NumBytes, 0, 0)
    return Summary, int(SimpleChecksum), int(SumofSumChecksum)

def WriteResetFlash(ChipSelect) :
    return Command.WriteResetFlash(ChipSelect)

def WriteMemory(Address, Value) :
    return Command.WriteMemory(Address, Value)

def ReadMemory(Address) :
    Summary, Value = \
        Command.ReadMemory(Address, 0)
    return Summary, int(Value)

def WriteMemoryArray(MemoryArrayObj) :
    return Command.WriteMemoryArray(MemoryArrayObj)

def ReadMemoryArray(StartAddress, AddressIncrement, AccessWidth, NumberOfWords, NumberOfBytesPerWord) :
    Summary, Data = \
        Command.ReadMemoryArray(StartAddress, AddressIncrement, AccessWidth, NumberOfWords, NumberOfBytesPerWord, bytearray())
    return Summary, bytearray(Data)

def WriteAnrSpatialFilterStatus(IsNoiseFilterEnabled, FilterStrength) :
    return Command.WriteAnrSpatialFilterStatus(IsNoiseFilterEnabled, FilterStrength)

def ReadAnrSpatialFilterStatus() :
    Summary, IsNoiseFilterEnabled, FilterStrength = \
        Command.ReadAnrSpatialFilterStatus(False, AnrFilterStrengthT.AnrStrength1)
    return Summary, bool(IsNoiseFilterEnabled), FilterStrength

def WriteAnrTemporalFilterStatus(IsNoiseFilterEnabled, FilterStrength) :
    return Command.WriteAnrTemporalFilterStatus(IsNoiseFilterEnabled, FilterStrength)

def ReadAnrTemporalFilterStatus() :
    Summary, IsNoiseFilterEnabled, FilterStrength = \
        Command.ReadAnrTemporalFilterStatus(False, AnrFilterStrengthT.AnrStrength1)
    return Summary, bool(IsNoiseFilterEnabled), FilterStrength

def ReadAnrNoiseFloorEstimate() :
    Summary, NoiseFloor = \
        Command.ReadAnrNoiseFloorEstimate(0)
    return Summary, int(NoiseFloor)

def WriteEnableDeiForProgNoiseReduction(Enable) :
    return Command.WriteEnableDeiForProgNoiseReduction(Enable)

def ReadEnableDeiForProgNoiseReduction() :
    Summary, Enable = \
        Command.ReadEnableDeiForProgNoiseReduction(False)
    return Summary, bool(Enable)

def WriteCalibrateAdc() :
    return Command.WriteCalibrateAdc()

def WriteSourceConnector(ConnectorNum) :
    return Command.WriteSourceConnector(ConnectorNum)

def ReadSourceConnector() :
    Summary, Source = \
        Command.ReadSourceConnector(0)
    return Summary, int(Source)

def WriteAutoSourceSelect(AutoSelectEnable) :
    return Command.WriteAutoSourceSelect(AutoSelectEnable)

def ReadAutoSourceSelect() :
    Summary, AutoSelectEnable = \
        Command.ReadAutoSourceSelect(False)
    return Summary, bool(AutoSelectEnable)

def ReadAutolockStatus() :
    Summary, AutolockStatusObj = \
        Command.ReadAutolockStatus(AutolockStatus())
    return Summary, AutolockStatusObj

def WriteAutoLockAsmCfg(AutoLockAsmCfgObj) :
    return Command.WriteAutoLockAsmCfg(AutoLockAsmCfgObj)

def ReadAutoLockAsmCfg() :
    Summary, AutoLockAsmCfgObj = \
        Command.ReadAutoLockAsmCfg(AutoLockAsmCfg())
    return Summary, AutoLockAsmCfgObj

def WritePhase(Phase) :
    return Command.WritePhase(Phase)

def ReadPhase() :
    Summary, Phase = \
        Command.ReadPhase(0)
    return Summary, int(Phase)

def ReadVerticalFramingRegionLimits() :
    Summary, LowerLimit, UpperLimit = \
        Command.ReadVerticalFramingRegionLimits(0, 0)
    return Summary, int(LowerLimit), int(UpperLimit)

def WriteGain(RedGain, GreenGain, BlueGain) :
    return Command.WriteGain(RedGain, GreenGain, BlueGain)

def ReadGain() :
    Summary, RedGain, GreenGain, BlueGain = \
        Command.ReadGain(0, 0, 0)
    return Summary, int(RedGain), int(GreenGain), int(BlueGain)

def WriteOffset(Red, Green, Blue) :
    return Command.WriteOffset(Red, Green, Blue)

def ReadOffset() :
    Summary, Red, Green, Blue = \
        Command.ReadOffset(0, 0, 0)
    return Summary, int(Red), int(Green), int(Blue)

def WriteLevelWindow(Left, Right, Top, Bottom) :
    return Command.WriteLevelWindow(Left, Right, Top, Bottom)

def ReadLevelWindow() :
    Summary, Left, Right, Top, Bottom = \
        Command.ReadLevelWindow(0, 0, 0, 0)
    return Summary, int(Left), int(Right), int(Top), int(Bottom)

def ReadRgbLevel() :
    Summary, RgbLevelObj = \
        Command.ReadRgbLevel(RgbLevel())
    return Summary, RgbLevelObj

def WriteBt656Reg(DevAddress, RegAddress, Value) :
    return Command.WriteBt656Reg(DevAddress, RegAddress, Value)

def ReadBt656Reg(DevAddress, RegAddress) :
    Summary, Value = \
        Command.ReadBt656Reg(DevAddress, RegAddress, 0)
    return Summary, int(Value)

def WriteEnableBt656Gpio(Enable) :
    return Command.WriteEnableBt656Gpio(Enable)

def WriteFilmMode(Mode) :
    return Command.WriteFilmMode(Mode)

def ReadFilmMode() :
    Summary, Mode = \
        Command.ReadFilmMode(DeiFilmModesT.ModeDisable)
    return Summary, Mode

def WriteFilmModeLockThresholds(BeforeLock, BeforeUnlock) :
    return Command.WriteFilmModeLockThresholds(BeforeLock, BeforeUnlock)

def ReadFilmModeLockThresholds() :
    Summary, BeforeLock, BeforeUnlock = \
        Command.ReadFilmModeLockThresholds(0, 0)
    return Summary, int(BeforeLock), int(BeforeUnlock)

def ReadDeiStatus() :
    Summary, FilmLockRegion0, FilmLockRegion1 = \
        Command.ReadDeiStatus(False, False)
    return Summary, bool(FilmLockRegion0), bool(FilmLockRegion1)

def WriteDeiEnable(DeiEnable) :
    return Command.WriteDeiEnable(DeiEnable)

def ReadDeiEnable() :
    Summary, DeiEnable = \
        Command.ReadDeiEnable(False)
    return Summary, bool(DeiEnable)

def ReadIntraFieldInterpolationStrength() :
    Summary, Strength = \
        Command.ReadIntraFieldInterpolationStrength(DeiInterpolationStrengthT.Optimized0)
    return Summary, Strength

def WriteMotionAdaptiveMode(Mode) :
    return Command.WriteMotionAdaptiveMode(Mode)

def ReadMotionAdaptiveMode() :
    Summary, Mode = \
        Command.ReadMotionAdaptiveMode(DeiModeT.MotionAdaptive)
    return Summary, Mode

def WriteFilmRegionEnable(Enable) :
    return Command.WriteFilmRegionEnable(Enable)

def ReadFilmRegionEnable() :
    Summary, Enable = \
        Command.ReadFilmRegionEnable(False)
    return Summary, bool(Enable)

def WriteFilmRegion1Area(FirstPixel, FirstLine, PixelsPerLine, LinesPerFrame) :
    return Command.WriteFilmRegion1Area(FirstPixel, FirstLine, PixelsPerLine, LinesPerFrame)

def ReadFilmRegion1Area() :
    Summary, FirstPixel, FirstLine, PixelsPerLine, LinesPerFrame = \
        Command.ReadFilmRegion1Area(0, 0, 0, 0)
    return Summary, int(FirstPixel), int(FirstLine), int(PixelsPerLine), int(LinesPerFrame)

def WriteUserInterpolationStrengthEnable(UserInterpolationStrengthEnableObj) :
    return Command.WriteUserInterpolationStrengthEnable(UserInterpolationStrengthEnableObj)

def ReadUserInterpolationStrengthEnable() :
    Summary, UserInterpolationStrengthEnableObj = \
        Command.ReadUserInterpolationStrengthEnable(UserInterpolationStrengthEnable())
    return Summary, UserInterpolationStrengthEnableObj

def WriteMotionDetectionInChroma(DetectInChroma) :
    return Command.WriteMotionDetectionInChroma(DetectInChroma)

def ReadMotionDetectionInChroma() :
    Summary, DetectInChroma = \
        Command.ReadMotionDetectionInChroma(False)
    return Summary, bool(DetectInChroma)

def WriteRateFactorUpdate(Enable) :
    return Command.WriteRateFactorUpdate(Enable)

def WriteSysTestMode(Enable) :
    return Command.WriteSysTestMode(Enable)

def ReadSysTestMode() :
    Summary, Enable = \
        Command.ReadSysTestMode(False)
    return Summary, bool(Enable)

def ReadTaskStatus(TaskId) :
    Summary, Priority, StackSize, StackUnused, StackUsed = \
        Command.ReadTaskStatus(TaskId, 0, 0, 0, 0)
    return Summary, int(Priority), int(StackSize), int(StackUnused), int(StackUsed)

def ReadMaxIntDisableTime() :
    Summary, MaxIntDisableTime = \
        Command.ReadMaxIntDisableTime(0)
    return Summary, int(MaxIntDisableTime)

def WriteResetMaxIntDisableTime() :
    return Command.WriteResetMaxIntDisableTime()

def ReadTaskTimeProfile(TaskName) :
    Summary, MaxExecutionTime, MinExecutionTime = \
        Command.ReadTaskTimeProfile(TaskName, 0, 0)
    return Summary, int(MaxExecutionTime), int(MinExecutionTime)

def WriteResetTaskTimeProfile(TaskName) :
    return Command.WriteResetTaskTimeProfile(TaskName)

def WriteToggleUsbMode() :
    return Command.WriteToggleUsbMode()

def WriteSendUsbMouseCode(MouseClick, MouseX, MouseY) :
    return Command.WriteSendUsbMouseCode(MouseClick, MouseX, MouseY)

def WriteSendUsbKeyboardCode(KeyCode) :
    return Command.WriteSendUsbKeyboardCode(KeyCode)

def WriteLmpEnable(Enable) :
    return Command.WriteLmpEnable(Enable)

def ReadIsLampLit() :
    Summary, Enable = \
        Command.ReadIsLampLit(False)
    return Summary, bool(Enable)

def WriteGpioPins(GpioPinsObj) :
    return Command.WriteGpioPins(GpioPinsObj)

def ReadGpioPins(MaskBits1, MaskBits2, MaskBits3) :
    Summary, LogicValue1, LogicValue2, LogicValue3 = \
        Command.ReadGpioPins(MaskBits1, MaskBits2, MaskBits3, 0, 0, 0)
    return Summary, int(LogicValue1), int(LogicValue2), int(LogicValue3)

def WriteGpioInterruptSource(InterruptSource, Pin) :
    return Command.WriteGpioInterruptSource(InterruptSource, Pin)

def ReadGpioInterruptSource(InterruptSource) :
    Summary, Pin = \
        Command.ReadGpioInterruptSource(InterruptSource, GpioPinsT.Pin0)
    return Summary, Pin

def ReadGpioEnable(Pin) :
    Summary, Enable, AlternateFuncSelect = \
        Command.ReadGpioEnable(Pin, False, False)
    return Summary, bool(Enable), bool(AlternateFuncSelect)

def WriteGpioEnableAlternateFunction(Function, AlternateFunctionEnable) :
    return Command.WriteGpioEnableAlternateFunction(Function, AlternateFunctionEnable)

def WriteGpioInterruptConfig(InterruptSource, TriggerType, TriggerPolarity) :
    return Command.WriteGpioInterruptConfig(InterruptSource, TriggerType, TriggerPolarity)

def ReadGpioInterruptConfig(InterruptSource) :
    Summary, TriggerType, TriggerPolarity = \
        Command.ReadGpioInterruptConfig(InterruptSource, GpioTriggerT.Level, GpioPolarityT.ActiveHi)
    return Summary, TriggerType, TriggerPolarity

def ReadGpioInterruptStatus(InterruptSource) :
    Summary, InterruptActive = \
        Command.ReadGpioInterruptStatus(InterruptSource, False)
    return Summary, bool(InterruptActive)

def ReadGpioPinName(PinNum) :
    Summary, PinName = \
        Command.ReadGpioPinName(PinNum, bytearray())
    return Summary, bytearray(PinName)

def WriteEnableScaleRingMinimization(Enable) :
    return Command.WriteEnableScaleRingMinimization(Enable)

def ReadEnableScaleRingMinimization() :
    Summary, Enable = \
        Command.ReadEnableScaleRingMinimization(False)
    return Summary, bool(Enable)

def WriteScalingFilter(Filter) :
    return Command.WriteScalingFilter(Filter)

def ReadScalingFilter() :
    Summary, Filter = \
        Command.ReadScalingFilter(DispScalingFilterT.Video)
    return Summary, Filter

def WriteEnableKeystone(Enabled) :
    return Command.WriteEnableKeystone(Enabled)

def ReadEnableKeystone() :
    Summary, Enabled = \
        Command.ReadEnableKeystone(False)
    return Summary, bool(Enabled)

def WriteHdrMode(HdrMode) :
    return Command.WriteHdrMode(HdrMode)

def ReadHdrMode() :
    Summary, HdrMode = \
        Command.ReadHdrMode(DpHdrMode.Auto)
    return Summary, HdrMode

def WriteImageCphw(ImageCphwObj) :
    return Command.WriteImageCphw(ImageCphwObj)

def ReadImageCphw() :
    Summary, ImageCphwObj = \
        Command.ReadImageCphw(ImageCphw())
    return Summary, ImageCphwObj

def WriteImageCpeep(Profile, ImageCpeepObj) :
    return Command.WriteImageCpeep(Profile, ImageCpeepObj)

def ReadImageCpeep(Profile) :
    Summary, ImageCpeepObj = \
        Command.ReadImageCpeep(Profile, ImageCpeep())
    return Summary, ImageCpeepObj

def WriteImageCtIup(HdSourceEnable) :
    return Command.WriteImageCtIup(HdSourceEnable)

def ReadImageCtIup() :
    Summary, HdSourceEnable = \
        Command.ReadImageCtIup(False)
    return Summary, bool(HdSourceEnable)

def WriteImageCtiGain(Gain) :
    return Command.WriteImageCtiGain(Gain)

def ReadImageCtiGain() :
    Summary, Gain = \
        Command.ReadImageCtiGain(ImgCtiGainT.ImgCtiGain1)
    return Summary, Gain

def ReadImageInverseHsg() :
    Summary, ImageInverseHsgObj = \
        Command.ReadImageInverseHsg(ImageInverseHsg())
    return Summary, ImageInverseHsgObj

def ReadLibSignature(LibName) :
    Summary, LibSignature, ChangesetSignature = \
        Command.ReadLibSignature(LibName, bytearray(), bytearray())
    return Summary, bytearray(LibSignature), bytearray(ChangesetSignature)

def WritePrintAllLibSignatures() :
    return Command.WritePrintAllLibSignatures()

def ReadOsdDisplayStatus() :
    Summary, OsdDisplayed = \
        Command.ReadOsdDisplayStatus(False)
    return Summary, bool(OsdDisplayed)

def WriteNavigateosd(Key) :
    return Command.WriteNavigateosd(Key)

def WriteOsdUpdateMode(UpdateMode) :
    return Command.WriteOsdUpdateMode(UpdateMode)

def ReadOsdUpdateMode() :
    Summary, UpdateMode = \
        Command.ReadOsdUpdateMode(OsdUpdateModesT.Blanking)
    return Summary, UpdateMode

def WriteEnableOsd(Enable) :
    return Command.WriteEnableOsd(Enable)

def WriteEnableWindow(WindowNumber, Enable) :
    return Command.WriteEnableWindow(WindowNumber, Enable)

def WriteGenerateWindow(WindowNumber, Left, Top, Height, Width) :
    return Command.WriteGenerateWindow(WindowNumber, Left, Top, Height, Width)

def WriteSspPassthru(SspPassthruObj) :
    return Command.WriteSspPassthru(SspPassthruObj)

def ReadSspPassthru(Port, ChipSelect, DeviceType, ClockRate, Command) :
    Summary, Data = \
        Command.ReadSspPassthru(Port, ChipSelect, DeviceType, ClockRate, Command, 0)
    return Summary, int(Data)

def WriteComposerPassthruData(Cmd, InpNumBytes, InputData) :
    InputData = Array[Byte](InputData)
    return Command.WriteComposerPassthruData(Cmd, InpNumBytes, InputData)

def ReadComposerPassthruData(Cmd, InpNumBytes, OutNumBytes, InputData) :
    Summary, OutputData = \
        Command.ReadComposerPassthruData(Cmd, InpNumBytes, OutNumBytes, InputData, bytearray())
    return Summary, bytearray(OutputData)

def WriteSetSubframeMask(SubframeNumber, SubframePattern) :
    return Command.WriteSetSubframeMask(SubframeNumber, SubframePattern)

def WriteEnableSubframeOverride(Enable, Subframe) :
    return Command.WriteEnableSubframeOverride(Enable, Subframe)

def WriteEnableBnmUpdate(Enable) :
    return Command.WriteEnableBnmUpdate(Enable)

def ReadEnableBnmUpdate() :
    Summary, Enable = \
        Command.ReadEnableBnmUpdate(False)
    return Summary, bool(Enable)

def ReadGetSequenceNumber() :
    Summary, Current = \
        Command.ReadGetSequenceNumber(0)
    return Summary, int(Current)

def WriteSetXpr25AdjustmentFactor(Adjustment) :
    return Command.WriteSetXpr25AdjustmentFactor(Adjustment)

def ReadSetXpr25AdjustmentFactor() :
    Summary, Adjustment = \
        Command.ReadSetXpr25AdjustmentFactor(0)
    return Summary, int(Adjustment)

def ReadSfgResolution() :
    Summary, HorizontalResolution, VerticalResolution = \
        Command.ReadSfgResolution(0, 0)
    return Summary, int(HorizontalResolution), int(VerticalResolution)

def WriteActivePortConfiguration(Port, PortWidth, AbcMux, IsClockPolarityPositive) :
    return Command.WriteActivePortConfiguration(Port, PortWidth, AbcMux, IsClockPolarityPositive)

def ReadActivePortConfiguration() :
    Summary, Port, PortWidth, AbcMux, IsClockPolarityPositive = \
        Command.ReadActivePortConfiguration(SrcPortT.Vbo, SrcPortWidthT.Src30Bits, SrcAbcMuxT.StraightThru, False)
    return Summary, Port, PortWidth, AbcMux, bool(IsClockPolarityPositive)

def WriteSplashFrameRate(FrameRate) :
    return Command.WriteSplashFrameRate(FrameRate)

def ReadSplashFrameRate() :
    Summary, FrameRate = \
        Command.ReadSplashFrameRate(0)
    return Summary, float(FrameRate)

def ReadCaptureExternalFrame() :
    Summary, CaptureExternalFrameObj = \
        Command.ReadCaptureExternalFrame(CaptureExternalFrame())
    return Summary, CaptureExternalFrameObj

def ReadCapturedFrameWithComp() :
    Summary, FrameData = \
        Command.ReadCapturedFrameWithComp(bytearray())
    return Summary, bytearray(FrameData)

def ReadSplashCaptureTime() :
    Summary, CaptureTime = \
        Command.ReadSplashCaptureTime(0)
    return Summary, int(CaptureTime)

def WriteEnableStructuredPatterns(Enable) :
    return Command.WriteEnableStructuredPatterns(Enable)

def ReadEnableStructuredPatterns() :
    Summary, Enable = \
        Command.ReadEnableStructuredPatterns(False)
    return Summary, bool(Enable)

def WriteInvertStructuredPatternBitplane(BitPlaneNum, Invert) :
    return Command.WriteInvertStructuredPatternBitplane(BitPlaneNum, Invert)

def ReadInvertStructuredPatternBitplane(BitPlaneNum) :
    Summary, Invert = \
        Command.ReadInvertStructuredPatternBitplane(BitPlaneNum, False)
    return Summary, bool(Invert)

def WriteSetStructuredPatternBitplane(BitPlaneNum, IsVerticalPattern, NumOfBytes, Bytes) :
    Bytes = Array[Byte](Bytes)
    return Command.WriteSetStructuredPatternBitplane(BitPlaneNum, IsVerticalPattern, NumOfBytes, Bytes)

def WriteSetStructuredPatternStripes(SetStructuredPatternStripesObj) :
    return Command.WriteSetStructuredPatternStripes(SetStructuredPatternStripesObj)

def ReadTpgPatternType() :
    Summary, PatternType = \
        Command.ReadTpgPatternType(TpgPatternT.SolidField)
    return Summary, PatternType

def WriteTpgPredefinedPattern(PatternNumber) :
    return Command.WriteTpgPredefinedPattern(PatternNumber)

def ReadTpgPredefinedPattern() :
    Summary, PatternNumber = \
        Command.ReadTpgPredefinedPattern(0)
    return Summary, int(PatternNumber)

def ReadTpgPixelClkFreq() :
    Summary, PixelClockFrequency = \
        Command.ReadTpgPixelClkFreq(0)
    return Summary, int(PixelClockFrequency)

def WriteTpgSolidField(SolidColorRed, SolidColorGreen, SolidColorBlue) :
    return Command.WriteTpgSolidField(SolidColorRed, SolidColorGreen, SolidColorBlue)

def ReadTpgSolidField() :
    Summary, SolidColorRed, SolidColorGreen, SolidColorBlue = \
        Command.ReadTpgSolidField(0, 0, 0)
    return Summary, int(SolidColorRed), int(SolidColorGreen), int(SolidColorBlue)

def WriteTpgRampHorizontal(RampStep, RampColor) :
    return Command.WriteTpgRampHorizontal(RampStep, RampColor)

def ReadTpgRampHorizontal() :
    Summary, RampStep, RampColor = \
        Command.ReadTpgRampHorizontal(TpgHorzRampStepT.TpgHorzrampStep0P5, TpgColorT.Black)
    return Summary, RampStep, RampColor

def WriteTpgRampVertical(RampStep, RampColor) :
    return Command.WriteTpgRampVertical(RampStep, RampColor)

def ReadTpgRampVertical() :
    Summary, RampStep, RampColor = \
        Command.ReadTpgRampVertical(TpgVertRampStepT.TpgVertrampStep1P0, TpgColorT.Black)
    return Summary, RampStep, RampColor

def WriteTpgHorizontalLines(TpgHorizontalLinesObj) :
    return Command.WriteTpgHorizontalLines(TpgHorizontalLinesObj)

def ReadTpgHorizontalLines() :
    Summary, TpgHorizontalLinesObj = \
        Command.ReadTpgHorizontalLines(TpgHorizontalLines())
    return Summary, TpgHorizontalLinesObj

def WriteTpgVerticalLines(TpgVerticalLinesObj) :
    return Command.WriteTpgVerticalLines(TpgVerticalLinesObj)

def ReadTpgVerticalLines() :
    Summary, TpgVerticalLinesObj = \
        Command.ReadTpgVerticalLines(TpgVerticalLines())
    return Summary, TpgVerticalLinesObj

def WriteTpgDiagonalLines(TpgDiagonalLinesObj) :
    return Command.WriteTpgDiagonalLines(TpgDiagonalLinesObj)

def ReadTpgDiagonalLines() :
    Summary, TpgDiagonalLinesObj = \
        Command.ReadTpgDiagonalLines(TpgDiagonalLines())
    return Summary, TpgDiagonalLinesObj

def WriteTpgGridLines(TpgGridLinesObj) :
    return Command.WriteTpgGridLines(TpgGridLinesObj)

def ReadTpgGridLines() :
    Summary, TpgGridLinesObj = \
        Command.ReadTpgGridLines(TpgGridLines())
    return Summary, TpgGridLinesObj

def WriteTpgColorBars(Width, ColorEnableRed, ColorEnableGreen, ColorEnableBlue) :
    return Command.WriteTpgColorBars(Width, ColorEnableRed, ColorEnableGreen, ColorEnableBlue)

def ReadTpgColorBars() :
    Summary, Width, ColorEnableRed, ColorEnableGreen, ColorEnableBlue = \
        Command.ReadTpgColorBars(0, False, False, False)
    return Summary, int(Width), bool(ColorEnableRed), bool(ColorEnableGreen), bool(ColorEnableBlue)

def WriteTpgColorHorzRamp(RampStep, Height, ColorEnableRed, ColorEnableGreen, ColorEnableBlue) :
    return Command.WriteTpgColorHorzRamp(RampStep, Height, ColorEnableRed, ColorEnableGreen, ColorEnableBlue)

def ReadTpgColorHorzRamp() :
    Summary, RampStep, Height, ColorEnableRed, ColorEnableGreen, ColorEnableBlue = \
        Command.ReadTpgColorHorzRamp(TpgHorzRampStepT.TpgHorzrampStep0P5, 0, False, False, False)
    return Summary, RampStep, int(Height), bool(ColorEnableRed), bool(ColorEnableGreen), bool(ColorEnableBlue)

def WriteTpgFixedRamp(TpgFixedRampObj) :
    return Command.WriteTpgFixedRamp(TpgFixedRampObj)

def ReadTpgFixedRamp() :
    Summary, TpgFixedRampObj = \
        Command.ReadTpgFixedRamp(TpgFixedRamp())
    return Summary, TpgFixedRampObj

def WriteTpgDiamondDiagLines(TpgDiamondDiagLinesObj) :
    return Command.WriteTpgDiamondDiagLines(TpgDiamondDiagLinesObj)

def ReadTpgDiamondDiagLines() :
    Summary, TpgDiamondDiagLinesObj = \
        Command.ReadTpgDiamondDiagLines(TpgDiamondDiagLines())
    return Summary, TpgDiamondDiagLinesObj

def WriteTpgInterlacedEnable(InterlaceEnable) :
    return Command.WriteTpgInterlacedEnable(InterlaceEnable)

def ReadTpgInterlacedEnable() :
    Summary, InterlaceEnable = \
        Command.ReadTpgInterlacedEnable(False)
    return Summary, bool(InterlaceEnable)

def WriteTpgCheckerboard(TpgCheckerboardObj) :
    return Command.WriteTpgCheckerboard(TpgCheckerboardObj)

def ReadTpgCheckerboard() :
    Summary, TpgCheckerboardObj = \
        Command.ReadTpgCheckerboard(TpgCheckerboard())
    return Summary, TpgCheckerboardObj

def WriteEnableThreeD(Enable3D) :
    return Command.WriteEnableThreeD(Enable3D)

def ReadEnableThreeD() :
    Summary, Enable3D = \
        Command.ReadEnableThreeD(False)
    return Summary, bool(Enable3D)

def WriteThreeDSourceConfiguration(ThreeDSourceConfigurationObj) :
    return Command.WriteThreeDSourceConfiguration(ThreeDSourceConfigurationObj)

def ReadThreeDSourceConfiguration() :
    Summary, ThreeDSourceConfigurationObj = \
        Command.ReadThreeDSourceConfiguration(ThreeDSourceConfiguration())
    return Summary, ThreeDSourceConfigurationObj

def WriteLeftRightSignalPolarity(Invert) :
    return Command.WriteLeftRightSignalPolarity(Invert)

def ReadLeftRightSignalPolarity() :
    Summary, Invert = \
        Command.ReadLeftRightSignalPolarity(False)
    return Summary, bool(Invert)

def ReadControllerInfo() :
    Summary, ControllerId, ControllerName = \
        Command.ReadControllerInfo(0, '')
    return Summary, int(ControllerId), list(ControllerName)

def ReadDmdInfo() :
    Summary, DmdId, FuseId, FuseBitString, DmdName = \
        Command.ReadDmdInfo(0, 0, '', '')
    return Summary, int(DmdId), int(FuseId), list(FuseBitString), list(DmdName)

def ReadDmdResolution() :
    Summary, Width, Height = \
        Command.ReadDmdResolution(0, 0)
    return Summary, int(Width), int(Height)

def ReadFlashVersion() :
    Summary, FlashVersionMajor, FlashVersionMinor, FlashVersionSubminor = \
        Command.ReadFlashVersion(0, 0, 0)
    return Summary, int(FlashVersionMajor), int(FlashVersionMinor), int(FlashVersionSubminor)

def ReadFlashLayoutVersion() :
    Summary, FlashConfigLayoutVersion, FlashConfigLayoutHash, ApplicationConfigLayoutVersion, ApplicationConfigLayoutHash = \
        Command.ReadFlashLayoutVersion(0, '', 0, '')
    return Summary, int(FlashConfigLayoutVersion), list(FlashConfigLayoutHash), int(ApplicationConfigLayoutVersion), list(ApplicationConfigLayoutHash)

def ReadProductConfigurationFailureCause() :
    Summary, ProductConfigFailCause = \
        Command.ReadProductConfigurationFailureCause(DdpProductConfigFailCauseT.InvalidController)
    return Summary, ProductConfigFailCause

def ReadSystemStatus() :
    Summary, SystemStatusObj = \
        Command.ReadSystemStatus(SystemStatus())
    return Summary, SystemStatusObj

def ReadEepromDataPresent() :
    Summary, EepromDataPresentObj = \
        Command.ReadEepromDataPresent(EepromDataPresent())
    return Summary, EepromDataPresentObj

def WriteGeneralDelayCommand(DelayInMilliseconds) :
    return Command.WriteGeneralDelayCommand(DelayInMilliseconds)

def WriteEepromInvalidate(EepromInvalidateObj) :
    return Command.WriteEepromInvalidate(EepromInvalidateObj)

def WriteSplashCapture() :
    return Command.WriteSplashCapture()

def ReadSplashCaptureStatus() :
    Summary, CaptureState, CaptureCompletionPercentage = \
        Command.ReadSplashCaptureStatus(SplashCaptureStateT.Terminated, 0)
    return Summary, CaptureState, int(CaptureCompletionPercentage)

def WriteTerminateSplashCapture() :
    return Command.WriteTerminateSplashCapture()

def ReadComposerVersion() :
    Summary, Major, Minor1, Minor2, Patch, BuildHash = \
        Command.ReadComposerVersion(0, 0, 0, 0, '')
    return Summary, int(Major), int(Minor1), int(Minor2), int(Patch), list(BuildHash)

def WriteAutolockControl(AutolockControl) :
    return Command.WriteAutolockControl(AutolockControl)

def WriteBlendMapGainValues(CompressionEnabled, ColorChannelSelect, TotalNumberOfCompressedValues, Index, GainValues) :
    GainValues = Array[UInt16](GainValues)
    return Command.WriteBlendMapGainValues(CompressionEnabled, ColorChannelSelect, TotalNumberOfCompressedValues, Index, GainValues)

def ReadBlendMapGainValues(ColorChannelSelect, Index, NoOfValues) :
    Summary, IsCompressionEnabled, GainValues = \
        Command.ReadBlendMapGainValues(ColorChannelSelect, Index, NoOfValues, 0, [])
    return Summary, int(IsCompressionEnabled), list(GainValues)

def WriteApplyBlendMap(BlendMapUploadEnable) :
    return Command.WriteApplyBlendMap(BlendMapUploadEnable)

def WriteBlendMapOffsetValues(CompressionEnabled, ColorChannelSelect, TotalNumberOfCompressedValues, Index, OffsetValues) :
    OffsetValues = Array[UInt16](OffsetValues)
    return Command.WriteBlendMapOffsetValues(CompressionEnabled, ColorChannelSelect, TotalNumberOfCompressedValues, Index, OffsetValues)

def ReadBlendMapOffsetValues(ColorChannelSelect, Index, NoOfValues) :
    Summary, IsCompressionEnabled, OffsetValues = \
        Command.ReadBlendMapOffsetValues(ColorChannelSelect, Index, NoOfValues, 0, [])
    return Summary, int(IsCompressionEnabled), list(OffsetValues)

def WriteBlendMapControlPoints(HorizontalResolutionProjector, VerticalResolutionProjector, HorizontalCtrlPoints, VerticalCtrlPoints) :
    HorizontalCtrlPoints = Array[UInt16](HorizontalCtrlPoints)
    VerticalCtrlPoints = Array[UInt16](VerticalCtrlPoints)
    return Command.WriteBlendMapControlPoints(HorizontalResolutionProjector, VerticalResolutionProjector, HorizontalCtrlPoints, VerticalCtrlPoints)

def ReadBlendMapControlPoints() :
    Summary, HorizontalCtrlPoints, VerticalCtrlPoints = \
        Command.ReadBlendMapControlPoints([], [])
    return Summary, list(HorizontalCtrlPoints), list(VerticalCtrlPoints)

def WriteEnableEdgeBlending(EdgeBlendingEnable) :
    return Command.WriteEnableEdgeBlending(EdgeBlendingEnable)

def ReadEnableEdgeBlending() :
    Summary, EdgeBlendingEnable = \
        Command.ReadEnableEdgeBlending(False)
    return Summary, bool(EdgeBlendingEnable)

def WriteEdgeBlendingSystemParams(NumProjectorsColumns, NumProjectorsRows, SelfProjectorColumn, SelfProjectorRow, WhiteBlackLevels) :
    WhiteBlackLevels = Array[UInt32](WhiteBlackLevels)
    return Command.WriteEdgeBlendingSystemParams(NumProjectorsColumns, NumProjectorsRows, SelfProjectorColumn, SelfProjectorRow, WhiteBlackLevels)

def ReadEdgeBlendingSystemParams() :
    Summary, NumProjectorsColumns, NumProjectorsRows, SelfProjectorColumn, SelfProjectorRow, WhiteBlackLevels = \
        Command.ReadEdgeBlendingSystemParams(0, 0, 0, 0, [])
    return Summary, int(NumProjectorsColumns), int(NumProjectorsRows), int(SelfProjectorColumn), int(SelfProjectorRow), list(WhiteBlackLevels)

def WriteEdgeBlendingConfiguration(OverlapHorizontal, OverlapVertical, GeometricAdjustmentType, StorageOptions, GeometryParams) :
    GeometryParams = Array[UInt16](GeometryParams)
    return Command.WriteEdgeBlendingConfiguration(OverlapHorizontal, OverlapVertical, GeometricAdjustmentType, StorageOptions, GeometryParams)

def ReadEdgeBlendingConfiguration() :
    Summary, OverlapHorizontal, OverlapVertical, GeometricAdjustmentType, StorageOptions, GeometryParams = \
        Command.ReadEdgeBlendingConfiguration(0, 0, DispEdgeBlendGeometryModeT.NoGeometricCorrection, DispfmtEdgeBlendStorageOptionsT.DontStore, [])
    return Summary, int(OverlapHorizontal), int(OverlapVertical), GeometricAdjustmentType, StorageOptions, list(GeometryParams)

def WriteCwIndexDelay(Wheel, DegreesInteger, DegreesFraction) :
    return Command.WriteCwIndexDelay(Wheel, DegreesInteger, DegreesFraction)

def ReadCwIndexDelay(Wheel) :
    Summary, DegreesInteger, DegreesFraction = \
        Command.ReadCwIndexDelay(Wheel, 0, 0)
    return Summary, int(DegreesInteger), int(DegreesFraction)

def WriteInitializeOnTheFlyLoadSplashImage(SplashHeader, Width, Height) :
    SplashHeader = Array[Byte](SplashHeader)
    return Command.WriteInitializeOnTheFlyLoadSplashImage(SplashHeader, Width, Height)

def WriteLoadSplashImageOnTheFly(ImageData) :
    ImageData = Array[Byte](ImageData)
    return Command.WriteLoadSplashImageOnTheFly(ImageData)

def WriteXprCalibPatternDisplay() :
    return Command.WriteXprCalibPatternDisplay()

def WriteXpr4WayOrientation(XprOrientationNumber) :
    return Command.WriteXpr4WayOrientation(XprOrientationNumber)

def ReadXpr4WayOrientation() :
    Summary, XprOrientationNumber = \
        Command.ReadXpr4WayOrientation(0)
    return Summary, int(XprOrientationNumber)

def WriteXprActuatorWaveformControlParameter(XprCommand, AwcChannel, Data) :
    return Command.WriteXprActuatorWaveformControlParameter(XprCommand, AwcChannel, Data)

def ReadXprActuatorWaveformControlParameter(XprCommand, AwcChannel) :
    Summary, Data = \
        Command.ReadXprActuatorWaveformControlParameter(XprCommand, AwcChannel, 0)
    return Summary, int(Data)

def WriteLoad4WayXprWaveform(AwcChannel, Index, Data) :
    Data = Array[Byte](Data)
    return Command.WriteLoad4WayXprWaveform(AwcChannel, Index, Data)

def WriteDbAperturePosition(Position) :
    return Command.WriteDbAperturePosition(Position)

def ReadDbAperturePosition() :
    Summary, Position = \
        Command.ReadDbAperturePosition(0)
    return Summary, int(Position)

def WriteDbApertureMinMax(AptMin, AptMax) :
    return Command.WriteDbApertureMinMax(AptMin, AptMax)

def ReadDbApertureMinMax() :
    Summary, AptMin, AptMax = \
        Command.ReadDbApertureMinMax(0, 0)
    return Summary, int(AptMin), int(AptMax)

def WriteDbManualMode(Enable) :
    return Command.WriteDbManualMode(Enable)

def ReadDbManualMode() :
    Summary, Enable = \
        Command.ReadDbManualMode(0)
    return Summary, int(Enable)

def WriteDbBorderConfiguration(Top, Bottom, Left, Right) :
    return Command.WriteDbBorderConfiguration(Top, Bottom, Left, Right)

def ReadDbBorderConfiguration() :
    Summary, Top, Bottom, Left, Right = \
        Command.ReadDbBorderConfiguration(0, 0, 0, 0)
    return Summary, int(Top), int(Bottom), int(Left), int(Right)

def WriteDbBorderWeight(BorderWeight) :
    return Command.WriteDbBorderWeight(BorderWeight)

def ReadDbBorderWeight() :
    Summary, BorderWeight = \
        Command.ReadDbBorderWeight(DbPixelWeightT.DbWeight0)
    return Summary, BorderWeight

def WriteDbClipPixels(ClipPixels) :
    return Command.WriteDbClipPixels(ClipPixels)

def ReadDbClipPixels() :
    Summary, ClipPixels = \
        Command.ReadDbClipPixels(0)
    return Summary, int(ClipPixels)

def WriteDbGain(DbGain) :
    return Command.WriteDbGain(DbGain)

def ReadDbGain() :
    Summary, DbGain = \
        Command.ReadDbGain(0)
    return Summary, float(DbGain)

def WriteDbNumSteps(Steps) :
    return Command.WriteDbNumSteps(Steps)

def ReadDbNumSteps() :
    Summary, Steps = \
        Command.ReadDbNumSteps(0)
    return Summary, int(Steps)

def WriteDbApertureSpeed(Speed) :
    return Command.WriteDbApertureSpeed(Speed)

def ReadDbApertureSpeed() :
    Summary, Speed = \
        Command.ReadDbApertureSpeed(0)
    return Summary, int(Speed)

def WriteDbStrength(Strength) :
    return Command.WriteDbStrength(Strength)

def ReadDbStrength() :
    Summary, Strength = \
        Command.ReadDbStrength(0)
    return Summary, int(Strength)

def ReadDbHistogram() :
    Summary, HistPtr = \
        Command.ReadDbHistogram(bytearray())
    return Summary, bytearray(HistPtr)

def ReadDbCurrentApertPos() :
    Summary, Position = \
        Command.ReadDbCurrentApertPos(0)
    return Summary, int(Position)

def ReadCurrentLedColorPoint() :
    Summary, ChromaticX, ChromaticY, LuminanceY = \
        Command.ReadCurrentLedColorPoint(0, 0, 0)
    return Summary, float(ChromaticX), float(ChromaticY), int(LuminanceY)

def WriteWpcOptimalDutyCycle() :
    return Command.WriteWpcOptimalDutyCycle()

def ReadWpcOptimalDutyCycle() :
    Summary, WpcOptimalDutyCycleObj = \
        Command.ReadWpcOptimalDutyCycle(WpcOptimalDutyCycle())
    return Summary, WpcOptimalDutyCycleObj

def WriteWpcCalibrationData(LedColor, ChromaticX, ChromaticY, LuminanceY) :
    return Command.WriteWpcCalibrationData(LedColor, ChromaticX, ChromaticY, LuminanceY)

def ReadWpcCalibrationData(LedColor) :
    Summary, WpcCalibrationDataObj = \
        Command.ReadWpcCalibrationData(LedColor, WpcCalibrationData())
    return Summary, WpcCalibrationDataObj

def ReadNumberOfBrightnessTableEntries(ReadFrom) :
    Summary, NumberOfEntries = \
        Command.ReadNumberOfBrightnessTableEntries(ReadFrom, 0)
    return Summary, int(NumberOfEntries)

def WriteWpcBrightnessTableEntry(Index, AperturePosition, RedDriveLevel, GreenDriveLevel, BlueDriveLevel) :
    return Command.WriteWpcBrightnessTableEntry(Index, AperturePosition, RedDriveLevel, GreenDriveLevel, BlueDriveLevel)

def ReadWpcBrightnessTableEntry(ReadFrom, Index) :
    Summary, AperturePosition, RedDriveLevel, GreenDriveLevel, BlueDriveLevel = \
        Command.ReadWpcBrightnessTableEntry(ReadFrom, Index, 0, 0, 0, 0)
    return Summary, int(AperturePosition), int(RedDriveLevel), int(GreenDriveLevel), int(BlueDriveLevel)

def WriteTransferWpcBrightnessTableToEeprom() :
    return Command.WriteTransferWpcBrightnessTableToEeprom()

def WriteWpcBrightnessTableApertureValues(Size, ApertureValues) :
    ApertureValues = Array[UInt16](ApertureValues)
    return Command.WriteWpcBrightnessTableApertureValues(Size, ApertureValues)

def WriteWpcBrightnessTableBuildStart() :
    return Command.WriteWpcBrightnessTableBuildStart()

def ReadWpcBrightnessTableBuildStart() :
    Summary, TableUnderBuildProcess, CurrentBuildIndex = \
        Command.ReadWpcBrightnessTableBuildStart(0, 0)
    return Summary, int(TableUnderBuildProcess), int(CurrentBuildIndex)

def WriteWpcBrightnessTableBuildAbort() :
    return Command.WriteWpcBrightnessTableBuildAbort()

def ReadWpcSensorOutput() :
    Summary, Red, Green, Blue = \
        Command.ReadWpcSensorOutput(0, 0, 0)
    return Summary, int(Red), int(Green), int(Blue)

def WriteMaximumSsiDriveLevel(Color, MaxDriveLevel) :
    return Command.WriteMaximumSsiDriveLevel(Color, MaxDriveLevel)

def ReadMaximumSsiDriveLevel(Color) :
    Summary, MaxDriveLevel = \
        Command.ReadMaximumSsiDriveLevel(Color, 0)
    return Summary, int(MaxDriveLevel)

def WriteSsiDutyCycleIndex(Index) :
    return Command.WriteSsiDutyCycleIndex(Index)

def ReadSsiDutyCycleIndex() :
    Summary, SsiDutyCycleIndexObj = \
        Command.ReadSsiDutyCycleIndex(SsiDutyCycleIndex())
    return Summary, SsiDutyCycleIndexObj

def WriteEnableXprCalibrationMode(Enable) :
    return Command.WriteEnableXprCalibrationMode(Enable)

def ReadEnableXprCalibrationMode() :
    Summary, Enable = \
        Command.ReadEnableXprCalibrationMode(0)
    return Summary, int(Enable)

def WriteWpcCalibrationStructureOverride(WpcCalibrationStructureOverrideObj) :
    return Command.WriteWpcCalibrationStructureOverride(WpcCalibrationStructureOverrideObj)

def WriteDebugMessageMask(DebugMessageMaskObj) :
    return Command.WriteDebugMessageMask(DebugMessageMaskObj)

def ReadDebugMessageMask() :
    Summary, DebugMessageMaskObj = \
        Command.ReadDebugMessageMask(DebugMessageMask())
    return Summary, DebugMessageMaskObj

def WriteEnableUsbDebugLog(Enable) :
    return Command.WriteEnableUsbDebugLog(Enable)

def WriteEepromMemory(Index, Size, Pwd, Data) :
    Data = Array[Byte](Data)
    return Command.WriteEepromMemory(Index, Size, Pwd, Data)

def ReadEepromMemory(Index, Size) :
    Summary, Data = \
        Command.ReadEepromMemory(Index, Size, bytearray())
    return Summary, bytearray(Data)

def WriteDlpa3005Register(RegisterAddress, RegisterValue) :
    return Command.WriteDlpa3005Register(RegisterAddress, RegisterValue)

def ReadDlpa3005Register(RegisterAddress) :
    Summary, RegisterValue = \
        Command.ReadDlpa3005Register(RegisterAddress, 0)
    return Summary, int(RegisterValue)

def WriteTiActuatorInterfaceDebug(TiActQueryType, TiActAddr, TiActNumData) :
    return Command.WriteTiActuatorInterfaceDebug(TiActQueryType, TiActAddr, TiActNumData)

def ReadTiActuatorInterfaceDebug() :
    Summary, ActuatorData = \
        Command.ReadTiActuatorInterfaceDebug(bytearray())
    return Summary, bytearray(ActuatorData)

def ReadVsyncPeriod() :
    Summary, FramePeriod = \
        Command.ReadVsyncPeriod(0)
    return Summary, int(FramePeriod)

def WriteSoftwareReset() :
    return Command.WriteSoftwareReset()

def ReadRstCountCause() :
    Summary, ResetCount, ResetCause = \
        Command.ReadRstCountCause(0, 0)
    return Summary, int(ResetCount), int(ResetCause)

def ReadDmdPower() :
    Summary, Enable = \
        Command.ReadDmdPower(False)
    return Summary, bool(Enable)

def WriteDmdPark(Park) :
    return Command.WriteDmdPark(Park)

def ReadDmdPark() :
    Summary, Park = \
        Command.ReadDmdPark(False)
    return Summary, bool(Park)

def WriteDmdTrueGlobalReset(GlobalResetEnable) :
    return Command.WriteDmdTrueGlobalReset(GlobalResetEnable)

def ReadDmdTrueGlobalReset() :
    Summary, GlobalResetEnable = \
        Command.ReadDmdTrueGlobalReset(False)
    return Summary, bool(GlobalResetEnable)

def WriteTpmHardware(SigNo, SigType) :
    return Command.WriteTpmHardware(SigNo, SigType)

def ReadTpmHardware(SigNo) :
    Summary, SigType = \
        Command.ReadTpmHardware(SigNo, 0)
    return Summary, int(SigType)

def WriteTpmSoftware(SigNo, SigType) :
    return Command.WriteTpmSoftware(SigNo, SigType)

def ReadTpmSoftware(SigNo) :
    Summary, SigType = \
        Command.ReadTpmSoftware(SigNo, 0)
    return Summary, int(SigType)

def ReadIntStack() :
    Summary, StackSize, StackUsed, StackFree = \
        Command.ReadIntStack(0, 0, 0)
    return Summary, int(StackSize), int(StackUsed), int(StackFree)

def WritePrintAllTaskInformation() :
    return Command.WritePrintAllTaskInformation()

def ReadResource() :
    Summary, ResourceObj = \
        Command.ReadResource(Resource())
    return Summary, ResourceObj

def WriteCwStart(Start) :
    return Command.WriteCwStart(Start)

def ReadCwStart(Wheel) :
    Summary, Running = \
        Command.ReadCwStart(Wheel, 0)
    return Summary, int(Running)

def WriteCwOperationStatus(CoastEnabled, EnableDebugMode) :
    return Command.WriteCwOperationStatus(CoastEnabled, EnableDebugMode)

def ReadCwOperationStatus() :
    Summary, CwGetSpinning, CwIsCoastEnabled, CwGetDebugMode = \
        Command.ReadCwOperationStatus(0, 0, 0)
    return Summary, int(CwGetSpinning), int(CwIsCoastEnabled), int(CwGetDebugMode)

def WriteCwSpeed(Speed) :
    return Command.WriteCwSpeed(Speed)

def ReadCwSpeed(Wheel) :
    Summary, Period, Frequency = \
        Command.ReadCwSpeed(Wheel, 0, 0)
    return Summary, int(Period), int(Frequency)

def WriteCwDualTrackMode(Mode) :
    return Command.WriteCwDualTrackMode(Mode)

def ReadCwDualTrackMode() :
    Summary, Mode = \
        Command.ReadCwDualTrackMode(CwMultiWheelTrackingModeT.Slow)
    return Summary, Mode

def WriteCwSpokeTestConfiguration(Enable, SpokeNumber, RevolutionNumber, Mode) :
    return Command.WriteCwSpokeTestConfiguration(Enable, SpokeNumber, RevolutionNumber, Mode)

def ReadCwSpokeTestConfiguration() :
    Summary, Enable, SpokeNumber, RevolutionNumber, Mode = \
        Command.ReadCwSpokeTestConfiguration(0, 0, 0, SeqSpokeTestModesT.OneSpkOneRev)
    return Summary, int(Enable), int(SpokeNumber), int(RevolutionNumber), Mode

def WriteSeqEnable(Enable) :
    return Command.WriteSeqEnable(Enable)

def ReadSeqEnable() :
    Summary, SeqIsEnabled = \
        Command.ReadSeqEnable(0)
    return Summary, int(SeqIsEnabled)

def ReadEepromFreeAreaOffset() :
    Summary, FreeAreaOffset = \
        Command.ReadEepromFreeAreaOffset(0)
    return Summary, int(FreeAreaOffset)

def ReadVx1HwStatus() :
    Summary, Vx1HwStatusObj = \
        Command.ReadVx1HwStatus(Vx1HwStatus())
    return Summary, Vx1HwStatusObj

def WritePower() :
    return Command.WritePower()

def ReadPower() :
    Summary, PowerState = \
        Command.ReadPower(PowerstateEnum.Reset)
    return Summary, PowerState

def WriteDisplay(Source) :
    return Command.WriteDisplay(Source)

def ReadDisplay() :
    Summary, Source = \
        Command.ReadDisplay(CmdProjectionModes.DispExternal)
    return Summary, Source

def WriteEnableLowLatencyMode(Enable) :
    return Command.WriteEnableLowLatencyMode(Enable)

def ReadEnableLowLatencyMode() :
    Summary, Enable = \
        Command.ReadEnableLowLatencyMode(False)
    return Summary, bool(Enable)

def WriteSystemLook(System) :
    return Command.WriteSystemLook(System)

def ReadSystemLook() :
    Summary, System = \
        Command.ReadSystemLook(0)
    return Summary, int(System)

def WriteTpgBorder(Width, BorderColorRed, BorderColorGreen, BorderColorBlue) :
    return Command.WriteTpgBorder(Width, BorderColorRed, BorderColorGreen, BorderColorBlue)

def ReadTpgBorder() :
    Summary, Width, BorderColorRed, BorderColorGreen, BorderColorBlue = \
        Command.ReadTpgBorder(0, 0, 0, 0)
    return Summary, int(Width), int(BorderColorRed), int(BorderColorGreen), int(BorderColorBlue)

def WriteTpgResolution(HorizontalResolution, VerticalResolution) :
    return Command.WriteTpgResolution(HorizontalResolution, VerticalResolution)

def ReadTpgResolution() :
    Summary, HorizontalResolution, VerticalResolution = \
        Command.ReadTpgResolution(0, 0)
    return Summary, int(HorizontalResolution), int(VerticalResolution)

def WriteTpgFrameRate(FrameRate) :
    return Command.WriteTpgFrameRate(FrameRate)

def ReadTpgFrameRate() :
    Summary, FrameRate = \
        Command.ReadTpgFrameRate(0)
    return Summary, int(FrameRate)

def WriteSfgColor(Red, Green, Blue) :
    return Command.WriteSfgColor(Red, Green, Blue)

def ReadSfgColor() :
    Summary, Red, Green, Blue = \
        Command.ReadSfgColor(0, 0, 0)
    return Summary, int(Red), int(Green), int(Blue)

def WriteCurtainColor(Color) :
    return Command.WriteCurtainColor(Color)

def ReadCurtainColor() :
    Summary, Color = \
        Command.ReadCurtainColor(DispBackgroundColorT.Black)
    return Summary, Color

def WriteSplashLoadImage(Index) :
    return Command.WriteSplashLoadImage(Index)

def ReadSplashLoadImage() :
    Summary, Index = \
        Command.ReadSplashLoadImage(0)
    return Summary, int(Index)

def WriteEnableImageFlip(VertFlip, HorzFlip) :
    return Command.WriteEnableImageFlip(VertFlip, HorzFlip)

def ReadEnableImageFlip() :
    Summary, VertFlip, HorzFlip = \
        Command.ReadEnableImageFlip(False, False)
    return Summary, bool(VertFlip), bool(HorzFlip)

def WriteEnableFreeze(Freeze) :
    return Command.WriteEnableFreeze(Freeze)

def ReadEnableFreeze() :
    Summary, Freeze = \
        Command.ReadEnableFreeze(False)
    return Summary, bool(Freeze)

def WriteKeystoneAngles(Pitch, Yaw, Roll) :
    return Command.WriteKeystoneAngles(Pitch, Yaw, Roll)

def ReadKeystoneAngles() :
    Summary, Pitch, Yaw, Roll = \
        Command.ReadKeystoneAngles(0, 0, 0)
    return Summary, float(Pitch), float(Yaw), float(Roll)

def WriteKeystoneConfigOverride(ThrowRatio, VerticalOffset) :
    return Command.WriteKeystoneConfigOverride(ThrowRatio, VerticalOffset)

def ReadKeystoneConfigOverride() :
    Summary, ThrowRatio, VerticalOffset = \
        Command.ReadKeystoneConfigOverride(0, 0)
    return Summary, float(ThrowRatio), float(VerticalOffset)

def WriteEnableAnamorphicScaling(Enable) :
    return Command.WriteEnableAnamorphicScaling(Enable)

def ReadEnableAnamorphicScaling() :
    Summary, Enable = \
        Command.ReadEnableAnamorphicScaling(False)
    return Summary, bool(Enable)

def WriteDisplayImageSize(DisplayImageSizeObj) :
    return Command.WriteDisplayImageSize(DisplayImageSizeObj)

def ReadDisplayImageSize() :
    Summary, DisplayImageSizeObj = \
        Command.ReadDisplayImageSize(DisplayImageSize())
    return Summary, DisplayImageSizeObj

def WriteSourceConfiguration(SourceConfiguration) :
    return Command.WriteSourceConfiguration(SourceConfiguration)

def ReadSourceConfiguration() :
    Summary, SourceConfiguration = \
        Command.ReadSourceConfiguration(SourceConfigurationRead())
    return Summary, SourceConfiguration

def ReadDatapathScanStatus() :
    Summary, ScanStatus, DatapathState = \
        Command.ReadDatapathScanStatus(DpScanStatus.DetectStableVideo, DpState.Standby)
    return Summary, ScanStatus, DatapathState

def ReadFrameRateParms() :
    Summary, InputFrameRate, OutputFrameRate, FrcMode = \
        Command.ReadFrameRateParms(0, 0, FrameFrcModeT.Fixed)
    return Summary, float(InputFrameRate), float(OutputFrameRate), FrcMode

def WriteXprEnableModeCommand(Mode) :
    return Command.WriteXprEnableModeCommand(Mode)

def ReadXprEnableModeCommand() :
    Summary, Mode = \
        Command.ReadXprEnableModeCommand(DispXprEnableModeT.Auto)
    return Summary, Mode

def ReadExecutionTimeOfLastCommandSent() :
    Summary, CommandId, CommandExecutionTime, TotalExecutionTime = \
        Command.ReadExecutionTimeOfLastCommandSent(0, 0, 0)
    return Summary, int(CommandId), int(CommandExecutionTime), int(TotalExecutionTime)

def WriteVboConfiguration(DataMapMode, ByteMode, NumberOfLanes, EnablePixelRepeat) :
    return Command.WriteVboConfiguration(DataMapMode, ByteMode, NumberOfLanes, EnablePixelRepeat)

def ReadVboConfiguration() :
    Summary, DataMapMode, ByteMode, NumberOfLanes, EnablePixelRepeat = \
        Command.ReadVboConfiguration(SrcVboDataMapModeT.Mode0, SrcVboByteModeT.SrcVbo3BytesMode, 0, False)
    return Summary, DataMapMode, ByteMode, int(NumberOfLanes), bool(EnablePixelRepeat)

def WriteFpdConfiguration(FpdMode, DataInterfaceMode, Enable3DRef, EnableField, EnablePixelRepeat) :
    return Command.WriteFpdConfiguration(FpdMode, DataInterfaceMode, Enable3DRef, EnableField, EnablePixelRepeat)

def ReadFpdConfiguration() :
    Summary, FpdMode, DataInterfaceMode, Enable3DRef, EnableField, EnablePixelRepeat = \
        Command.ReadFpdConfiguration(SrcFpdDataMapModeT.SrcFpd30BitmapMode0, SrcFpdDataInterfaceModeT.OddevenOnA, False, False, False)
    return Summary, FpdMode, DataInterfaceMode, bool(Enable3DRef), bool(EnableField), bool(EnablePixelRepeat)

def WriteKeystoneCorners(KeystoneCornersObj) :
    return Command.WriteKeystoneCorners(KeystoneCornersObj)

def ReadKeystoneCorners() :
    Summary, KeystoneCornersObj = \
        Command.ReadKeystoneCorners(KeystoneCorners())
    return Summary, KeystoneCornersObj

def WriteWarpTimingValidationEnableAdjustWrp(Enable) :
    return Command.WriteWarpTimingValidationEnableAdjustWrp(Enable)

def ReadWarpTimingValidationEnableAdjustWrp() :
    Summary, Enable = \
        Command.ReadWarpTimingValidationEnableAdjustWrp(False)
    return Summary, bool(Enable)

def ReadIsWarpGeometryModified() :
    Summary, State = \
        Command.ReadIsWarpGeometryModified(False)
    return Summary, bool(State)

def WriteIlluminationEnable(Enable) :
    return Command.WriteIlluminationEnable(Enable)

def ReadIlluminationEnable() :
    Summary, Enable = \
        Command.ReadIlluminationEnable(0)
    return Summary, int(Enable)

def WriteDlpa3005IlluminationCurrent(DriveLevelRed, DriveLevelGreen, DriveLevelBlue) :
    return Command.WriteDlpa3005IlluminationCurrent(DriveLevelRed, DriveLevelGreen, DriveLevelBlue)

def ReadDlpa3005IlluminationCurrent() :
    Summary, DriveLevelRed, DriveLevelGreen, DriveLevelBlue = \
        Command.ReadDlpa3005IlluminationCurrent(0, 0, 0)
    return Summary, int(DriveLevelRed), int(DriveLevelGreen), int(DriveLevelBlue)

def WriteSsiDriveLevels(PwmGroup, SsiDriveLevelsObj) :
    return Command.WriteSsiDriveLevels(PwmGroup, SsiDriveLevelsObj)

def ReadSsiDriveLevels(PwmGroup) :
    Summary, SsiDriveLevelsObj = \
        Command.ReadSsiDriveLevels(PwmGroup, SsiDriveLevels())
    return Summary, SsiDriveLevelsObj

def WriteVarLmpEnableComms(Enable) :
    return Command.WriteVarLmpEnableComms(Enable)

def ReadVarLmpEnableComms() :
    Summary, Enable = \
        Command.ReadVarLmpEnableComms(0)
    return Summary, int(Enable)

def WriteVarLmpWaveformIndex(WaveformIndex) :
    return Command.WriteVarLmpWaveformIndex(WaveformIndex)

def ReadVarLmpWaveformIndex() :
    Summary, WaveformIndex = \
        Command.ReadVarLmpWaveformIndex(0)
    return Summary, int(WaveformIndex)

def ReadVarLmpWaveformId() :
    Summary, WaveformId = \
        Command.ReadVarLmpWaveformId(0)
    return Summary, int(WaveformId)

def ReadVarLmpNumOfWaveForms() :
    Summary, NumWaveforms = \
        Command.ReadVarLmpNumOfWaveForms(0)
    return Summary, int(NumWaveforms)

def WriteVarLmpWaveformGain(WaveformGain) :
    return Command.WriteVarLmpWaveformGain(WaveformGain)

def ReadVarLmpWaveformGain() :
    Summary, WaveformGain = \
        Command.ReadVarLmpWaveformGain(0)
    return Summary, int(WaveformGain)

def WriteLmpSyncType(SyncType, NegativePolarity, LampSyncSel) :
    return Command.WriteLmpSyncType(SyncType, NegativePolarity, LampSyncSel)

def ReadLmpSyncType() :
    Summary, SyncType, NegativePolarity, LampSyncSel = \
        Command.ReadLmpSyncType(LmpSyncTypes.Pulse, 0, 0)
    return Summary, SyncType, int(NegativePolarity), int(LampSyncSel)

def WriteLmpSyncDelay(ThisDelay) :
    return Command.WriteLmpSyncDelay(ThisDelay)

def ReadLmpSyncDelay() :
    Summary, ThisDelay = \
        Command.ReadLmpSyncDelay(0)
    return Summary, int(ThisDelay)

def ReadVarLmpMinGain() :
    Summary, MinGain = \
        Command.ReadVarLmpMinGain(0)
    return Summary, int(MinGain)

def ReadVarLmpMaxGain() :
    Summary, MaxGain = \
        Command.ReadVarLmpMaxGain(0)
    return Summary, int(MaxGain)

def ReadVarLmpManufactureId() :
    Summary, ManufacturerId = \
        Command.ReadVarLmpManufactureId(0)
    return Summary, int(ManufacturerId)

def ReadVarLmpBallastId() :
    Summary, BallastId = \
        Command.ReadVarLmpBallastId(0)
    return Summary, int(BallastId)

def ReadVarLmpBallastStatus() :
    Summary, BallastStatus = \
        Command.ReadVarLmpBallastStatus(0)
    return Summary, int(BallastStatus)

def ReadVarLmpLampStatus() :
    Summary, SafeMode, ErrorCode = \
        Command.ReadVarLmpLampStatus(0, 0)
    return Summary, int(SafeMode), int(ErrorCode)

def WriteLmpDynGain(PowerGain) :
    return Command.WriteLmpDynGain(PowerGain)

def WriteLmpDynGainState(State) :
    return Command.WriteLmpDynGainState(State)

def ReadLmpDynGainStatus() :
    Summary, LmpDynGainStatusObj = \
        Command.ReadLmpDynGainStatus(LmpDynGainStatus())
    return Summary, LmpDynGainStatusObj

def WriteLmpWaveformIndexOverride(WaveformIndexOverrideEnable) :
    return Command.WriteLmpWaveformIndexOverride(WaveformIndexOverrideEnable)

def ReadLmpWaveformIndexOverride() :
    Summary, WaveformIndexOverrideEnable = \
        Command.ReadLmpWaveformIndexOverride(0)
    return Summary, int(WaveformIndexOverrideEnable)

def WriteImageAlgorithmEnable(ImageAlgorithmEnableObj) :
    return Command.WriteImageAlgorithmEnable(ImageAlgorithmEnableObj)

def ReadImageAlgorithmEnable() :
    Summary, ImageAlgorithmEnableObj = \
        Command.ReadImageAlgorithmEnable(ImageAlgorithmEnable())
    return Summary, ImageAlgorithmEnableObj

def WriteImageBrightness(BrightnessAdjustment) :
    return Command.WriteImageBrightness(BrightnessAdjustment)

def ReadImageBrightness() :
    Summary, BrightnessAdjustment = \
        Command.ReadImageBrightness(0)
    return Summary, float(BrightnessAdjustment)

def WriteImageContrast(Contrast) :
    return Command.WriteImageContrast(Contrast)

def ReadImageContrast() :
    Summary, Contrast = \
        Command.ReadImageContrast(0)
    return Summary, int(Contrast)

def WriteImageHueAndColorControl(HueAdjustmentAngle, ColorControlGain) :
    return Command.WriteImageHueAndColorControl(HueAdjustmentAngle, ColorControlGain)

def ReadImageHueAndColorControl() :
    Summary, HueAdjustmentAngle, ColorControlGain = \
        Command.ReadImageHueAndColorControl(0, 0)
    return Summary, int(HueAdjustmentAngle), int(ColorControlGain)

def WriteImageSharpness(Sharpness) :
    return Command.WriteImageSharpness(Sharpness)

def ReadImageSharpness() :
    Summary, Sharpness = \
        Command.ReadImageSharpness(0)
    return Summary, int(Sharpness)

def WriteImageRgbOffset(RedOffset, GreenOffset, BlueOffset) :
    return Command.WriteImageRgbOffset(RedOffset, GreenOffset, BlueOffset)

def ReadImageRgbOffset() :
    Summary, RedOffset, GreenOffset, BlueOffset = \
        Command.ReadImageRgbOffset(0, 0, 0)
    return Summary, float(RedOffset), float(GreenOffset), float(BlueOffset)

def WriteImageRgbGain(RedGain, GreenGain, BlueGain) :
    return Command.WriteImageRgbGain(RedGain, GreenGain, BlueGain)

def ReadImageRgbGain() :
    Summary, RedGain, GreenGain, BlueGain = \
        Command.ReadImageRgbGain(0, 0, 0)
    return Summary, int(RedGain), int(GreenGain), int(BlueGain)

def WriteCscTable(Index) :
    return Command.WriteCscTable(Index)

def ReadCscTable() :
    Summary, Index = \
        Command.ReadCscTable(SrcCscTablesT.TableFullrangeRgb)
    return Summary, Index

def WriteImageCcaCoordinates(ImageCcaCoordinatesObj) :
    return Command.WriteImageCcaCoordinates(ImageCcaCoordinatesObj)

def ReadImageCcaCoordinates() :
    Summary, ImageCcaCoordinatesObj = \
        Command.ReadImageCcaCoordinates(ImageCcaCoordinates())
    return Summary, ImageCcaCoordinatesObj

def WriteImageHsg(ImageHsgObj) :
    return Command.WriteImageHsg(ImageHsgObj)

def ReadImageHsg() :
    Summary, ImageHsgObj = \
        Command.ReadImageHsg(ImageHsg())
    return Summary, ImageHsgObj

def WriteImageGammaLut(GammaLutNumber) :
    return Command.WriteImageGammaLut(GammaLutNumber)

def ReadImageGammaLut() :
    Summary, GammaLutNumber = \
        Command.ReadImageGammaLut(0)
    return Summary, int(GammaLutNumber)

def WriteImageGammaCurveShift(RedShift, GreenShift, BlueShift, AllColorShift) :
    return Command.WriteImageGammaCurveShift(RedShift, GreenShift, BlueShift, AllColorShift)

def ReadImageGammaCurveShift() :
    Summary, RedShift, GreenShift, BlueShift, AllColorShift = \
        Command.ReadImageGammaCurveShift(0, 0, 0, 0)
    return Summary, int(RedShift), int(GreenShift), int(BlueShift), int(AllColorShift)

def WriteImgWhitePeakingFactor(WhitePeakingVal) :
    return Command.WriteImgWhitePeakingFactor(WhitePeakingVal)

def ReadImgWhitePeakingFactor() :
    Summary, WhitePeakingVal = \
        Command.ReadImgWhitePeakingFactor(0)
    return Summary, int(WhitePeakingVal)

def WriteXprFilterStrengthCommand(Strength) :
    return Command.WriteXprFilterStrengthCommand(Strength)

def ReadXprFilterStrengthCommand() :
    Summary, Strength = \
        Command.ReadXprFilterStrengthCommand(0)
    return Summary, int(Strength)

def WriteHdrSourceConfiguration(HdrSourceConfigurationObj) :
    return Command.WriteHdrSourceConfiguration(HdrSourceConfigurationObj)

def ReadHdrSourceConfiguration() :
    Summary, HdrSourceConfigurationObj = \
        Command.ReadHdrSourceConfiguration(HdrSourceConfiguration())
    return Summary, HdrSourceConfigurationObj

def WriteHdrStrengthSetting(HdrStrength) :
    return Command.WriteHdrStrengthSetting(HdrStrength)

def ReadHdrStrengthSetting() :
    Summary, HdrStrength = \
        Command.ReadHdrStrengthSetting(0)
    return Summary, int(HdrStrength)

def WriteSystemBrightnessRangeSetting(MinBrightness, MaxBrightness) :
    return Command.WriteSystemBrightnessRangeSetting(MinBrightness, MaxBrightness)

def ReadSystemBrightnessRangeSetting() :
    Summary, MinBrightness, MaxBrightness = \
        Command.ReadSystemBrightnessRangeSetting(0, 0)
    return Summary, float(MinBrightness), float(MaxBrightness)

def WriteImageColorProfile(ColorProfile) :
    return Command.WriteImageColorProfile(ColorProfile)

def WriteImagePointHsg(Point, ImagePointHsgObj) :
    return Command.WriteImagePointHsg(Point, ImagePointHsgObj)

def ReadImagePointHsg(Point) :
    Summary, ImagePointHsgObj = \
        Command.ReadImagePointHsg(Point, ImagePointHsg())
    return Summary, ImagePointHsgObj

def WriteSpccControlPoints(ControlPointY, ControlPointX1, ControlPointX2) :
    return Command.WriteSpccControlPoints(ControlPointY, ControlPointX1, ControlPointX2)

def ReadSpccControlPoints() :
    Summary, ControlPointY, ControlPointX1, ControlPointX2 = \
        Command.ReadSpccControlPoints(0, 0, 0)
    return Summary, int(ControlPointY), int(ControlPointX1), int(ControlPointX2)

def WritePccCoefficientsDirect(Point, PccCoefficientsDirectObj) :
    return Command.WritePccCoefficientsDirect(Point, PccCoefficientsDirectObj)

def ReadPccCoefficientsDirect(Point) :
    Summary, PccCoefficientsDirectObj = \
        Command.ReadPccCoefficientsDirect(Point, PccCoefficientsDirect())
    return Summary, PccCoefficientsDirectObj

def WriteWpcTargetManualMode(Enable) :
    return Command.WriteWpcTargetManualMode(Enable)

def ReadWpcTargetManualMode() :
    Summary, Enable = \
        Command.ReadWpcTargetManualMode(0)
    return Summary, int(Enable)

def WriteWpcTargetColorPoint(CieX, CieY) :
    return Command.WriteWpcTargetColorPoint(CieX, CieY)

def ReadWpcTargetColorPoint() :
    Summary, CieX, CieY = \
        Command.ReadWpcTargetColorPoint(0, 0)
    return Summary, float(CieX), float(CieY)

def WriteGpioPinConfig(PinNumber, Output, LogicVal, OpenDrain) :
    return Command.WriteGpioPinConfig(PinNumber, Output, LogicVal, OpenDrain)

def ReadGpioPinConfig(PinNumber) :
    Summary, Output, LogicVal, OpenDrain = \
        Command.ReadGpioPinConfig(PinNumber, False, False, False)
    return Summary, bool(Output), bool(LogicVal), bool(OpenDrain)

def WriteGpioPin(PinNumber, LogicVal) :
    return Command.WriteGpioPin(PinNumber, LogicVal)

def ReadGpioPin(PinNumber) :
    Summary, LogicVal = \
        Command.ReadGpioPin(PinNumber, False)
    return Summary, bool(LogicVal)

def WriteStatusIntMask(StatusIntMaskObj) :
    return Command.WriteStatusIntMask(StatusIntMaskObj)

def ReadStatusIntMask() :
    Summary, StatusIntMaskObj = \
        Command.ReadStatusIntMask(StatusIntMask())
    return Summary, StatusIntMaskObj

def WriteGenPurpseClockEnable(Clk, Enabled, Freq) :
    return Command.WriteGenPurpseClockEnable(Clk, Enabled, Freq)

def ReadGenPurpseClockEnable(Clk) :
    Summary, IsEnabled = \
        Command.ReadGenPurpseClockEnable(Clk, 0)
    return Summary, int(IsEnabled)

def ReadGenPurpseClockFrequency(Clk) :
    Summary, Freq = \
        Command.ReadGenPurpseClockFrequency(Clk, 0)
    return Summary, int(Freq)

def WritePwmOutputConfiguration(Port, Frequency, DutyCycle, OutputEnabled) :
    return Command.WritePwmOutputConfiguration(Port, Frequency, DutyCycle, OutputEnabled)

def ReadPwmOutputConfiguration(Port) :
    Summary, Frequency, DutyCycle, OutputEnabledBit = \
        Command.ReadPwmOutputConfiguration(Port, 0, 0, False)
    return Summary, int(Frequency), int(DutyCycle), bool(OutputEnabledBit)

def WritePwmInputConfiguration(Port, SampleRate, InCounterEnabled) :
    return Command.WritePwmInputConfiguration(Port, SampleRate, InCounterEnabled)

def ReadPwmInputConfiguration(Port) :
    Summary, SampleRate, InCounterEnabled, HighPulseWidth, LowPulseWidth, DutyCycle = \
        Command.ReadPwmInputConfiguration(Port, 0, 0, 0, 0, 0)
    return Summary, int(SampleRate), int(InCounterEnabled), int(HighPulseWidth), int(LowPulseWidth), int(DutyCycle)

def WriteI2CPassthrough(I2CPassthroughObj) :
    return Command.WriteI2CPassthrough(I2CPassthroughObj)

def ReadI2CPassthrough(Port, Is7Bit, HasSubaddr, ClockRate, DeviceAddress, ByteCount, SubAddr) :
    Summary, DataBytes = \
        Command.ReadI2CPassthrough(Port, Is7Bit, HasSubaddr, ClockRate, DeviceAddress, ByteCount, SubAddr, bytearray())
    return Summary, bytearray(DataBytes)

def WriteCwPwmConfiguration(Port, Enable, DutyCycle) :
    return Command.WriteCwPwmConfiguration(Port, Enable, DutyCycle)

def ReadCwPwmConfiguration(Port) :
    Summary, Available, Enable, DutyCycle = \
        Command.ReadCwPwmConfiguration(Port, 0, 0, 0)
    return Summary, int(Available), int(Enable), int(DutyCycle)

def ReadDmdTemperature() :
    Summary, Temperature = \
        Command.ReadDmdTemperature(0)
    return Summary, int(Temperature)

def WriteLmpFanCtl(FanNum, SwFreq, DutyCycle, Select) :
    return Command.WriteLmpFanCtl(FanNum, SwFreq, DutyCycle, Select)

def ReadLmpFanCtl(FanNum, Select) :
    Summary, SwFreq, DutyCycle = \
        Command.ReadLmpFanCtl(FanNum, Select, 0, 0)
    return Summary, int(SwFreq), int(DutyCycle)

def WriteEepromLockState(LockState) :
    return Command.WriteEepromLockState(LockState)

def ReadEepromLockState() :
    Summary, LockState = \
        Command.ReadEepromLockState(0)
    return Summary, int(LockState)

def WriteUartConfiguration(Port, UartConfigurationObj) :
    return Command.WriteUartConfiguration(Port, UartConfigurationObj)

def ReadUartConfiguration(Port) :
    Summary, UartConfigurationObj = \
        Command.ReadUartConfiguration(Port, UartConfiguration())
    return Summary, UartConfigurationObj

def WriteManualWarpTable(WarpTableIndex, WarpPoints) :
    WarpPoints = Array[UInt16](WarpPoints)
    return Command.WriteManualWarpTable(WarpTableIndex, WarpPoints)

def ReadManualWarpTable(WarpTableIndex, NumEntries) :
    Summary, WarpPoints = \
        Command.ReadManualWarpTable(WarpTableIndex, NumEntries, [])
    return Summary, list(WarpPoints)

def WriteManualWarpControlPoints(ControlPointsDefinedByArray, HorizontalCtrlPoints, VerticalCtrlPoints) :
    HorizontalCtrlPoints = Array[UInt16](HorizontalCtrlPoints)
    VerticalCtrlPoints = Array[UInt16](VerticalCtrlPoints)
    return Command.WriteManualWarpControlPoints(ControlPointsDefinedByArray, HorizontalCtrlPoints, VerticalCtrlPoints)

def ReadManualWarpControlPoints() :
    Summary, ControlPointsDefinedByArray, CtrlPoints = \
        Command.ReadManualWarpControlPoints(0, [])
    return Summary, int(ControlPointsDefinedByArray), list(CtrlPoints)

def WriteApplyManualWarping(WarpEnabled) :
    return Command.WriteApplyManualWarping(WarpEnabled)

def ReadApplyManualWarping() :
    Summary, WarpEnabled = \
        Command.ReadApplyManualWarping(False)
    return Summary, bool(WarpEnabled)

def WriteSmoothWarpTable(SmoothWarpTableObj) :
    return Command.WriteSmoothWarpTable(SmoothWarpTableObj)

def ReadSmoothWarpTable() :
    Summary, SmoothWarpTableObj = \
        Command.ReadSmoothWarpTable(SmoothWarpTable())
    return Summary, SmoothWarpTableObj

def WriteManualWarpTableUpdateMode(Mode) :
    return Command.WriteManualWarpTableUpdateMode(Mode)

def ReadManualWarpTableUpdateMode() :
    Summary, Mode = \
        Command.ReadManualWarpTableUpdateMode(0)
    return Summary, int(Mode)

def WritePadChipIdentificationRegister(RevId, ChipId) :
    return Command.WritePadChipIdentificationRegister(RevId, ChipId)

def ReadPadChipIdentificationRegister() :
    Summary, RevId, ChipId = \
        Command.ReadPadChipIdentificationRegister(0, 0)
    return Summary, int(RevId), int(ChipId)

def WritePadEnableRegister(PadEnableRegisterObj) :
    return Command.WritePadEnableRegister(PadEnableRegisterObj)

def ReadPadEnableRegister() :
    Summary, PadEnableRegisterObj = \
        Command.ReadPadEnableRegister(PadEnableRegister())
    return Summary, PadEnableRegisterObj

def WritePadIregSwitchControl(IllumSwCurrentLimitEnable, IllumSwCurrentLimit) :
    return Command.WritePadIregSwitchControl(IllumSwCurrentLimitEnable, IllumSwCurrentLimit)

def ReadPadIregSwitchControl() :
    Summary, IllumSwCurrentLimitEnable, IllumSwCurrentLimit = \
        Command.ReadPadIregSwitchControl(0, 0)
    return Summary, int(IllumSwCurrentLimitEnable), int(IllumSwCurrentLimit)

def WritePadSw1IdacMsbBits8And9(SwLedCurrentCh1Msb) :
    return Command.WritePadSw1IdacMsbBits8And9(SwLedCurrentCh1Msb)

def ReadPadSw1IdacMsbBits8And9() :
    Summary, SwLedCurrentCh1Msb = \
        Command.ReadPadSw1IdacMsbBits8And9(0)
    return Summary, int(SwLedCurrentCh1Msb)

def WritePadSw1IdacLsbBits0To7(SwLedCurrentCh1Lsb) :
    return Command.WritePadSw1IdacLsbBits0To7(SwLedCurrentCh1Lsb)

def ReadPadSw1IdacLsbBits0To7() :
    Summary, SwLedCurrentCh1Lsb = \
        Command.ReadPadSw1IdacLsbBits0To7(0)
    return Summary, int(SwLedCurrentCh1Lsb)

def WritePadSw2IdacMsbBits8And9(SwLedCurrentCh2Msb) :
    return Command.WritePadSw2IdacMsbBits8And9(SwLedCurrentCh2Msb)

def ReadPadSw2IdacMsbBits8And9() :
    Summary, SwLedCurrentCh2Msb = \
        Command.ReadPadSw2IdacMsbBits8And9(0)
    return Summary, int(SwLedCurrentCh2Msb)

def WritePadSw2IdacLsbBits0To7(SwLedCurrentCh2Lsb) :
    return Command.WritePadSw2IdacLsbBits0To7(SwLedCurrentCh2Lsb)

def ReadPadSw2IdacLsbBits0To7() :
    Summary, SwLedCurrentCh2Lsb = \
        Command.ReadPadSw2IdacLsbBits0To7(0)
    return Summary, int(SwLedCurrentCh2Lsb)

def WritePadSw3IdacMsbBits8And9(SwLedCurrentCh3Msb) :
    return Command.WritePadSw3IdacMsbBits8And9(SwLedCurrentCh3Msb)

def ReadPadSw3IdacMsbBits8And9() :
    Summary, SwLedCurrentCh3Msb = \
        Command.ReadPadSw3IdacMsbBits8And9(0)
    return Summary, int(SwLedCurrentCh3Msb)

def WritePadSw3IdacLsbBits0To7(SwLedCurrentCh3Lsb) :
    return Command.WritePadSw3IdacLsbBits0To7(SwLedCurrentCh3Lsb)

def ReadPadSw3IdacLsbBits0To7() :
    Summary, SwLedCurrentCh3Lsb = \
        Command.ReadPadSw3IdacLsbBits0To7(0)
    return Summary, int(SwLedCurrentCh3Lsb)

def WritePadSwitchOnOffControl(Sw1Enable, Sw2Enable, Sw3Enable) :
    return Command.WritePadSwitchOnOffControl(Sw1Enable, Sw2Enable, Sw3Enable)

def ReadPadSwitchOnOffControl() :
    Summary, Sw1Enable, Sw2Enable, Sw3Enable = \
        Command.ReadPadSwitchOnOffControl(False, False, False)
    return Summary, bool(Sw1Enable), bool(Sw2Enable), bool(Sw3Enable)

def WritePadAnalogFrontEnd1(AfeSel, AfeGain, AfeCalDisable, AfeEnable) :
    return Command.WritePadAnalogFrontEnd1(AfeSel, AfeGain, AfeCalDisable, AfeEnable)

def ReadPadAnalogFrontEnd1() :
    Summary, AfeSel, AfeGain, AfeCalDisable, AfeEnable = \
        Command.ReadPadAnalogFrontEnd1(0, 0, False, False)
    return Summary, int(AfeSel), int(AfeGain), bool(AfeCalDisable), bool(AfeEnable)

def WritePadAnalogFrontEnd2(AfeDivSel, SampleLabbEnable, TsampleSel) :
    return Command.WritePadAnalogFrontEnd2(AfeDivSel, SampleLabbEnable, TsampleSel)

def ReadPadAnalogFrontEnd2() :
    Summary, AfeDivSel, SampleLabbEnable, TsampleSel = \
        Command.ReadPadAnalogFrontEnd2(0, False, 0)
    return Summary, int(AfeDivSel), bool(SampleLabbEnable), int(TsampleSel)

def WritePadMainStatusRegister(PadMainStatusRegisterObj) :
    return Command.WritePadMainStatusRegister(PadMainStatusRegisterObj)

def ReadPadMainStatusRegister() :
    Summary, PadMainStatusRegisterObj = \
        Command.ReadPadMainStatusRegister(PadMainStatusRegister())
    return Summary, PadMainStatusRegisterObj

def WritePadInterruptMaskRegister(PadInterruptMaskRegisterObj) :
    return Command.WritePadInterruptMaskRegister(PadInterruptMaskRegisterObj)

def ReadPadInterruptMaskRegister() :
    Summary, PadInterruptMaskRegisterObj = \
        Command.ReadPadInterruptMaskRegister(PadInterruptMaskRegister())
    return Summary, PadInterruptMaskRegisterObj

def WritePadBreakBeforeMakeDelay(BbmDelay) :
    return Command.WritePadBreakBeforeMakeDelay(BbmDelay)

def ReadPadBreakBeforeMakeDelay() :
    Summary, BbmDelay = \
        Command.ReadPadBreakBeforeMakeDelay(0)
    return Summary, int(BbmDelay)

def WritePadFastShutdownTimingReg(Vbias, Vofs) :
    return Command.WritePadFastShutdownTimingReg(Vbias, Vofs)

def ReadPadFastShutdownTimingReg() :
    Summary, Vbias, Vofs = \
        Command.ReadPadFastShutdownTimingReg(0, 0)
    return Summary, int(Vbias), int(Vofs)

def WritePadVofsStateDurationReg(LowbattSel, VofsStateDuration) :
    return Command.WritePadVofsStateDurationReg(LowbattSel, VofsStateDuration)

def ReadPadVofsStateDurationReg() :
    Summary, LowbattSel, VofsStateDuration = \
        Command.ReadPadVofsStateDurationReg(0, 0)
    return Summary, int(LowbattSel), int(VofsStateDuration)

def WritePadVbiasStateDurationReg(UvloSel, VbiasStateDuration) :
    return Command.WritePadVbiasStateDurationReg(UvloSel, VbiasStateDuration)

def ReadPadVbiasStateDurationReg() :
    Summary, UvloSel, VbiasStateDuration = \
        Command.ReadPadVbiasStateDurationReg(0, 0)
    return Summary, int(UvloSel), int(VbiasStateDuration)

def WritePadGp1BuckConverterVoltageSelection(BuckGp1ConvVoltageSel) :
    return Command.WritePadGp1BuckConverterVoltageSelection(BuckGp1ConvVoltageSel)

def ReadPadGp1BuckConverterVoltageSelection() :
    Summary, BuckGp1ConvVoltageSel = \
        Command.ReadPadGp1BuckConverterVoltageSelection(0)
    return Summary, int(BuckGp1ConvVoltageSel)

def WritePadGp2BuckConverterVoltageSelection(BuckGp2ConvVoltageSel) :
    return Command.WritePadGp2BuckConverterVoltageSelection(BuckGp2ConvVoltageSel)

def ReadPadGp2BuckConverterVoltageSelection() :
    Summary, BuckGp2ConvVoltageSel = \
        Command.ReadPadGp2BuckConverterVoltageSelection(0)
    return Summary, int(BuckGp2ConvVoltageSel)

def WritePadGp3BuckConverterVoltageSelection(BuckGp3ConvVoltageSel) :
    return Command.WritePadGp3BuckConverterVoltageSelection(BuckGp3ConvVoltageSel)

def ReadPadGp3BuckConverterVoltageSelection() :
    Summary, BuckGp3ConvVoltageSel = \
        Command.ReadPadGp3BuckConverterVoltageSelection(0)
    return Summary, int(BuckGp3ConvVoltageSel)

def WritePadGp1BuckSkipMode(BuckGp1ConvVoltageSel) :
    return Command.WritePadGp1BuckSkipMode(BuckGp1ConvVoltageSel)

def ReadPadGp1BuckSkipMode() :
    Summary, BuckGp1ConvVoltageSel = \
        Command.ReadPadGp1BuckSkipMode(0)
    return Summary, int(BuckGp1ConvVoltageSel)

def WritePadUserConfigurationSelection(PadUserConfigurationSelectionObj) :
    return Command.WritePadUserConfigurationSelection(PadUserConfigurationSelectionObj)

def ReadPadUserConfigurationSelection() :
    Summary, PadUserConfigurationSelectionObj = \
        Command.ReadPadUserConfigurationSelection(PadUserConfigurationSelection())
    return Summary, PadUserConfigurationSelectionObj

def WritePadOlvLaserBypassVinDivisionFactor(IllumLaserBypEl, IllumOlvSel) :
    return Command.WritePadOlvLaserBypassVinDivisionFactor(IllumLaserBypEl, IllumOlvSel)

def ReadPadOlvLaserBypassVinDivisionFactor() :
    Summary, IllumLaserBypEl, IllumOlvSel = \
        Command.ReadPadOlvLaserBypassVinDivisionFactor(0, 0)
    return Summary, int(IllumLaserBypEl), int(IllumOlvSel)

def WritePadIllumBuckConverterOvervoltageFaultLevel(IllumBcOvFaultSel) :
    return Command.WritePadIllumBuckConverterOvervoltageFaultLevel(IllumBcOvFaultSel)

def ReadPadIllumBuckConverterOvervoltageFaultLevel() :
    Summary, IllumBcOvFaultSel = \
        Command.ReadPadIllumBuckConverterOvervoltageFaultLevel(0)
    return Summary, int(IllumBcOvFaultSel)

def WritePadCwPwmVoltageLsb0To7(CwPwmLsb) :
    return Command.WritePadCwPwmVoltageLsb0To7(CwPwmLsb)

def ReadPadCwPwmVoltageLsb0To7() :
    Summary, CwPwmLsb = \
        Command.ReadPadCwPwmVoltageLsb0To7(0)
    return Summary, int(CwPwmLsb)

def WritePadCwPwmVoltageMsb8To15(CwPwmMsb) :
    return Command.WritePadCwPwmVoltageMsb8To15(CwPwmMsb)

def ReadPadCwPwmVoltageMsb8To15() :
    Summary, CwPwmMsb = \
        Command.ReadPadCwPwmVoltageMsb8To15(0)
    return Summary, int(CwPwmMsb)

def WritePadCapabilityRegister(PadCapabilityRegisterObj) :
    return Command.WritePadCapabilityRegister(PadCapabilityRegisterObj)

def ReadPadCapabilityRegister() :
    Summary, PadCapabilityRegisterObj = \
        Command.ReadPadCapabilityRegister(PadCapabilityRegister())
    return Summary, PadCapabilityRegisterObj

def WritePadDetailedStatusRegister1(IllumBc2PgFault, IllumBc1PgFault, BuckGp2PgFault, BuckGp1PgFault, BuckGp3PgFault) :
    return Command.WritePadDetailedStatusRegister1(IllumBc2PgFault, IllumBc1PgFault, BuckGp2PgFault, BuckGp1PgFault, BuckGp3PgFault)

def ReadPadDetailedStatusRegister1() :
    Summary, IllumBc2PgFault, IllumBc1PgFault, BuckGp2PgFault, BuckGp1PgFault, BuckGp3PgFault = \
        Command.ReadPadDetailedStatusRegister1(False, False, False, False, False)
    return Summary, bool(IllumBc2PgFault), bool(IllumBc1PgFault), bool(BuckGp2PgFault), bool(BuckGp1PgFault), bool(BuckGp3PgFault)

def WritePadDetailedStatusRegister2(IllumBc2OvFault, IllumBc1OvFault, BuckGp2OvFault, BuckGp1OvFault, BuckGp3OvFault) :
    return Command.WritePadDetailedStatusRegister2(IllumBc2OvFault, IllumBc1OvFault, BuckGp2OvFault, BuckGp1OvFault, BuckGp3OvFault)

def ReadPadDetailedStatusRegister2() :
    Summary, IllumBc2OvFault, IllumBc1OvFault, BuckGp2OvFault, BuckGp1OvFault, BuckGp3OvFault = \
        Command.ReadPadDetailedStatusRegister2(False, False, False, False, False)
    return Summary, bool(IllumBc2OvFault), bool(IllumBc1OvFault), bool(BuckGp2OvFault), bool(BuckGp1OvFault), bool(BuckGp3OvFault)

def WritePadDetailedStatusRegister3(Gp2OrDmd2PgFault, Gp1OrDmd1PgFault, BuckDmd2PgFault, BuckDmd1PgFault, DmdPgFault) :
    return Command.WritePadDetailedStatusRegister3(Gp2OrDmd2PgFault, Gp1OrDmd1PgFault, BuckDmd2PgFault, BuckDmd1PgFault, DmdPgFault)

def ReadPadDetailedStatusRegister3() :
    Summary, Gp2OrDmd2PgFault, Gp1OrDmd1PgFault, BuckDmd2PgFault, BuckDmd1PgFault, DmdPgFault = \
        Command.ReadPadDetailedStatusRegister3(False, False, False, False, False)
    return Summary, bool(Gp2OrDmd2PgFault), bool(Gp1OrDmd1PgFault), bool(BuckDmd2PgFault), bool(BuckDmd1PgFault), bool(DmdPgFault)

def WritePadDetailedStatusRegister4(Gp2OrDmd2OvFault, Gp1OrDmd1OvFault, BuckDmd2OvFault, BuckDmd1OvFault) :
    return Command.WritePadDetailedStatusRegister4(Gp2OrDmd2OvFault, Gp1OrDmd1OvFault, BuckDmd2OvFault, BuckDmd1OvFault)

def ReadPadDetailedStatusRegister4() :
    Summary, Gp2OrDmd2OvFault, Gp1OrDmd1OvFault, BuckDmd2OvFault, BuckDmd1OvFault = \
        Command.ReadPadDetailedStatusRegister4(False, False, False, False)
    return Summary, bool(Gp2OrDmd2OvFault), bool(Gp1OrDmd1OvFault), bool(BuckDmd2OvFault), bool(BuckDmd1OvFault)

def WritePadChipIdExtension(ChipIdExtension) :
    return Command.WritePadChipIdExtension(ChipIdExtension)

def ReadPadChipIdExtension() :
    Summary, ChipIdExtension = \
        Command.ReadPadChipIdExtension(0)
    return Summary, int(ChipIdExtension)

def WritePadUserPassword(UserPassword) :
    return Command.WritePadUserPassword(UserPassword)

def ReadPadUserPassword() :
    Summary, UserPassword = \
        Command.ReadPadUserPassword(0)
    return Summary, int(UserPassword)

def WritePadUserProtectionRegister(ProtectUserReg, DirectMode) :
    return Command.WritePadUserProtectionRegister(ProtectUserReg, DirectMode)

def ReadPadUserProtectionRegister() :
    Summary, ProtectUserReg, DirectMode = \
        Command.ReadPadUserProtectionRegister(False, False)
    return Summary, bool(ProtectUserReg), bool(DirectMode)

def WritePadUserEepromRegister1(UserEepromReg1) :
    return Command.WritePadUserEepromRegister1(UserEepromReg1)

def ReadPadUserEepromRegister1() :
    Summary, UserEepromReg1 = \
        Command.ReadPadUserEepromRegister1(0)
    return Summary, int(UserEepromReg1)

def WritePadUserEepromRegister2(UserEepromReg2) :
    return Command.WritePadUserEepromRegister2(UserEepromReg2)

def ReadPadUserEepromRegister2() :
    Summary, UserEepromReg2 = \
        Command.ReadPadUserEepromRegister2(0)
    return Summary, int(UserEepromReg2)

def WritePadUserEepromRegister3(UserEepromReg3) :
    return Command.WritePadUserEepromRegister3(UserEepromReg3)

def ReadPadUserEepromRegister3() :
    Summary, UserEepromReg3 = \
        Command.ReadPadUserEepromRegister3(0)
    return Summary, int(UserEepromReg3)

def WritePadUserEepromRegister4(UserEepromReg4) :
    return Command.WritePadUserEepromRegister4(UserEepromReg4)

def ReadPadUserEepromRegister4() :
    Summary, UserEepromReg4 = \
        Command.ReadPadUserEepromRegister4(0)
    return Summary, int(UserEepromReg4)

def WritePadUserEepromRegister5(UserEepromReg5) :
    return Command.WritePadUserEepromRegister5(UserEepromReg5)

def ReadPadUserEepromRegister5() :
    Summary, UserEepromReg5 = \
        Command.ReadPadUserEepromRegister5(0)
    return Summary, int(UserEepromReg5)

def WritePadUserEepromRegister6(UserEepromReg6) :
    return Command.WritePadUserEepromRegister6(UserEepromReg6)

def ReadPadUserEepromRegister6() :
    Summary, UserEepromReg6 = \
        Command.ReadPadUserEepromRegister6(0)
    return Summary, int(UserEepromReg6)

def WriteDmdModeRegister(DmdModeRegisterObj) :
    return Command.WriteDmdModeRegister(DmdModeRegisterObj)

def ReadDmdModeRegister() :
    Summary, DmdModeRegisterObj = \
        Command.ReadDmdModeRegister(DmdModeRegister())
    return Summary, DmdModeRegisterObj

def WriteDmdIrwTimingRegister(IrwTsVcc2Delay, IrwTrplDelay, IrwToffsetDelay, IrwThVcc2Delay) :
    return Command.WriteDmdIrwTimingRegister(IrwTsVcc2Delay, IrwTrplDelay, IrwToffsetDelay, IrwThVcc2Delay)

def ReadDmdIrwTimingRegister() :
    Summary, IrwTsVcc2Delay, IrwTrplDelay, IrwToffsetDelay, IrwThVcc2Delay = \
        Command.ReadDmdIrwTimingRegister(0, 0, 0, 0)
    return Summary, int(IrwTsVcc2Delay), int(IrwTrplDelay), int(IrwToffsetDelay), int(IrwThVcc2Delay)

def WriteDmdTestRegister(DmdTestRegisterObj) :
    return Command.WriteDmdTestRegister(DmdTestRegisterObj)

def ReadDmdTestRegister() :
    Summary, DmdTestRegisterObj = \
        Command.ReadDmdTestRegister(DmdTestRegister())
    return Summary, DmdTestRegisterObj

def WriteDmdErrorStatusRegister(HssiPktError, LsifPktError, LsifParityError, MpsTimeoutMonitor) :
    return Command.WriteDmdErrorStatusRegister(HssiPktError, LsifPktError, LsifParityError, MpsTimeoutMonitor)

def ReadDmdErrorStatusRegister() :
    Summary, DmdErrorStatusRegisterObj = \
        Command.ReadDmdErrorStatusRegister(DmdErrorStatusRegister())
    return Summary, DmdErrorStatusRegisterObj

def WriteDmdHssiConfig1Register(DmdHssiConfig1RegisterObj) :
    return Command.WriteDmdHssiConfig1Register(DmdHssiConfig1RegisterObj)

def ReadDmdHssiConfig1Register() :
    Summary, DmdHssiConfig1RegisterObj = \
        Command.ReadDmdHssiConfig1Register(DmdHssiConfig1Register())
    return Summary, DmdHssiConfig1RegisterObj

def WriteDmdHssiConfig2Register(DmdHssiConfig2RegisterObj) :
    return Command.WriteDmdHssiConfig2Register(DmdHssiConfig2RegisterObj)

def ReadDmdHssiConfig2Register() :
    Summary, DmdHssiConfig2RegisterObj = \
        Command.ReadDmdHssiConfig2Register(DmdHssiConfig2Register())
    return Summary, DmdHssiConfig2RegisterObj

def WriteDmdHssiLaneEnable0Register(DmdHssiLaneEnable0RegisterObj) :
    return Command.WriteDmdHssiLaneEnable0Register(DmdHssiLaneEnable0RegisterObj)

def ReadDmdHssiLaneEnable0Register() :
    Summary, DmdHssiLaneEnable0RegisterObj = \
        Command.ReadDmdHssiLaneEnable0Register(DmdHssiLaneEnable0Register())
    return Summary, DmdHssiLaneEnable0RegisterObj

def WriteDmdHssiLaneEnable1Register(DmdHssiLaneEnable1RegisterObj) :
    return Command.WriteDmdHssiLaneEnable1Register(DmdHssiLaneEnable1RegisterObj)

def ReadDmdHssiLaneEnable1Register() :
    Summary, DmdHssiLaneEnable1RegisterObj = \
        Command.ReadDmdHssiLaneEnable1Register(DmdHssiLaneEnable1Register())
    return Summary, DmdHssiLaneEnable1RegisterObj

def WriteDmdHssiLaneEnable2Register(DmdHssiLaneEnable2RegisterObj) :
    return Command.WriteDmdHssiLaneEnable2Register(DmdHssiLaneEnable2RegisterObj)

def ReadDmdHssiLaneEnable2Register() :
    Summary, DmdHssiLaneEnable2RegisterObj = \
        Command.ReadDmdHssiLaneEnable2Register(DmdHssiLaneEnable2Register())
    return Summary, DmdHssiLaneEnable2RegisterObj

def WriteDmdHssiLaneEnable3Register(DmdHssiLaneEnable3RegisterObj) :
    return Command.WriteDmdHssiLaneEnable3Register(DmdHssiLaneEnable3RegisterObj)

def ReadDmdHssiLaneEnable3Register() :
    Summary, DmdHssiLaneEnable3RegisterObj = \
        Command.ReadDmdHssiLaneEnable3Register(DmdHssiLaneEnable3Register())
    return Summary, DmdHssiLaneEnable3RegisterObj

def WriteDmdHssiMacroEnableRegister(DmdHssiMacroEnableRegisterObj) :
    return Command.WriteDmdHssiMacroEnableRegister(DmdHssiMacroEnableRegisterObj)

def ReadDmdHssiMacroEnableRegister() :
    Summary, DmdHssiMacroEnableRegisterObj = \
        Command.ReadDmdHssiMacroEnableRegister(DmdHssiMacroEnableRegister())
    return Summary, DmdHssiMacroEnableRegisterObj

def WriteDmdAmuxDmuxSelectRegister(AmuxSel, DmuxSel, MacroSel, CoreAmuxSel, CoreDmuxSel) :
    return Command.WriteDmdAmuxDmuxSelectRegister(AmuxSel, DmuxSel, MacroSel, CoreAmuxSel, CoreDmuxSel)

def ReadDmdAmuxDmuxSelectRegister() :
    Summary, AmuxSel, DmuxSel, MacroSel, CoreAmuxSel, CoreDmuxSel = \
        Command.ReadDmdAmuxDmuxSelectRegister(0, 0, 0, False, False)
    return Summary, int(AmuxSel), int(DmuxSel), int(MacroSel), bool(CoreAmuxSel), bool(CoreDmuxSel)

def WriteDmdLsRwTestRegister(LsRwTest) :
    return Command.WriteDmdLsRwTestRegister(LsRwTest)

def ReadDmdLsRwTestRegister() :
    Summary, LsRwTest = \
        Command.ReadDmdLsRwTestRegister(0)
    return Summary, int(LsRwTest)

def WriteDmdDriveControlRegister(WlDriver20PercentEnable, WlDriver40PercentEnable, BlDriverEnable, ProgrammableTimingEnable, BlockClearTransistorsEnable) :
    return Command.WriteDmdDriveControlRegister(WlDriver20PercentEnable, WlDriver40PercentEnable, BlDriverEnable, ProgrammableTimingEnable, BlockClearTransistorsEnable)

def ReadDmdDriveControlRegister() :
    Summary, WlDriver20PercentEnable, WlDriver40PercentEnable, BlDriverEnable, ProgrammableTimingEnable, BlockClearTransistorsEnable = \
        Command.ReadDmdDriveControlRegister(False, False, 0, False, False)
    return Summary, bool(WlDriver20PercentEnable), bool(WlDriver40PercentEnable), int(BlDriverEnable), bool(ProgrammableTimingEnable), bool(BlockClearTransistorsEnable)

def WriteDmdVarTimingRegister(DmdVarTimingRegisterObj) :
    return Command.WriteDmdVarTimingRegister(DmdVarTimingRegisterObj)

def ReadDmdVarTimingRegister() :
    Summary, DmdVarTimingRegisterObj = \
        Command.ReadDmdVarTimingRegister(DmdVarTimingRegister())
    return Summary, DmdVarTimingRegisterObj

def ReadDmdProgFuseGroup1Register() :
    Summary, ProgrammableFuseByte0, ProgrammableFuseByte1, ProgrammableFuseByte2, ProgrammableFuseByte3 = \
        Command.ReadDmdProgFuseGroup1Register(0, 0, 0, 0)
    return Summary, int(ProgrammableFuseByte0), int(ProgrammableFuseByte1), int(ProgrammableFuseByte2), int(ProgrammableFuseByte3)

def ReadDmdProgFuseGroup2Register() :
    Summary, ProgrammableFuseByte0, ProgrammableFuseByte1, ProgrammableFuseByte2, ProgrammableFuseByte3 = \
        Command.ReadDmdProgFuseGroup2Register(0, 0, 0, 0)
    return Summary, int(ProgrammableFuseByte0), int(ProgrammableFuseByte1), int(ProgrammableFuseByte2), int(ProgrammableFuseByte3)

def ReadDmdProgFuseGroup3Register() :
    Summary, ProgrammableFuseByte0, ProgrammableFuseByte1, ProgrammableFuseByte2, ProgrammableFuseByte3 = \
        Command.ReadDmdProgFuseGroup3Register(0, 0, 0, 0)
    return Summary, int(ProgrammableFuseByte0), int(ProgrammableFuseByte1), int(ProgrammableFuseByte2), int(ProgrammableFuseByte3)

def ReadDmdProgFuseGroup4Register() :
    Summary, ProgrammableFuseByte0, ProgrammableFuseByte1, ProgrammableFuseByte2, ProgrammableFuseByte3 = \
        Command.ReadDmdProgFuseGroup4Register(0, 0, 0, 0)
    return Summary, int(ProgrammableFuseByte0), int(ProgrammableFuseByte1), int(ProgrammableFuseByte2), int(ProgrammableFuseByte3)

def ReadDmdIdRegister() :
    Summary, DmdIdByte0, DmdIdByte1, DmdIdByte2, DmdIdByte3 = \
        Command.ReadDmdIdRegister(0, 0, 0, 0)
    return Summary, int(DmdIdByte0), int(DmdIdByte1), int(DmdIdByte2), int(DmdIdByte3)

def ReadColorMode() :
    Summary, ByteMode = \
        Command.ReadColorMode(0)
    return Summary, int(ByteMode)

def ReadLaneEnable() :
    Summary, LaneEnableObj = \
        Command.ReadLaneEnable(LaneEnable())
    return Summary, LaneEnableObj

def ReadPhyReset() :
    Summary, PhyReset = \
        Command.ReadPhyReset(False)
    return Summary, bool(PhyReset)

def ReadPhyEnable() :
    Summary, PhyEnable = \
        Command.ReadPhyEnable(False)
    return Summary, bool(PhyEnable)

def ReadHotPlugDetectControl() :
    Summary, HtpdnDeAssert = \
        Command.ReadHotPlugDetectControl(False)
    return Summary, bool(HtpdnDeAssert)

def ReadInterruptEnable() :
    Summary, InterruptEnableObj = \
        Command.ReadInterruptEnable(InterruptEnable())
    return Summary, InterruptEnableObj

def ReadInterruptStatus() :
    Summary, InterruptStatusObj = \
        Command.ReadInterruptStatus(InterruptStatus())
    return Summary, InterruptStatusObj

def ReadInterruptClear() :
    Summary, InterruptClearObj = \
        Command.ReadInterruptClear(InterruptClear())
    return Summary, InterruptClearObj

def ReadLockMonitor() :
    Summary, BitLocked, ByteLocked, DataLocked = \
        Command.ReadLockMonitor(False, False, False)
    return Summary, bool(BitLocked), bool(ByteLocked), bool(DataLocked)

def ReadBitLockMonitorLan0ToLane7() :
    Summary, BitLockMonitorLan0ToLane7Obj = \
        Command.ReadBitLockMonitorLan0ToLane7(BitLockMonitorLan0ToLane7())
    return Summary, BitLockMonitorLan0ToLane7Obj

def ReadBitLockMonitorLane8ToLane15() :
    Summary, BitLockMonitorLane8ToLane15Obj = \
        Command.ReadBitLockMonitorLane8ToLane15(BitLockMonitorLane8ToLane15())
    return Summary, BitLockMonitorLane8ToLane15Obj

def ReadByteLockMonitorLane0ToLane7() :
    Summary, ByteLockMonitorLane0ToLane7Obj = \
        Command.ReadByteLockMonitorLane0ToLane7(ByteLockMonitorLane0ToLane7())
    return Summary, ByteLockMonitorLane0ToLane7Obj

def ReadByteLockMonitorLane8ToLane15() :
    Summary, ByteLockMonitorLane8ToLane15Obj = \
        Command.ReadByteLockMonitorLane8ToLane15(ByteLockMonitorLane8ToLane15())
    return Summary, ByteLockMonitorLane8ToLane15Obj

def ReadDataLockMonitorLane0ToLane7() :
    Summary, DataLockMonitorLane0ToLane7Obj = \
        Command.ReadDataLockMonitorLane0ToLane7(DataLockMonitorLane0ToLane7())
    return Summary, DataLockMonitorLane0ToLane7Obj

def ReadDataLockMonitorLane8ToLane15() :
    Summary, DataLockMonitorLane8ToLane15Obj = \
        Command.ReadDataLockMonitorLane8ToLane15(DataLockMonitorLane8ToLane15())
    return Summary, DataLockMonitorLane8ToLane15Obj

def ReadVideoOutputEnableLane0ToLane7() :
    Summary, VideoOutputEnableLane0ToLane7Obj = \
        Command.ReadVideoOutputEnableLane0ToLane7(VideoOutputEnableLane0ToLane7())
    return Summary, VideoOutputEnableLane0ToLane7Obj

def ReadVideoOutputEnableLane8ToLane15() :
    Summary, VideoOutputEnableLane8ToLane15Obj = \
        Command.ReadVideoOutputEnableLane8ToLane15(VideoOutputEnableLane8ToLane15())
    return Summary, VideoOutputEnableLane8ToLane15Obj

def ReadComIntmode() :
    Summary, ComIntmode = \
        Command.ReadComIntmode(False)
    return Summary, bool(ComIntmode)

def ReadComModeLow() :
    Summary, ComModeLow = \
        Command.ReadComModeLow(0)
    return Summary, int(ComModeLow)

def ReadComModeHigh() :
    Summary, ComModeHigh = \
        Command.ReadComModeHigh(0)
    return Summary, int(ComModeHigh)

def ReadRxmBand0EqTrim() :
    Summary, RxmBand0EqTrim = \
        Command.ReadRxmBand0EqTrim(0)
    return Summary, int(RxmBand0EqTrim)

def ReadRxmBand1EqTrim() :
    Summary, RxmBand1EqTrim = \
        Command.ReadRxmBand1EqTrim(0)
    return Summary, int(RxmBand1EqTrim)

def ReadRxmBand2EqTrim() :
    Summary, RxmBand2EqTrim = \
        Command.ReadRxmBand2EqTrim(0)
    return Summary, int(RxmBand2EqTrim)

def ReadRxmBand3EqTrim() :
    Summary, RxmBand3EqTrim = \
        Command.ReadRxmBand3EqTrim(0)
    return Summary, int(RxmBand3EqTrim)

def WriteXprFixedOutputEnable(ChannelNum, FixedOutputEnable) :
    return Command.WriteXprFixedOutputEnable(ChannelNum, FixedOutputEnable)

def ReadXprFixedOutputEnable(ChannelNum) :
    Summary, FixedOutputEnable = \
        Command.ReadXprFixedOutputEnable(ChannelNum, False)
    return Summary, bool(FixedOutputEnable)

def WriteXprDacGain(ChannelNum, DacGain) :
    return Command.WriteXprDacGain(ChannelNum, DacGain)

def ReadXprDacGain(ChannelNum) :
    Summary, DacGain = \
        Command.ReadXprDacGain(ChannelNum, 0)
    return Summary, float(DacGain)

def WriteXprSubframeDelay(ChannelNum, SubframeDelay) :
    return Command.WriteXprSubframeDelay(ChannelNum, SubframeDelay)

def ReadXprSubframeDelay(ChannelNum) :
    Summary, SubframeDelay = \
        Command.ReadXprSubframeDelay(ChannelNum, 0)
    return Summary, int(SubframeDelay)

def ReadXprActuatorType() :
    Summary, ActuatorType = \
        Command.ReadXprActuatorType(0)
    return Summary, int(ActuatorType)

def WriteXprOutputEnable(ChannelNum, OutputEnable) :
    return Command.WriteXprOutputEnable(ChannelNum, OutputEnable)

def ReadXprOutputEnable(ChannelNum) :
    Summary, OutputEnable = \
        Command.ReadXprOutputEnable(ChannelNum, False)
    return Summary, bool(OutputEnable)

def WriteXprClockWidth(ChannelNum, ClockWidth) :
    return Command.WriteXprClockWidth(ChannelNum, ClockWidth)

def ReadXprClockWidth(ChannelNum) :
    Summary, ClockWidth = \
        Command.ReadXprClockWidth(ChannelNum, 0)
    return Summary, int(ClockWidth)

def WriteXprDacOffset(ChannelNum, DacOffset) :
    return Command.WriteXprDacOffset(ChannelNum, DacOffset)

def ReadXprDacOffset(ChannelNum) :
    Summary, DacOffset = \
        Command.ReadXprDacOffset(ChannelNum, 0)
    return Summary, int(DacOffset)

def WriteXprNumberOfSegments(ChannelNum, NumberOfSegments) :
    return Command.WriteXprNumberOfSegments(ChannelNum, NumberOfSegments)

def ReadXprNumberOfSegments(ChannelNum) :
    Summary, NumberOfSegments = \
        Command.ReadXprNumberOfSegments(ChannelNum, 0)
    return Summary, int(NumberOfSegments)

def WriteXprSegmentLength(ChannelNum, SegmentLength) :
    return Command.WriteXprSegmentLength(ChannelNum, SegmentLength)

def ReadXprSegmentLength(ChannelNum) :
    Summary, SegmentLength = \
        Command.ReadXprSegmentLength(ChannelNum, 0)
    return Summary, int(SegmentLength)

def WriteXprInvertPwmA(ChannelNum, InvertPwmA) :
    return Command.WriteXprInvertPwmA(ChannelNum, InvertPwmA)

def ReadXprInvertPwmA(ChannelNum) :
    Summary, InvertPwmA = \
        Command.ReadXprInvertPwmA(ChannelNum, False)
    return Summary, bool(InvertPwmA)

def WriteXprInvertPwmB(ChannelNum, InvertPwmB) :
    return Command.WriteXprInvertPwmB(ChannelNum, InvertPwmB)

def ReadXprInvertPwmB(ChannelNum) :
    Summary, InvertPwmB = \
        Command.ReadXprInvertPwmB(ChannelNum, False)
    return Summary, bool(InvertPwmB)

def WriteXprSubframeFilterValue(ChannelNum, SubframeFilterValue) :
    return Command.WriteXprSubframeFilterValue(ChannelNum, SubframeFilterValue)

def ReadXprSubframeFilterValue(ChannelNum) :
    Summary, SubframeFilterValue = \
        Command.ReadXprSubframeFilterValue(ChannelNum, 0)
    return Summary, int(SubframeFilterValue)

def WriteXprSubframeWatchDog(ChannelNum, SubframeWatchDog) :
    return Command.WriteXprSubframeWatchDog(ChannelNum, SubframeWatchDog)

def ReadXprSubframeWatchDog(ChannelNum) :
    Summary, SubframeWatchDog = \
        Command.ReadXprSubframeWatchDog(ChannelNum, 0)
    return Summary, int(SubframeWatchDog)

def WriteXprFixedOutputValue(ChannelNum, FixedOutputValue) :
    return Command.WriteXprFixedOutputValue(ChannelNum, FixedOutputValue)

def ReadXprFixedOutputValue(ChannelNum) :
    Summary, FixedOutputValue = \
        Command.ReadXprFixedOutputValue(ChannelNum, 0)
    return Summary, int(FixedOutputValue)

