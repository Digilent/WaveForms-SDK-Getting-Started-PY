""" POWER SUPPLIES CONTROL FUNCTIONS: switch, switch_fixed, switch_variable, switch_digital, close """

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

def switch_fixed(device_handle, master_state, positive_state, negative_state):
    """
        turn the power supplies on/off

        parameters: - device handle
                    - master switch - True = on, False = off
                    - positive supply switch - True = on, False = off
                    - negative supply switch - True = on, False = off
    """
    # enable/disable the positive supply
    dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(0), ctypes.c_int(0), ctypes.c_int(positive_state))
    
    # enable the negative supply
    dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(1), ctypes.c_int(0), ctypes.c_int(negative_state))
    
    # start/stop the supplies - master switch
    dwf.FDwfAnalogIOEnableSet(device_handle, ctypes.c_int(master_state))
    return

"""-----------------------------------------------------------------------"""

def switch_variable(device_handle, master_state, positive_state, negative_state, positive_voltage, negative_voltage):
    """
        turn the power supplies on/off

        parameters: - device handle
                    - master switch - True = on, False = off
                    - positive supply switch - True = on, False = off
                    - negative supply switch - True = on, False = off
                    - positive supply voltage in Volts
                    - negative supply voltage in Volts
    """
    # set positive voltage
    positive_voltage = max(0, min(5, positive_voltage))
    dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(0), ctypes.c_int(1), ctypes.c_double(positive_voltage))
    
    # set negative voltage
    negative_voltage = max(-5, min(0, negative_voltage))
    dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(1), ctypes.c_int(1), ctypes.c_double(negative_voltage))

    # enable/disable the positive supply
    dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(0), ctypes.c_int(0), ctypes.c_int(positive_state))
    
    # enable the negative supply
    dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(1), ctypes.c_int(0), ctypes.c_int(negative_state))
    
    # start/stop the supplies - master switch
    dwf.FDwfAnalogIOEnableSet(device_handle, ctypes.c_int(master_state))
    return

"""-----------------------------------------------------------------------"""

def switch_digital(device_handle, master_state, voltage):
    """
        turn the power supplies on/off

        parameters: - device handle
                    - master switch - True = on, False = off
                    - supply voltage in Volts
    """
    # set supply voltage
    voltage = max(1.2, min(3.3, voltage))
    dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(0), ctypes.c_int(0), ctypes.c_double(voltage))
    
    # start/stop the supplies - master switch
    dwf.FDwfAnalogIOEnableSet(device_handle, ctypes.c_int(master_state))
    return

"""-----------------------------------------------------------------------"""

def switch_6V(device_handle, master_state, voltage, current=1):
    """
        turn the 6V supply on the ADP5250 on/off

        parameters: - device handle
                    - master switch - True = on, False = off
                    - voltage in volts between 0-6
                    - current in amperes between 0-1
    """
    # set the voltage
    voltage = max(0, min(6, voltage))
    dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(0), ctypes.c_int(1), ctypes.c_double(voltage))
    
    # set the current
    current = max(0, min(1, current))
    dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(0), ctypes.c_int(2), ctypes.c_double(current))
    
    # start/stop the supply - master switch
    dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(0), ctypes.c_int(0), ctypes.c_int(master_state))
    return

"""-----------------------------------------------------------------------"""

def switch_25V(device_handle, positive_state, negative_state, positive_voltage, negative_voltage, positive_current=0.5, negative_current=-0.5):
    """
        turn the 25V power supplies on/off on the ADP5250

        parameters: - device handle
                    - positive supply switch - True = on, False = off
                    - negative supply switch - True = on, False = off
                    - positive supply voltage in Volts
                    - negative supply voltage in Volts
                    - positive supply current limit
                    - negative supply current limit
    """
    # set positive voltage
    positive_voltage = max(0, min(25, positive_voltage))
    dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(1), ctypes.c_int(1), ctypes.c_double(positive_voltage))
    
    # set negative voltage
    negative_voltage = max(-25, min(0, negative_voltage))
    dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(2), ctypes.c_int(1), ctypes.c_double(negative_voltage))

    # set positive current limit
    positive_current = max(0, min(0.5, positive_current))
    dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(1), ctypes.c_int(2), ctypes.c_double(positive_current))
    
    # set negative current limit
    negative_current = max(-0.5, min(0, negative_current))
    dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(2), ctypes.c_int(2), ctypes.c_double(negative_current))

    # enable/disable the positive supply
    dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(1), ctypes.c_int(0), ctypes.c_int(positive_state))
    
    # enable/disable the negative supply
    dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(2), ctypes.c_int(0), ctypes.c_int(negative_state))
    return

"""-----------------------------------------------------------------------"""

def switch(device_handle, device_name, master_state, positive_state, negative_state, positive_voltage, negative_voltage):
    """
        turn the power supplies on/off

        parameters: - device handle
                    - device name
                    - master switch - True = on, False = off
                    - positive supply switch - True = on, False = off
                    - negative supply switch - True = on, False = off
                    - positive supply voltage in Volts
                    - negative supply voltage in Volts
    """
    if device_name == "Analog Discovery":
        switch_fixed(device_handle, master_state, positive_state, negative_state)
    elif device_name == "Analog Discovery 2" or device_name == "Analog Discovery Studio":
        switch_variable(device_handle, master_state, positive_state, negative_state, positive_voltage, negative_voltage)
    elif device_name == "Digital Discovery" or device_name == "Analog Discovery Pro 3X50":
        switch_digital(device_handle, master_state, positive_voltage)
    return

"""-----------------------------------------------------------------------"""

def close(device_handle):
    """
        reset the supplies
    """
    dwf.FDwfAnalogIOReset(device_handle)
    return
