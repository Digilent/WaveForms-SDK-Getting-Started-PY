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
from WF_SDK.device import check_error

"""-----------------------------------------------------------------------"""

class data:
    """ power supply parameters """
    master_state = False    # master switch
    positive_state = False  # positive supply switch
    negative_state = False  # negative supply switch
    state = False           # digital/6V supply state
    positive_voltage = 0    # positive supply voltage
    negative_voltage = 0    # negative supply voltage
    voltage = 0             # digital/6V supply voltage
    positive_current = 0    # positive supply current
    negative_current = 0    # negative supply current
    current = 0             # digital/6V supply current

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
    # find the positive supply
    channel = -1
    for channel_index in range(device_data.analog.IO.channel_count):
        if device_data.analog.IO.channel_label[channel_index] == "V+" or device_data.analog.IO.channel_label[channel_index] == "p25V":
            channel = channel_index
            break
    if channel != -1:
        # set enable
        try:
            node = -1
            # find the voltage node
            for node_index in range(device_data.analog.IO.node_count[channel]):
                if device_data.analog.IO.node_name[channel][node_index] == "Enable":
                    node = node_index
                    break
            if node != -1:
                enable = ctypes.c_int(supplies_data.positive_state)
                if dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(channel), ctypes.c_int(node), enable) == 0:
                    check_error()
        except:
            pass
        # set voltage
        try:
            node = -1
            # find the voltage node
            for node_index in range(device_data.analog.IO.node_count[channel]):
                if device_data.analog.IO.node_name[channel][node_index] == "Voltage":
                    node = node_index
                    break
            if node != -1:
                voltage = min(max(supplies_data.positive_voltage, device_data.analog.IO.min_set_range[channel][node]), device_data.analog.IO.max_set_range[channel][node])
                if dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(channel), ctypes.c_int(node), ctypes.c_double(voltage)) == 0:
                    check_error()
        except:
            pass
        # set current
        try:
            node = -1
            # find the voltage node
            for node_index in range(device_data.analog.IO.node_count[channel]):
                if device_data.analog.IO.node_name[channel][node_index] == "Current":
                    node = node_index
                    break
            if node != -1:
                current = min(max(supplies_data.positive_current, device_data.analog.IO.min_set_range[channel][node]), device_data.analog.IO.max_set_range[channel][node])
                if dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(channel), ctypes.c_int(node), ctypes.c_double(current)) == 0:
                    check_error()
        except:
            pass
    
    # find the negative supply
    channel = -1
    for channel_index in range(device_data.analog.IO.channel_count):
        if device_data.analog.IO.channel_label[channel_index] == "V-" or device_data.analog.IO.channel_label[channel_index] == "n25V":
            channel = channel_index
            break
    if channel != -1:
        # set enable
        try:
            node = -1
            # find the voltage node
            for node_index in range(device_data.analog.IO.node_count[channel]):
                if device_data.analog.IO.node_name[channel][node_index] == "Enable":
                    node = node_index
                    break
            if node != -1:
                enable = ctypes.c_int(supplies_data.negative_state)
                if dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(channel), ctypes.c_int(node), enable) == 0:
                    check_error()
        except:
            pass
        # set voltage
        try:
            node = -1
            # find the voltage node
            for node_index in range(device_data.analog.IO.node_count[channel]):
                if device_data.analog.IO.node_name[channel][node_index] == "Voltage":
                    node = node_index
                    break
            if node != -1:
                voltage = min(max(supplies_data.negative_voltage, device_data.analog.IO.min_set_range[channel][node]), device_data.analog.IO.max_set_range[channel][node])
                if dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(channel), ctypes.c_int(node), ctypes.c_double(voltage)) == 0:
                    check_error()
        except:
            pass
        # set current
        try:
            node = -1
            # find the voltage node
            for node_index in range(device_data.analog.IO.node_count[channel]):
                if device_data.analog.IO.node_name[channel][node_index] == "Current":
                    node = node_index
                    break
            if node != -1:
                current = min(max(supplies_data.negative_current, device_data.analog.IO.min_set_range[channel][node]), device_data.analog.IO.max_set_range[channel][node])
                if dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(channel), ctypes.c_int(node), ctypes.c_double(current)) == 0:
                    check_error()
        except:
            pass
    
    # find the digital/6V supply
    channel = -1
    for channel_index in range(device_data.analog.IO.channel_count):
        if device_data.analog.IO.channel_label[channel_index] == "VDD" or device_data.analog.IO.channel_label[channel_index] == "p6V":
            channel = channel_index
            break
    if channel != -1:
        # set enable
        try:
            node = -1
            # find the voltage node
            for node_index in range(device_data.analog.IO.node_count[channel]):
                if device_data.analog.IO.node_name[channel][node_index] == "Enable":
                    node = node_index
                    break
            if node != -1:
                enable = ctypes.c_int(supplies_data.state)
                if dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(channel), ctypes.c_int(node), enable) == 0:
                    check_error()
        except:
            pass
        # set voltage
        try:
            node = -1
            # find the voltage node
            for node_index in range(device_data.analog.IO.node_count[channel]):
                if device_data.analog.IO.node_name[channel][node_index] == "Voltage":
                    node = node_index
                    break
            if node != -1:
                voltage = min(max(supplies_data.voltage, device_data.analog.IO.min_set_range[channel][node]), device_data.analog.IO.max_set_range[channel][node])
                if dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(channel), ctypes.c_int(node), ctypes.c_double(voltage)) == 0:
                    check_error()
        except:
            pass
        # set current
        try:
            node = -1
            # find the voltage node
            for node_index in range(device_data.analog.IO.node_count[channel]):
                if device_data.analog.IO.node_name[channel][node_index] == "Current":
                    node = node_index
                    break
            if node != -1:
                current = min(max(supplies_data.current, device_data.analog.IO.min_set_range[channel][node]), device_data.analog.IO.max_set_range[channel][node])
                if dwf.FDwfAnalogIOChannelNodeSet(device_data.handle, ctypes.c_int(channel), ctypes.c_int(node), ctypes.c_double(current)) == 0:
                    check_error()
        except:
            pass

    # turn all supplies on/off
    try:
        if dwf.FDwfAnalogIOEnableSet(device_data.handle, ctypes.c_int(supplies_data.master_state)) == 0:
            check_error()
    except:
        pass
    return

"""-----------------------------------------------------------------------"""

def close(device_data):
    """
        reset the supplies
    """
    if dwf.FDwfAnalogIOReset(device_data.handle) == 0:
        check_error()
    return
