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
    channel = -1
    count = 0
    class nodes :
        current = -1
        pull_enable = -1
        pull_direction = -1
        pull_weak = -1

"""-----------------------------------------------------------------------"""

class pull:
    """ digital pin pull directions """
    down = 0
    idle = 0.5
    up = 1

"""-----------------------------------------------------------------------"""

def set_mode(device_data, channel, output):
    """
        set a DIO line as input, or as output

        parameters: - device data
                    - selected DIO channel number
                    - True means output, False means input
    """
    if device_data.name == "Digital Discovery":
        channel = channel - 24

    # count the DIO channels
    state.count = min(device_data.digital.input.channel_count, device_data.digital.output.channel_count)

    # load current state of the output enable buffer
    mask = ctypes.c_uint16()
    dwf.FDwfDigitalIOOutputEnableGet(device_data.handle, ctypes.byref(mask))
    mask = mask.value
    
    # set bit in mask
    if output == True:
        mask |= __rotate_left__(1, channel, state.count)
    else:
        bits = pow(2, state.count) - 2
        mask &= __rotate_left__(bits, channel, state.count)
    
    # set the pin to output
    dwf.FDwfDigitalIOOutputEnableSet(device_data.handle, ctypes.c_int(mask))
    return

"""-----------------------------------------------------------------------"""

def get_state(device_data, channel):
    """
        get the state of a DIO line

        parameters: - device data
                    - selected DIO channel number

        returns:    - True if the channel is HIGH, or False, if the channel is LOW
    """
    if device_data.name == "Digital Discovery":
        channel = channel - 24

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
        set a DIO line as input, or as output

        parameters: - device data
                    - selected DIO channel number
                    - True means HIGH, False means LOW
    """
    if device_data.name == "Digital Discovery":
        channel = channel - 24

    # count the DIO channels
    state.count = min(device_data.digital.input.channel_count, device_data.digital.output.channel_count)

    # load current state of the output state buffer
    mask = ctypes.c_uint16()
    dwf.FDwfDigitalIOOutputGet(device_data.handle, ctypes.byref(mask))
    
    # set bit in mask
    if value == True:
        mask |= __rotate_left__(1, channel, state.count)
    else:
        bits = pow(2, state.count) - 2
        mask &= __rotate_left__(bits, channel, state.count)
    
    # set the pin state
    dwf.FDwfDigitalIOOutputSet(device_data.handle, ctypes.c_int(mask))
    return

"""-----------------------------------------------------------------------"""

def set_current(device_data, current):
    """
        limit the output current of the DIO lines

        parameters: - device data
                    - current limit in mA: possible values are 2, 4, 6, 8, 12 and 16mA
    """
    # search for the digital voltage channel
    for channel_index in range(device_data.analog.IO.channel_count):
        if device_data.analog.IO.channel_label[channel_index] == "VDD":
            state.channel = channel_index
            break

    # search for the drive node
    if state.channel >= 0:
        for node_index in range(device_data.analog.IO.node_count[state.channel]):
            if device_data.analog.IO.node_name[state.channel][node_index] == "Drive":
                state.nodes.current = node_index
                break

    # set limit
    if state.channel >= 0 and state.nodes.current >= 0:
        current = max(min(current, device_data.analog.IO.max_set_range[state.channel][state.nodes.current]), device_data.analog.IO.min_set_range[state.channel][state.nodes.current])
        dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, state.channel, state.nodes.current, ctypes.c_double(current))
    return

"""-----------------------------------------------------------------------"""

def set_pull(device_data, channel, direction):
    """
        pull a DIO line up, or down

        parameters: - device data
                    - selected DIO channel number
                    - direction: pull.up, pull.idle, or pull.down
    """
    if device_data.name == "Digital Discovery":
        channel = channel - 24
        
    # count the DIO channels
    state.count = min(device_data.digital.input.channel_count, device_data.digital.output.channel_count)

    # search for the digital voltage channel
    for channel_index in range(device_data.analog.IO.channel_count):
        if device_data.analog.IO.channel_label[channel_index] == "VDD":
            state.channel = channel_index
            break

    # search for the pull enable node
    if state.channel >= 0:
        for node_index in range(device_data.analog.IO.node_count[state.channel]):
            if device_data.analog.IO.node_name[state.channel][node_index] == "DIOPE":
                state.nodes.pull_enable = node_index
                break

    # search for the pull direction node
    if state.channel >= 0:
        for node_index in range(device_data.analog.IO.node_count[state.channel]):
            if device_data.analog.IO.node_name[state.channel][node_index] == "DIOPP":
                state.nodes.pull_direction = node_index
                break

    # search for the weak pull node
    if state.channel >= 0:
        for node_index in range(device_data.analog.IO.node_count[state.channel]):
            if device_data.analog.IO.node_name[state.channel][node_index] == "DINPP":
                state.nodes.pull_weak = node_index
                break

    # set pull enable mask
    mask = ctypes.c_uint16()
    dwf.FDwfAnalogIOChannelNodeGet(device_data.handle, state.channel, state.nodes.pull_enable, ctypes.byref(mask))
    bitmask = int(mask)
    if direction == pull.idle:
        bitmask |= __rotate_left__(1, channel, state.count)
    else:
        bits = int(pow(2, state.count) - 2)
        bitmask &= __rotate_left__(bits, channel, state.count)
    dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, state.channel, state.nodes.pull_enable, bitmask)

    # set direction if necessary
    if direction != pull.idle:
        # set direction mask
        mask = ctypes.c_uint16()
        dwf.FDwfAnalogIOChannelNodeGet(device_data.handle, state.channel, state.nodes.pull_direction, ctypes.byref(mask))
        bitmask = int(mask)
        if direction == pull.up:
            bitmask |= __rotate_left__(1, channel, state.count)
        else:
            bits = int(pow(2, state.count) - 2)
            bitmask &= __rotate_left__(bits, channel, state.count)
        dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, state.channel, state.nodes.pull_direction, bitmask)
    return

"""-----------------------------------------------------------------------"""

def close(device_data):
    """
        reset the instrument
    """
    dwf.FDwfDigitalIOReset(device_data.handle)
    return

"""-----------------------------------------------------------------------"""

def __rotate_left__(number, position, size=16):
    """
        rotate left a number bitwise
    """
    return (number << position) | (number >> (size - position))
