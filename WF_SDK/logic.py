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
from WF_SDK.device import check_error

"""-----------------------------------------------------------------------"""

class data:
    """ stores the sampling frequency and the buffer size """
    sampling_frequency = 100e06
    buffer_size = 4096
    max_buffer_size = 0

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
    if dwf.FDwfDigitalInInternalClockInfo(device_data.handle, ctypes.byref(internal_frequency)) == 0:
        check_error()
    
    # set clock frequency divider (needed for lower frequency input signals)
    if dwf.FDwfDigitalInDividerSet(device_data.handle, ctypes.c_int(int(internal_frequency.value / sampling_frequency))) == 0:
        check_error()
    
    # set 16-bit sample format
    if dwf.FDwfDigitalInSampleFormatSet(device_data.handle, ctypes.c_int(16)) == 0:
        check_error()
    
    # set buffer size
    if buffer_size == 0:
        buffer_size = data.max_buffer_size
    data.buffer_size = buffer_size
    if dwf.FDwfDigitalInBufferSizeSet(device_data.handle, ctypes.c_int(buffer_size)) == 0:
        check_error()
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
        if dwf.FDwfDigitalInTriggerSourceSet(device_data.handle, constants.trigsrcDetectorDigitalIn) == 0:
            check_error()
    else:
        if dwf.FDwfDigitalInTriggerSourceSet(device_data.handle, constants.trigsrcNone) == 0:
            check_error()
        return
    
    # set starting position and prefill
    position = min(data.buffer_size, max(0, position))
    if dwf.FDwfDigitalInTriggerPositionSet(device_data.handle, ctypes.c_int(data.buffer_size - position)) == 0:
        check_error()
    if dwf.FDwfDigitalInTriggerPrefillSet(device_data.handle, ctypes.c_int(position)) == 0:
        check_error()

    # set trigger condition
    channel = ctypes.c_int(1 << channel)
    if not rising_edge:
        if dwf.FDwfDigitalInTriggerSet(device_data.handle, channel, ctypes.c_int(0), ctypes.c_int(0), ctypes.c_int(0)) == 0:
            check_error()
        if dwf.FDwfDigitalInTriggerResetSet(device_data.handle, ctypes.c_int(0), ctypes.c_int(0), ctypes.c_int(0), channel) == 0:
            check_error()
    else:
        if dwf.FDwfDigitalInTriggerSet(device_data.handle, ctypes.c_int(0), channel, ctypes.c_int(0), ctypes.c_int(0)) == 0:
            check_error()
        if dwf.FDwfDigitalInTriggerResetSet(device_data.handle, ctypes.c_int(0), ctypes.c_int(0), channel, ctypes.c_int(0)) == 0:
            check_error()
    
    # set auto triggering
    if dwf.FDwfDigitalInTriggerAutoTimeoutSet(device_data.handle, ctypes.c_double(timeout)) == 0:
        check_error()
    
    # set sequence length to activate trigger
    if dwf.FDwfDigitalInTriggerLengthSet(device_data.handle, ctypes.c_double(length_min), ctypes.c_double(length_max), ctypes.c_int(0)) == 0:
        check_error()

    # set event counter
    if dwf.FDwfDigitalInTriggerCountSet(device_data.handle, ctypes.c_int(count), ctypes.c_int(0)) == 0:
        check_error()
    return

"""-----------------------------------------------------------------------"""

def record(device_data, channel):
    """
        initialize the logic analyzer

        parameters: - device data
                    - channel - the selected DIO line number

        returns:    - a list with the recorded logic values
    """
    # set up the instrument
    if dwf.FDwfDigitalInConfigure(device_data.handle, ctypes.c_bool(False), ctypes.c_bool(True)) == 0:
        check_error()
    
    # read data to an internal buffer
    while True:
        status = ctypes.c_byte()    # variable to store buffer status
        if dwf.FDwfDigitalInStatus(device_data.handle, ctypes.c_bool(True), ctypes.byref(status)) == 0:
            check_error()
    
        if status.value == constants.stsDone.value:
            # exit loop when finished
            break
    
    # get samples
    buffer = (ctypes.c_uint16 * data.buffer_size)()
    if dwf.FDwfDigitalInStatusData(device_data.handle, buffer, ctypes.c_int(2 * data.buffer_size)) == 0:
        check_error()
    
    # convert buffer to list of lists of integers
    result = []
    for point in buffer:
        result.append((int(point) & (1 << channel)) >> channel)
    
    return result

"""-----------------------------------------------------------------------"""

def close(device_data):
    """
        reset the instrument
    """
    if dwf.FDwfDigitalInReset(device_data.handle) == 0:
        check_error()
    return
