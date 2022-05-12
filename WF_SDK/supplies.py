""" POWER SUPPLIES CONTROL FUNCTIONS: switch, switch_fixed, switch_variable, switch_digital, close """

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
    """ power supply parameters """
    master_state = False    # master switch
    state = False           # digital/6V/positive supply state
    positive_state = False  # positive supply switch
    negative_state = False  # negative supply switch
    positive_voltage = 0    # positive supply voltage
    negative_voltage = 0    # negative supply voltage
    voltage = 0             # digital/positive supply voltage
    positive_current = 0    # positive supply current
    negative_current = 0    # negative supply current
    current = 0             # digital/6V supply current

class state:
    """ stores the state of the instrument """
    on = False
    off = True
    type = ""
    positive_voltage = 0    # positive supply voltage
    negative_voltage = 0    # negative supply voltage
    voltage = 0             # digital/positive supply voltage
    positive_current = 0    # positive supply current
    negative_current = 0    # negative supply current
    current = 0             # digital/6V supply current

"""-----------------------------------------------------------------------"""

def _switch_fixed_(device_data, master_state, positive_state, negative_state):
    """
        turn the power supplies on/off

        parameters: - device data
                    - master switch - True = on, False = off
                    - positive supply switch - True = on, False = off
                    - negative supply switch - True = on, False = off
    """
    # enable/disable the positive supply
    dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(0), ctypes.c_int(0), ctypes.c_int(positive_state))
    
    # enable the negative supply
    dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(1), ctypes.c_int(0), ctypes.c_int(negative_state))
    
    # start/stop the supplies - master switch
    dwf.FDwfAnalogIOEnableSet(device_data.handle, ctypes.c_int(master_state))
    state.on = master_state or positive_state or negative_state
    state.off = not state.on
    state.positive_voltage = 5 if positive_state and master_state else 0
    state.negative_voltage = -5 if negative_state and master_state else 0
    state.type = "fixed"
    return

"""-----------------------------------------------------------------------"""

def _switch_variable_(device_data, master_state, positive_state, negative_state, positive_voltage, negative_voltage):
    """
        turn the power supplies on/off

        parameters: - device data
                    - master switch - True = on, False = off
                    - positive supply switch - True = on, False = off
                    - negative supply switch - True = on, False = off
                    - positive supply voltage in Volts
                    - negative supply voltage in Volts
    """
    # set positive voltage
    positive_voltage = max(0, min(5, positive_voltage))
    dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(0), ctypes.c_int(1), ctypes.c_double(positive_voltage))
    
    # set negative voltage
    negative_voltage = max(-5, min(0, negative_voltage))
    dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(1), ctypes.c_int(1), ctypes.c_double(negative_voltage))

    # enable/disable the positive supply
    dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(0), ctypes.c_int(0), ctypes.c_int(positive_state))
    
    # enable the negative supply
    dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(1), ctypes.c_int(0), ctypes.c_int(negative_state))
    
    # start/stop the supplies - master switch
    dwf.FDwfAnalogIOEnableSet(device_data.handle, ctypes.c_int(master_state))
    state.on = master_state or positive_state or negative_state
    state.off = not state.on
    state.positive_voltage = positive_voltage if positive_state and master_state else 0
    state.negative_voltage = negative_voltage if negative_state and master_state else 0
    state.type = "variable"
    return

"""-----------------------------------------------------------------------"""

def _switch_digital_(device_data, master_state, voltage):
    """
        turn the power supplies on/off

        parameters: - device data
                    - master switch - True = on, False = off
                    - supply voltage in Volts
    """
    # set supply voltage
    voltage = max(1.2, min(3.3, voltage))
    dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(0), ctypes.c_int(0), ctypes.c_double(voltage))
    
    # start/stop the supplies - master switch
    dwf.FDwfAnalogIOEnableSet(device_data.handle, ctypes.c_int(master_state))
    state.on = master_state
    state.off = not state.on
    state.voltage = voltage if master_state else 0
    state.type = "digital"
    return

"""-----------------------------------------------------------------------"""

def _switch_6V_(device_data, master_state, voltage, current=1):
    """
        turn the 6V supply on the ADP5250 on/off

        parameters: - master switch - True = on, False = off
                    - voltage in volts between 0-6
                    - current in amperes between 0-1
    """
    # set the voltage
    voltage = max(0, min(6, voltage))
    dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(0), ctypes.c_int(1), ctypes.c_double(voltage))
    
    # set the current
    current = max(0, min(1, current))
    dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(0), ctypes.c_int(2), ctypes.c_double(current))
    
    # start/stop the supply - master switch
    dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(0), ctypes.c_int(0), ctypes.c_double(float(master_state)))
    dwf.FDwfAnalogIOEnableSet(device_data.handle, ctypes.c_int(master_state))
    state.on = master_state
    state.off = not state.on
    state.voltage = voltage if master_state else 0
    state.current = current if master_state else 0
    state.type = "6V"
    return

"""-----------------------------------------------------------------------"""

def _switch_25V_(device_data, positive_state, negative_state, positive_voltage, negative_voltage, positive_current=0.5, negative_current=-0.5):
    """
        turn the 25V power supplies on/off on the ADP5250

        parameters: - positive supply switch - True = on, False = off
                    - negative supply switch - True = on, False = off
                    - positive supply voltage in Volts
                    - negative supply voltage in Volts
                    - positive supply current limit
                    - negative supply current limit
    """
    # set positive voltage
    positive_voltage = max(0, min(25, positive_voltage))
    dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(1), ctypes.c_int(1), ctypes.c_double(positive_voltage))
    
    # set negative voltage
    negative_voltage *= -1
    dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(2), ctypes.c_int(1), ctypes.c_double(negative_voltage))

    # set positive current limit
    positive_current = max(0, min(0.5, positive_current))
    dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(1), ctypes.c_int(2), ctypes.c_double(positive_current))
    
    # set negative current limit
    negative_current *= -1
    dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(2), ctypes.c_int(2), ctypes.c_double(negative_current))

    # enable/disable the supplies
    dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(1), ctypes.c_int(0), ctypes.c_double(float(positive_state)))
    dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(2), ctypes.c_int(0), ctypes.c_double(float(negative_state)))
    
    # master switch
    dwf.FDwfAnalogIOEnableSet(device_data.handle, ctypes.c_int(positive_state or negative_state))
    state.on = positive_state or negative_state
    state.off = not state.on
    state.positive_voltage = positive_voltage if positive_state else 0
    state.negative_voltage = negative_voltage if negative_state else 0
    state.positive_current = positive_current if positive_state else 0
    state.negative_current = negative_current if negative_state else 0
    state.type = "25V"
    return

"""-----------------------------------------------------------------------"""

def switch(device_data, supplies_data):
    """
        turn the power supplies on/off

        parameters: - device data
                    - class containing supplies data:
                        - master_state
                        - state and/or positive_state and negative_state
                        - voltage and/or positive_voltage and negative_voltage
                        - current and/or positive_current and negative_current
    """
    if device_data.name == "Analog Discovery":
        # switch fixed supplies on AD
        supply_state = supplies_data.state or supplies_data.positive_state
        _switch_fixed_(device_data, supplies_data.master_state, supply_state, supplies_data.negative_state)

    elif device_data.name == "Analog Discovery 2" or device_data.name == "Analog Discovery Studio":
        # switch variable supplies on AD2
        supply_state = supplies_data.state or supplies_data.positive_state
        supply_voltage = supplies_data.voltage + supplies_data.positive_voltage
        _switch_variable_(device_data, supplies_data.master_state, supply_state, supplies_data.negative_state, supply_voltage, supplies_data.negative_voltage)

    elif device_data.name == "Digital Discovery" or device_data.name == "Analog Discovery Pro 3X50":
        # switch the digital supply on DD, or ADP3x50
        supply_state = supplies_data.master_state and (supplies_data.state or supplies_data.positive_state)
        supply_voltage = supplies_data.voltage + supplies_data.positive_voltage
        _switch_digital_(device_data, supply_state, supply_voltage)

    elif device_data.name == "Analog Discovery Pro 5250":
        # switch the 6V supply on ADP5250
        supply_state = supplies_data.master_state and supplies_data.state
        _switch_6V_(device_data, supply_state, supplies_data.voltage, supplies_data.current)
        # switch the 25V supplies on ADP5250
        supply_positive_state = supplies_data.master_state and supplies_data.positive_state
        supply_negative_state = supplies_data.master_state and supplies_data.negative_state
        _switch_25V_(device_data, supply_positive_state, supply_negative_state, supplies_data.positive_voltage, supplies_data.negative_voltage, supplies_data.positive_current, supplies_data.negative_current)
    return

"""-----------------------------------------------------------------------"""

def close(device_data):
    """
        reset the supplies
    """
    dwf.FDwfAnalogIOReset(device_data.handle)
    state.on = False
    state.off = True
    state.type = ""
    state.positive_voltage = 0    # positive supply voltage
    state.negative_voltage = 0    # negative supply voltage
    state.voltage = 0             # digital/positive supply voltage
    state.positive_current = 0    # positive supply current
    state.negative_current = 0    # negative supply current
    state.current = 0             # digital/6V supply current
    return
