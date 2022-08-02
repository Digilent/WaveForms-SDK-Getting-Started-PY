""" LOGIC ANALYZER CONTROL FUNCTIONS: open, trigger, record, close """

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

class data:
    """ stores the sampling frequency and the buffer size """
    sampling_frequency = 100e06
    buffer_size = 4096
    max_buffer_size = 0

class state:
    """ stores the state of the instrument """
    on = False
    off = True
    trigger = False

"""-----------------------------------------------------------------------"""

def open(device_data, sampling_frequency=100e06, buffer_size=0):
    """
        initialize the logic analyzer

        parameters: - device data
                    - sampling frequency in Hz, default is 100MHz
                    - buffer size, default is 0 (maximum)
    """
    # set global variables
    data.sampling_frequency = sampling_frequency
    data.max_buffer_size = device_data.digital.input.max_buffer_size

    # get internal clock frequency
    internal_frequency = ctypes.c_double()
    dwf.FDwfDigitalInInternalClockInfo(device_data.handle, ctypes.byref(internal_frequency))
    
    # set clock frequency divider (needed for lower frequency input signals)
    dwf.FDwfDigitalInDividerSet(device_data.handle, ctypes.c_int(int(internal_frequency.value / sampling_frequency)))
    
    # set 16-bit sample format
    dwf.FDwfDigitalInSampleFormatSet(device_data.handle, ctypes.c_int(16))
    
    # set buffer size
    if buffer_size == 0 or buffer_size > data.max_buffer_size:
        buffer_size = data.max_buffer_size
    data.buffer_size = buffer_size
    dwf.FDwfDigitalInBufferSizeSet(device_data.handle, ctypes.c_int(buffer_size))
    
    state.on = True
    state.off = False
    return

"""-----------------------------------------------------------------------"""

def trigger(device_data, enable, channel, position=0, timeout=0, rising_edge=True, length_min=0, length_max=20, count=0):
    """
        set up triggering

        parameters: - device data
                    - enable - True or False to enable, or disable triggering
                    - channel - the selected DIO line number to use as trigger source
                    - buffer size, the default is 4096
                    - position - prefill size, the default is 0
                    - timeout - auto trigger time, the default is 0
                    - rising_edge - set True for rising edge, False for falling edge, the default is rising edge
                    - length_min - trigger sequence minimum time in seconds, the default is 0
                    - length_max - trigger sequence maximum time in seconds, the default is 20
                    - count - instance count, the default is 0 (immediate)
    """
    # set trigger source to digital I/O lines, or turn it off
    if enable:
        dwf.FDwfDigitalInTriggerSourceSet(device_data.handle, constants.trigsrcDetectorDigitalIn)
        state.trigger = True
    else:
        dwf.FDwfDigitalInTriggerSourceSet(device_data.handle, constants.trigsrcNone)
        state.trigger = False
    
    # set starting position and prefill
    position = min(data.buffer_size, max(0, position))
    dwf.FDwfDigitalInTriggerPositionSet(device_data.handle, ctypes.c_int(data.buffer_size - position))
    dwf.FDwfDigitalInTriggerPrefillSet(device_data.handle, ctypes.c_int(position))

    # set trigger condition
    channel = ctypes.c_int(1 << channel)
    if not rising_edge:
        dwf.FDwfDigitalInTriggerSet(device_data.handle, channel, ctypes.c_int(0), ctypes.c_int(0), ctypes.c_int(0))
        dwf.FDwfDigitalInTriggerResetSet(device_data.handle, ctypes.c_int(0), ctypes.c_int(0), ctypes.c_int(0), channel)
    else:
        dwf.FDwfDigitalInTriggerSet(device_data.handle, ctypes.c_int(0), channel, ctypes.c_int(0), ctypes.c_int(0))
        dwf.FDwfDigitalInTriggerResetSet(device_data.handle, ctypes.c_int(0), ctypes.c_int(0), channel, ctypes.c_int(0))
    
    # set auto triggering
    dwf.FDwfDigitalInTriggerAutoTimeoutSet(device_data.handle, ctypes.c_double(timeout))
    
    # set sequence length to activate trigger
    dwf.FDwfDigitalInTriggerLengthSet(device_data.handle, ctypes.c_double(length_min), ctypes.c_double(length_max), ctypes.c_int(0))

    # set event counter
    dwf.FDwfDigitalInTriggerCountSet(device_data.handle, ctypes.c_int(count), ctypes.c_int(0))
    return

"""-----------------------------------------------------------------------"""

def record(device_data, channel):
    """
        initialize the logic analyzer

        parameters: - device data
                    - channel - the selected DIO line number

        returns:    - buffer - a list with the recorded logic values
                    - time - a list with the time moments for each value in seconds (with the same index as "buffer")
    """
    # set up the instrument
    dwf.FDwfDigitalInConfigure(device_data.handle, ctypes.c_bool(False), ctypes.c_bool(True))
    
    # read data to an internal buffer
    while True:
        status = ctypes.c_byte()    # variable to store buffer status
        dwf.FDwfDigitalInStatus(device_data.handle, ctypes.c_bool(True), ctypes.byref(status))
    
        if status.value == constants.stsDone.value:
            # exit loop when finished
            break
    
    # get samples
    buffer = (ctypes.c_uint16 * data.buffer_size)()
    dwf.FDwfDigitalInStatusData(device_data.handle, buffer, ctypes.c_int(2 * data.buffer_size))
    
    # convert buffer to list of lists of integers
    buffer = [int(element) for element in buffer]
    result = [[] for _ in range(16)]
    for point in buffer:
        for index in range(16):
            result[index].append(point & (1 << index))
    
    # calculate acquisition time
    time = range(0, data.buffer_size)
    time = [moment / data.sampling_frequency for moment in time]
    
    # get channel specific data
    buffer = result[channel]
    return buffer, time

"""-----------------------------------------------------------------------"""

def close(device_data):
    """
        reset the instrument
    """
    dwf.FDwfDigitalInReset(device_data.handle)
    state.on = False
    state.off = True
    state.trigger = False
    return
