""" DIGITAL MULTIMETER CONTROL FUNCTIONS: open, measure, close """

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

class mode:
    """ DMM modes """
    ac_voltage = constants.DwfDmmACVoltage
    dc_voltage = constants.DwfDmmDCVoltage
    ac_high_current = constants.DwfDmmACCurrent
    dc_high_current = constants.DwfDmmDCCurrent
    ac_low_current = constants.DwfDmmACLowCurrent
    dc_low_current = constants.DwfDmmDCLowCurrent
    resistance = constants.DwfDmmResistance
    continuity = constants.DwfDmmContinuity
    diode = constants.DwfDmmDiode
    temperature = constants.DwfDmmTemperature

"""-----------------------------------------------------------------------"""

class data:
    """ storers instrument information """
    __channel__ = -1
    class __nodes__:
        __enable__ = -1
        __mode__ = -1
        __range__ = -1
        __meas__ = -1
        __raw__ = -1
        __input__ = -1

"""-----------------------------------------------------------------------"""

def open(device_data):
    """
        initialize the digital multimeter
    """
    # find channel
    for channel_index in range(device_data.analog.IO.channel_count):
        if device_data.analog.IO.channel_label[channel_index] == "DMM":
            data.__channel__ = channel_index
            break
    
    # find nodes
    if data.__channel__ >= 0:
        for node_index in range(device_data.analog.IO.node_count[data.__channel__]):
            if device_data.analog.IO.node_name[data.__channel__][node_index] == "Enable":
                data.__nodes__.__enable__ = node_index
            elif device_data.analog.IO.node_name[data.__channel__][node_index] == "Mode":
                data.__nodes__.__mode__ = node_index
            elif device_data.analog.IO.node_name[data.__channel__][node_index] == "Range":
                data.__nodes__.__range__ = node_index
            elif device_data.analog.IO.node_name[data.__channel__][node_index] == "Meas":
                data.__nodes__.__meas__ = node_index
            elif device_data.analog.IO.node_name[data.__channel__][node_index] == "Raw":
                data.__nodes__.__raw__ = node_index
            elif device_data.analog.IO.node_name[data.__channel__][node_index] == "Input":
                data.__nodes__.__input__ = node_index

    # enable the DMM
    if data.__channel__ >= 0 and data.__nodes__.__enable__ >= 0:
        if dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(data.__channel__), ctypes.c_int(data.__nodes__.__enable__), ctypes.c_double(1.0)) == 0:
            check_error()
    return

"""-----------------------------------------------------------------------"""

def measure(device_data, mode, range=0, high_impedance=False):
    """
        measure a voltage/current/resistance/continuity/temperature

        parameters: - device data
                    - mode: dmm.mode.ac_voltage/dc_voltage/ac_high_current/dc_high_current/ac_low_current/dc_low_current/resistance/continuity/diode/temperature
                    - range: voltage/current/resistance/temperature range, 0 means auto, default is auto
                    - high_impedance: input impedance for DC voltage measurement, False means 10MΩ, True means 10GΩ, default is 10MΩ
        
        returns:    - the measured value in V/A/Ω/°C, or None on error
    """
    if data.__channel__ >= 0:
        # set input impedance
        if data.__nodes__.__input__ >= 0:
            if high_impedance:
                if dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(data.__channel__), ctypes.c_int(data.__nodes__.__input__), ctypes.c_double(1)) == 0:
                    check_error()
            else:
                if dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(data.__channel__), ctypes.c_int(data.__nodes__.__input__), ctypes.c_double(0)) == 0:
                    check_error()

        # set mode
        if data.__nodes__.__mode__ >= 0:
            if dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(data.__channel__), ctypes.c_int(data.__nodes__.__mode__), mode) == 0:
                check_error()

        # set range
        if data.__nodes__.__range__ >= 0:
            if dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(data.__channel__), ctypes.c_int(data.__nodes__.__range__), range) == 0:
                check_error()

        # fetch analog IO status
        if dwf.FDwfAnalogIOStatus(device_data.handle) == 0:
            # signal error
            check_error()
            return None
        
        # get reading
        if data.__nodes__.__meas__ >= 0:
            measurement = ctypes.c_double()
            if dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(data.__channel__), ctypes.c_int(data.__nodes__.__meas__), ctypes.byref(measurement)) == 0:
                check_error()
            return measurement.value
    return None

"""-----------------------------------------------------------------------"""

def close(device_data):
    """
        reset the instrument
    """
    # disable the DMM
    if data.__channel__ >= 0 and data.__nodes__.__enable__ >= 0:
        if dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(data.__channel__), ctypes.c_int(data.__nodes__.__enable__), ctypes.c_double(0)) == 0:
            check_error()
    # reset the instrument
    if dwf.FDwfAnalogIOReset(device_data.handle) == 0:
        check_error()
    return
