def open(device_handle, sampling_frequency=100e06, buffer_size=4096):
    """
        initialize the logic analyzer

        parameters: - device handle
                    - sampling frequency in Hz, default is 100MHz
                    - buffer size, default is 4096
    """
    # get internal clock frequency
    internal_frequency = ctypes.c_double()
    dwf.FDwfDigitalInInternalClockInfo(device_handle, ctypes.byref(internal_frequency))
    
    # set clock frequency divider (needed for lower frequency input signals)
    dwf.FDwfDigitalInDividerSet(device_handle, ctypes.c_int(int(internal_frequency.value / sampling_frequency)))
    
    # set 16-bit sample format
    dwf.FDwfDigitalInSampleFormatSet(device_handle, ctypes.c_int(16))
    
    # set buffer size
    dwf.FDwfDigitalInBufferSizeSet(device_handle, ctypes.c_int(buffer_size))
    return
