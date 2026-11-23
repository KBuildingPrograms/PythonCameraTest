import sys
import clr

if __name__ == '__main__' or __name__ == 'registers' or __name__ == 'dlpc754x.registers':
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
clr.AddReference('DLPComposer.Registers')
from System import *
from DLPComposer.Registers.DLPC754x import *
