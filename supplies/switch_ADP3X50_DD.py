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
