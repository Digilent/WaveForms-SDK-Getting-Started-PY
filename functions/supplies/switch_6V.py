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
