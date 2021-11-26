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
