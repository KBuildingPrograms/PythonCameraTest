# Imports
if __name__ == '__main__' or __name__ == 'usb_comms':
    import license_strings as lic
    import dlpc754x.connection as conn
else:
    from ..libs import license_strings as lic
    from .dlpc754x import connection as conn

# Module metadata
__copyright__ = lic.copyright_str
__author__ = lic.author
__status__ = lic.status
__doc__ = "DESCRIPTION: USB comms library"

#--------------------------- Connect to USB ----------------------------#
def Connect_USB():
    """
    Description: tries to connect a 7540 to the host PC, via USB

    Input arguments:
    None

    Output arguments:
    Status: connection success/fail
    """
    Status = conn.usb_connect()

    if not Status:
        print('Connecting USB...failed!')
    else:
        print('Connecting USB...connection established!')
    
    return Status

#--------------------------- Disconnect USB ----------------------------#
def Disconnect_USB():
    """
    Description: tries to disconnect a 7540 to the host PC, via USB

    Input arguments:
    None

    Output arguments:
    None
    """
    conn.usb_disconnect()
    print('Disconnecting USB...')

#---------------------------- Check if USB is connected ------------------------#
def IsConnected_USB():
    """
    Description: checks if a 7540 system is currently connected to the host PC

    Input arguments:
    None

    Output arguments:
    Status: connected/not connected
    """
    return conn.usb_is_connected()
