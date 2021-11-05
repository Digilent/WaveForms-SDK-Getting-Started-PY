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
