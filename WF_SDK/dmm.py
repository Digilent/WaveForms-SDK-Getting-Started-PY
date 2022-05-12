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

"""-----------------------------------------------------------------------"""

class state:
    """ stores the state of the instrument """
    on = False
    off = True

"""-----------------------------------------------------------------------"""

def open(device_data):
    """
        initialize the digital multimeter
    """
    # enable the DMM
    dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(3), ctypes.c_int(0), ctypes.c_double(1.0))
    state.on = True
    state.off = False
    return

"""-----------------------------------------------------------------------"""

def measure(device_data, mode, ac=False, range=0, high_impedance=False):
    """
        measure a voltage/current/resistance/continuity/temperature

        parameters: - device data
                    - mode: "voltage", "low current", "high current", "resistance", "continuity", "diode", "temperature"
                    - ac: True means AC value, False means DC value, default is DC
                    - range: voltage/current/resistance/temperature range, 0 means auto, default is auto
                    - high_impedance: input impedance for DC voltage measurement, False means 10MΩ, True means 10GΩ, default is 10MΩ
        
        returns:    - the measured value in V/A/Ω/°C, or None on error
    """
    # set voltage mode
    if mode == "voltage":
        # set coupling
        if ac:
            dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(3), ctypes.c_int(1), constants.DwfDmmACVoltage)
        else:
            dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(3), ctypes.c_int(1), constants.DwfDmmDCVoltage)

        # set input impedance
        if high_impedance:
            dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(3), ctypes.c_int(5), ctypes.c_double(1))
        else:
            dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(3), ctypes.c_int(5), ctypes.c_double(0))

    # set high current mode
    elif mode == "high current":
        # set coupling
        if ac:
            dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(3), ctypes.c_int(1), constants.DwfDmmACCurrent)
        else:
            dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(3), ctypes.c_int(1), constants.DwfDmmDCCurrent)

    # set low current mode
    elif mode == "low current":
        # set coupling
        if ac:
            dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(3), ctypes.c_int(1), constants.DwfDmmACLowCurrent)
        else:
            dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(3), ctypes.c_int(1), constants.DwfDmmDCLowCurrent)
            
    # set resistance mode
    elif mode == "resistance":
        dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(3), ctypes.c_int(1), constants.DwfDmmResistance)

    # set continuity mode
    elif mode == "continuity":
        dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(3), ctypes.c_int(1), constants.DwfDmmContinuity)

    # set diode mode
    elif mode == "diode":
        dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(3), ctypes.c_int(1), constants.DwfDmmDiode)

    # set temperature mode
    elif mode == "temperature":
        dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(3), ctypes.c_int(1), constants.DwfDmmTemperature)
        
    # set range
    dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(3), ctypes.c_int(2), ctypes.c_double(range))

    # fetch analog I/O status
    if dwf.FDwfAnalogIOStatus(device_data.handle) == 0:
        # signal error
        return None

    # get reading
    measurement = ctypes.c_double()
    dwf.FDwfAnalogIOChannelNodeStatus(device_data.handle, ctypes.c_int(3), ctypes.c_int(3), ctypes.byref(measurement))

    return measurement.value

"""-----------------------------------------------------------------------"""

def close(device_data):
    """
        reset the instrument
    """
    # disable the DMM
    dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(3), ctypes.c_int(0), ctypes.c_double(0))
    # reset the instrument
    dwf.FDwfAnalogIOReset(device_data.handle)
    state.on = False
    state.off = True
    return
