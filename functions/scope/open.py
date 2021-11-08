def open(device_handle, sampling_frequency=20e06, buffer_size=8192, offset=0, amplitude_range=5):
    """
        initialize the oscilloscope

        parameters: - device handle
                    - sampling frequency in Hz, default is 20MHz
                    - buffer size, default is 8192
                    - offset voltage in Volts, default is 0V
                    - amplitude range in Volts, default is ±5V
    """
    # enable all channels
    dwf.FDwfAnalogInChannelEnableSet(device_handle, ctypes.c_int(0), ctypes.c_bool(True))
    
    # set offset voltage (in Volts)
    dwf.FDwfAnalogInChannelOffsetSet(device_handle, ctypes.c_int(0), ctypes.c_double(offset))
    
    # set range (maximum signal amplitude in Volts)
    dwf.FDwfAnalogInChannelRangeSet(device_handle, ctypes.c_int(0), ctypes.c_double(amplitude_range))
    
    # set the buffer size (data point in a recording)
    dwf.FDwfAnalogInBufferSizeSet(device_handle, ctypes.c_int(buffer_size))
    
    # set the acquisition frequency (in Hz)
    dwf.FDwfAnalogInFrequencySet(device_handle, ctypes.c_double(sampling_frequency))
    
    # disable averaging (for more info check the documentation)
    dwf.FDwfAnalogInChannelFilterSet(device_handle, ctypes.c_int(-1), constants.filterDecimate)
    return
