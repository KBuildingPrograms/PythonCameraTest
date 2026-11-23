import sys
import clr

if __name__ == '__main__' or __name__ == 'connection' or __name__ == 'dlpc754x.connection':
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
__doc__ = "DESCRIPTION: DLPC754x connection library (DO NOT MODIFY THIS FILE!)"

clr.AddReference('DLPComposer.IO')
from DLPComposer.IO.DLPC754x import WinUSBCommandInterface, I2CCommandInterface

clr.AddReference('DLPComposer.Commands.DLPC754x')
from DLPComposer.Commands.DLPC754x import *

clr.AddReference('DLPComposer.IO.Communications')
from DLPComposer.IO.Communications import DLPC754xCommunicationManager as CommunicationManager

clr.AddReference('DLPComposer.Registers')
from DLPComposer.IO import RegisterBase


def _connect(comm_interface):
    comm_interface.CommandHeader.InsertByteLength = True
    comm_interface.CommandHeader.InsertChecksum = False
    comm_interface.CommandHeader.RequestACK = True
    comm_interface.Timeout = 2000

    comm_interface.Connect()
    Command.CommInterface = comm_interface

    if RegisterBase.CommunicationManager == None:
        RegisterBase.CommunicationManager = CommunicationManager()

    return comm_interface.IsConnected


def _disconnect():
    if Command.CommInterface != None:
        Command.CommInterface.Disconnect()
        Command.CommInterface = None

def _is_connected():
    if Command.CommInterface != None:
        return True
    else:
        return False

def usb_connect(vid=0x451, pid=0x7540):
    """
    Description: establishes USB connection to a 7540 system
    """
    _disconnect()
    available_usb_interfaces = WinUSBCommandInterface.GetAvailableInterfaces()
    for interface in available_usb_interfaces:
        if interface.VID == vid and interface.PID == pid:
            return _connect(interface)
    return False

def usb_is_connected():
    """
    Description: returns true if a 7540 is currently connected to the PC
    """
    return _is_connected()

def usb_disconnect():
    """
    Description: terminates the USB connection between a 7540 system and a PC
    """
    _disconnect()

def i2c_connect(dev_instance=0):
    """
    Description: establishes i2c connection between a 7540 system and a PC
    """
    _disconnect()
    available_i2c_interfaces = I2CCommandInterface.GetAvailableInterfaces()
    if len(available_i2c_interfaces) < (dev_instance + 1):
        return False

    i2c_interface = available_i2c_interfaces[dev_instance]
    return _connect(i2c_interface)


__all__ = ['usb_connect', 'usb_disconnect', 'usb_is_connected', 'i2c_connect']
