def measure(device_handle, channel):
    """
        measure a voltage

        parameters: - device handler
                    - the selected oscilloscope channel (1-2, or 1-4)
        
        returns:    - the measured voltage in Volts
    """
    # set up the instrument
    dwf.FDwfAnalogInConfigure(device_handle, ctypes.c_bool(False), ctypes.c_bool(False))
    
    # read data to an internal buffer
    dwf.FDwfAnalogInStatus(device_handle, ctypes.c_bool(False), ctypes.c_int(0))
    
    # extract data from that buffer
    voltage = ctypes.c_double()   # variable to store the measured voltage
    dwf.FDwfAnalogInStatusSample(device_handle, ctypes.c_int(channel - 1), ctypes.byref(voltage))
    
    # store the result as float
    voltage = voltage.value
    return voltage
