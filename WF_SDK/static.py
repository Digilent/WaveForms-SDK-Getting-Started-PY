""" STATIC I/O CONTROL FUNCTIONS: set_mode, get_state, set_state, set_current, set_pull, close """

import ctypes                     # import the C compatible data types
from sys import platform, path    # this is needed to check the OS type and get the PATH
from os import sep                # OS specific file path separators

# load the dynamic library, get constants path (the path is OS specific)
if platform.startswith("win"):
    # on Windows
    dwf = ctypes.cdll.dwf
    constants_path = "C:" + sep + "Program Files (x86)" + sep + "Digilent" + sep + "WaveFormsSDK" + sep + "samples" + sep + "py"
elif platform.startswith("darwin"):
    # on macOS
    lib_path = sep + "Library" + sep + "Frameworks" + sep + "dwf.framework" + sep + "dwf"
    dwf = ctypes.cdll.LoadLibrary(lib_path)
    constants_path = sep + "Applications" + sep + "WaveForms.app" + sep + "Contents" + sep + "Resources" + sep + "SDK" + sep + "samples" + sep + "py"
else:
    # on Linux
    dwf = ctypes.cdll.LoadLibrary("libdwf.so")
    constants_path = sep + "usr" + sep + "share" + sep + "digilent" + sep + "waveforms" + sep + "samples" + sep + "py"

# import constants
path.append(constants_path)
import dwfconstants as constants

"""-----------------------------------------------------------------------"""

class state:
    """ stores the state of the instrument """
    state = [None for _ in range(16)]
    input = [True for _ in range(16)]
    output = [False for _ in range(16)]
    pull = [None for _ in range(16)]
    current = None

"""-----------------------------------------------------------------------"""

def set_mode(device_data, channel, output):
    """
        set a DIO line as input, or as output

        parameters: - device data
                    - selected DIO channel number
                    - True means output, False means input
    """
    # load current state of the output enable buffer
    mask = ctypes.c_uint16()
    dwf.FDwfDigitalIOOutputEnableGet(device_data.handle, ctypes.byref(mask))
    mask = mask.value
    
    # set bit in mask
    if output == True:
        mask |= __rotate_left__(1, channel)
    else:
        mask &= __rotate_left__(0xFFFE, channel)
    
    # set the pin to output
    dwf.FDwfDigitalIOOutputEnableSet(device_data.handle, ctypes.c_int(mask))
    state.input[channel] = not output
    state.output[channel] = output
    if not output:
        state.state[channel] = None
    return

"""-----------------------------------------------------------------------"""

def get_state(device_data, channel):
    """
        get the state of a DIO line

        parameters: - device data
                    - selected DIO channel number

        returns:    - True if the channel is HIGH, or False, if the channel is LOW
    """
    # load internal buffer with current state of the pins
    dwf.FDwfDigitalIOStatus(device_data.handle)
    
    # get the current state of the pins
    data = ctypes.c_uint32()  # variable for this current state
    dwf.FDwfDigitalIOInputStatus(device_data.handle, ctypes.byref(data))
    data = data.value
    
    # check the required bit
    if data & (1 << channel) != 0:
        value = True
    else:
        value = False
    return value

"""-----------------------------------------------------------------------"""

def set_state(device_data, channel, value):
    """
        set a DIO line as High, or Low

        parameters: - device data
                    - selected DIO channel number
                    - True means HIGH, False means LOW
    """
    # load current state of the output state buffer
    mask = ctypes.c_uint16()
    dwf.FDwfDigitalIOOutputGet(device_data.handle, ctypes.byref(mask))
    mask = mask.value
    
    # set bit in mask
    if value == True:
        mask |= __rotate_left__(1, channel)
    else:
        mask &= __rotate_left__(0xFFFE, channel)
    
    # set the pin state
    dwf.FDwfDigitalIOOutputSet(device_data.handle, ctypes.c_int(mask))
    state.state[channel] = value
    return

"""-----------------------------------------------------------------------"""

def set_current(device_data, current):
    """
        limit the output current of the DIO lines

        parameters: - device data
                    - current limit in mA: possible values are 2, 4, 6, 8, 12 and 16mA
    """
    # clamp current
    current = max(2, min(16, current))

    # round
    current = round(current)

    # discard odd values
    if current % 2 != 0:
        current -= 1

    # discard unavailable even values
    if current == 10:
        current = 12
    elif current == 14:
        current = 16

    # set limit  
    dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(0), ctypes.c_int(4), ctypes.c_double(current))
    state.current = current
    return

"""-----------------------------------------------------------------------"""

def set_pull(device_data, channel, direction):
    """
        pull a DIO line up, or down

        parameters: - device data
                    - selected DIO channel number between 0-15
                    - direction: True means HIGH, False means LOW, None means idle
    """
    
    state.pull[channel] = direction
    # encode direction
    if direction == True:
        direction = ctypes.c_double(1)
    elif direction == False:
        direction = ctypes.c_double(0)
    else:
        direction = ctypes.c_double(0.5)

    # get pull enable mask
    mask = ctypes.c_uint16()
    dwf.FDwfAnalogIOChannelNodeGet(device_data.handle, ctypes.c_int(0), ctypes.c_int(2), ctypes.byref(mask))
    mask = mask.value
    
    # set bit in mask
    if direction.value == 0.5:
        mask |= __rotate_left__(1, channel)
    else:
        mask &= __rotate_left__(0xFFFE, channel)
    
    # set pull enable mask
    dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(0), ctypes.c_int(2), ctypes.c_int(mask))
    
    # set direction if necessary
    if direction.value != 0.5:
        # get direction mask
        mask = ctypes.c_uint16()
        dwf.FDwfAnalogIOChannelNodeGet(device_data.handle, ctypes.c_int(0), ctypes.c_int(3), ctypes.byref(mask))
        mask = mask.value
    
        # set bit in mask
        if direction.value == 1.0:
            mask |= __rotate_left__(1, channel)
        else:
            mask &= __rotate_left__(0xFFFE, channel)

        # set direction mask
        dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(0), ctypes.c_int(3), ctypes.c_int(mask))

    return

"""-----------------------------------------------------------------------"""

def close(device_data):
    """
        reset the instrument
    """
    dwf.FDwfDigitalIOReset(device_data.handle)
    state.state = [None for _ in range(16)]
    state.input = [True for _ in range(16)]
    state.output = [False for _ in range(16)]
    state.pull = [None for _ in range(16)]
    state.current = None
    return

"""-----------------------------------------------------------------------"""

def __rotate_left__(number, position, size=16):
    """
        rotate left a number bitwise
    """
    return (number << position) | (number >> (size - position))
