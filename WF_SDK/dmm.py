""" DIGITAL MULTIMETER CONTROL FUNCTIONS: open, measure, close """

import ctypes                            # import the C compatible data types
import WF_SDK.dwfconstants as constants  # import every constant
from sys import platform                 # this is needed to check the OS type

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

def open(device_handle):
    """
        initialize the digital multimeter
    """
    # enable the DMM
    dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(3), ctypes.c_int(0), ctypes.c_double(1.0))
    return

"""-----------------------------------------------------------------------"""

def measure(device_handle, mode, ac=False, range=0, high_impedance=False):
    """
        measure a voltage/current/resistance/continuity/temperature

        parameters: - device handler
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
            dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(3), ctypes.c_int(1), constants.DwfDmmACVoltage)
        else:
            dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(3), ctypes.c_int(1), constants.DwfDmmDCVoltage)

        # set input impedance
        if high_impedance:
            dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(3), ctypes.c_int(5), ctypes.c_double(1))
        else:
            dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(3), ctypes.c_int(5), ctypes.c_double(0))

    # set high current mode
    elif mode == "high current":
        # set coupling
        if ac:
            dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(3), ctypes.c_int(1), constants.DwfDmmACCurrent)
        else:
            dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(3), ctypes.c_int(1), constants.DwfDmmDCCurrent)

    # set low current mode
    elif mode == "low current":
        # set coupling
        if ac:
            dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(3), ctypes.c_int(1), constants.DwfDmmACLowCurrent)
        else:
            dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(3), ctypes.c_int(1), constants.DwfDmmDCLowCurrent)
            
    # set resistance mode
    elif mode == "resistance":
        dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(3), ctypes.c_int(1), constants.DwfDmmResistance)

    # set continuity mode
    elif mode == "continuity":
        dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(3), ctypes.c_int(1), constants.DwfDmmContinuity)

    # set diode mode
    elif mode == "diode":
        dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(3), ctypes.c_int(1), constants.DwfDmmDiode)

    # set temperature mode
    elif mode == "temperature":
        dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(3), ctypes.c_int(1), constants.DwfDmmTemperature)
        
    # set range
    dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(3), ctypes.c_int(2), ctypes.c_double(range))

    # fetch analog I/O status
    if dwf.FDwfAnalogIOStatus(device_handle) == 0:
        # signal error
        return None

    # get reading
    measurement = ctypes.c_double()
    dwf.FDwfAnalogIOChannelNodeStatus(device_handle, ctypes.c_int(3), ctypes.c_int(3), ctypes.byref(measurement))

    return measurement.value

"""-----------------------------------------------------------------------"""

def close(device_handle):
    """
        reset the instrument
    """
    # disable the DMM
    dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(3), ctypes.c_int(0), ctypes.c_double(0))
    # reset the instrument
    dwf.FDwfAnalogIOReset(device_handle)
    return
