""" OSCILLOSCOPE CONTROL FUNCTIONS: open, measure, trigger, record, close """

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
    sampling_frequency = 20e06
    buffer_size = 8192
    max_buffer_size = 0

"""-----------------------------------------------------------------------"""

class trigger_source:
    """ trigger source names """
    none = constants.trigsrcNone
    analog = constants.trigsrcDetectorAnalogIn
    digital = constants.trigsrcDetectorDigitalIn
    external = [None, constants.trigsrcExternal1, constants.trigsrcExternal2, constants.trigsrcExternal3, constants.trigsrcExternal4]

"""-----------------------------------------------------------------------"""

def open(device_data, sampling_frequency=20e06, buffer_size=0, offset=0, amplitude_range=5):
    """
        initialize the oscilloscope

        parameters: - device data
                    - sampling frequency in Hz, default is 20MHz
                    - buffer size, default is 0 (maximum)
                    - offset voltage in Volts, default is 0V
                    - amplitude range in Volts, default is ±5V
    """
    # set global variables
    data.sampling_frequency = sampling_frequency
    data.max_buffer_size = device_data.analog.input.max_buffer_size

    # enable all channels
    if dwf.FDwfAnalogInChannelEnableSet(device_data.handle, ctypes.c_int(-1), ctypes.c_bool(True)) == 0:
        check_error()
    
    # set offset voltage (in Volts)
    if dwf.FDwfAnalogInChannelOffsetSet(device_data.handle, ctypes.c_int(-1), ctypes.c_double(offset)) == 0:
        check_error()
    
    # set range (maximum signal amplitude in Volts)
    if dwf.FDwfAnalogInChannelRangeSet(device_data.handle, ctypes.c_int(-1), ctypes.c_double(amplitude_range)) == 0:
        check_error()
    
    # set the buffer size (data point in a recording)
    if buffer_size == 0:
        buffer_size = data.max_buffer_size
    data.buffer_size = buffer_size
    if dwf.FDwfAnalogInBufferSizeSet(device_data.handle, ctypes.c_int(buffer_size)) == 0:
        check_error()
    
    # set the acquisition frequency (in Hz)
    if dwf.FDwfAnalogInFrequencySet(device_data.handle, ctypes.c_double(sampling_frequency)) == 0:
        check_error()
    
    # disable averaging (for more info check the documentation)
    if dwf.FDwfAnalogInChannelFilterSet(device_data.handle, ctypes.c_int(-1), constants.filterDecimate) == 0:
        check_error()
    return

"""-----------------------------------------------------------------------"""

def measure(device_data, channel):
    """
        measure a voltage

        parameters: - device data
                    - the selected oscilloscope channel (1-2, or 1-4)
        
        returns:    - the measured voltage in Volts
    """
    # set up the instrument
    if dwf.FDwfAnalogInConfigure(device_data.handle, ctypes.c_bool(False), ctypes.c_bool(False)) == 0:
        check_error()
    
    # read data to an internal buffer
    if dwf.FDwfAnalogInStatus(device_data.handle, ctypes.c_bool(False), ctypes.c_int(0)) == 0:
        check_error()
    
    # extract data from that buffer
    voltage = ctypes.c_double()   # variable to store the measured voltage
    if dwf.FDwfAnalogInStatusSample(device_data.handle, ctypes.c_int(channel - 1), ctypes.byref(voltage)) == 0:
        check_error()
    
    # store the result as float
    voltage = voltage.value
    return voltage

"""-----------------------------------------------------------------------"""

def trigger(device_data, enable, source=trigger_source.none, channel=1, timeout=0, edge_rising=True, level=0):
    """
        set up triggering

        parameters: - device data
                    - enable / disable triggering with True/False
                    - trigger source - possible: none, analog, digital, external[1-4]
                    - trigger channel - possible options: 1-4 for analog, or 0-15 for digital
                    - auto trigger timeout in seconds, default is 0
                    - trigger edge rising - True means rising, False means falling, default is rising
                    - trigger level in Volts, default is 0V
    """
    if enable and source != constants.trigsrcNone:
        # enable/disable auto triggering
        if dwf.FDwfAnalogInTriggerAutoTimeoutSet(device_data.handle, ctypes.c_double(timeout)) == 0:
            check_error()

        # set trigger source
        if dwf.FDwfAnalogInTriggerSourceSet(device_data.handle, source) == 0:
            check_error()

        # set trigger channel
        if source == constants.trigsrcDetectorAnalogIn:
            channel -= 1    # decrement analog channel index
        if dwf.FDwfAnalogInTriggerChannelSet(device_data.handle, ctypes.c_int(channel)) == 0:
            check_error()

        # set trigger type
        if dwf.FDwfAnalogInTriggerTypeSet(device_data.handle, constants.trigtypeEdge) == 0:
            check_error()

        # set trigger level
        if dwf.FDwfAnalogInTriggerLevelSet(device_data.handle, ctypes.c_double(level)) == 0:
            check_error()

        # set trigger edge
        if edge_rising:
            # rising edge
            if dwf.FDwfAnalogInTriggerConditionSet(device_data.handle, constants.trigcondRisingPositive) == 0:
                check_error()
        else:
            # falling edge
            if dwf.FDwfAnalogInTriggerConditionSet(device_data.handle, constants.trigcondFallingNegative) == 0:
                check_error()
    else:
        # turn off the trigger
        if dwf.FDwfAnalogInTriggerSourceSet(device_data.handle, constants.trigsrcNone) == 0:
            check_error()
    return

"""-----------------------------------------------------------------------"""

def record(device_data, channel):
    """
        record an analog signal

        parameters: - device data
                    - the selected oscilloscope channel (1-2, or 1-4)

        returns:    - a list with the recorded voltages
    """
    # set up the instrument
    if dwf.FDwfAnalogInConfigure(device_data.handle, ctypes.c_bool(False), ctypes.c_bool(True)) == 0:
        check_error()
    
    # read data to an internal buffer
    while True:
        status = ctypes.c_byte()    # variable to store buffer status
        if dwf.FDwfAnalogInStatus(device_data.handle, ctypes.c_bool(True), ctypes.byref(status)) == 0:
            check_error()
    
        # check internal buffer status
        if status.value == constants.DwfStateDone.value:
                # exit loop when ready
                break
    
    # copy buffer
    buffer = (ctypes.c_double * data.buffer_size)()   # create an empty buffer
    if dwf.FDwfAnalogInStatusData(device_data.handle, ctypes.c_int(channel - 1), buffer, ctypes.c_int(data.buffer_size)) == 0:
        check_error()
    
    # convert into list
    buffer = [float(element) for element in buffer]
    return buffer

"""-----------------------------------------------------------------------"""

def close(device_data):
    """
        reset the scope
    """
    if dwf.FDwfAnalogInReset(device_data.handle) == 0:
        check_error()
    return
