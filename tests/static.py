import ctypes                     # import the C compatible data types
import dwfconstants as constants  # import every constant
from sys import platform          # this is needed to check the OS type

# load the dynamic library (the path is OS specific)
if platform.startswith("win"):
    # on Windows
    dwf = ctypes.cdll.dwf
elif platform.startswith("darwin"):
    # on macOS
    dwf = ctypes.cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    # on Linux
    dwf = ctypes.cdll.LoadLibrary("libdwf.so")

"""-----------------------------------------------------------------------"""

def set_mode(device_handle, channel, output):
    """
        set a DIO line as input, or as output

        parameters: - device handle
                    - selected DIO channel number
                    - True means output, False means input
    """
    # load current state of the output enable buffer
    mask = ctypes.c_uint16()
    dwf.FDwfDigitalIOOutputEnableGet(device_handle, ctypes.byref(mask))
    
    # convert mask to list
    mask = list(bin(mask.value)[2:].zfill(16))
    
    # set bit in mask
    if output:
        mask[15 - channel] = "1"
    else:
        mask[15 - channel] = "0"
    
    # convert mask to number
    mask = "".join(element for element in mask)
    mask = int(mask, 2)
    
    # set the pin to output
    dwf.FDwfDigitalIOOutputEnableSet(device_handle, ctypes.c_int(mask))
    return

"""-----------------------------------------------------------------------"""

def get_state(device_handle, channel):
    """
        get the state of a DIO line

        parameters: - device handle
                    - selected DIO channel number

        returns:    - True if the channel is HIGH, or False, if the channel is LOW
    """
    # load internal buffer with current state of the pins
    dwf.FDwfDigitalIOStatus(device_handle)
    
    # get the current state of the pins
    data = ctypes.c_uint32()  # variable for this current state
    dwf.FDwfDigitalIOInputStatus(device_handle, ctypes.byref(data))
    
    # convert the state to a 16 character binary string
    data = list(bin(data.value)[2:].zfill(16))
    
    # check the required bit
    if data[15 - channel] != "0":
        state = True
    else:
        state = False
    return state

"""-----------------------------------------------------------------------"""

def set_state(device_handle, channel, state):
    """
        set a DIO line as input, or as output

        parameters: - device handle
                    - selected DIO channel number
                    - True means HIGH, False means LOW
    """
    # load current state of the output state buffer
    mask = ctypes.c_uint16()
    dwf.FDwfDigitalIOOutputGet(device_handle, ctypes.byref(mask))
    
    # convert mask to list
    mask = list(bin(mask.value)[2:].zfill(16))
    
    # set bit in mask
    if state:
        mask[15 - channel] = "1"
    else:
        mask[15 - channel] = "0"
    
    # convert mask to number
    mask = "".join(element for element in mask)
    mask = int(mask, 2)
    
    # set the pin state
    dwf.FDwfDigitalIOOutputSet(device_handle, ctypes.c_int(mask))
    return

"""-----------------------------------------------------------------------"""

def close(device_handle):
    """
        reset the instrument
    """
    dwf.FDwfDigitalIOReset(device_handle)
    return
