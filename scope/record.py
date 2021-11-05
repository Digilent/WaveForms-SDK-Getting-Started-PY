def record(device_handle, channel, sampling_frequency=20e06, buffer_size=8192):
    """
        record an analog signal

        parameters: - device handle
                    - the selected oscilloscope channel (1-2, or 1-4)
                    - sampling frequency in Hz, default is 20MHz
                    - buffer size, default is 8192

        returns:    - buffer - a list with the recorded voltages
                    - time - a list with the time moments for each voltage in seconds (with the same index as "buffer")
    """
    # set up the instrument
    dwf.FDwfAnalogInConfigure(device_handle, ctypes.c_bool(False), ctypes.c_bool(True))
    
    # read data to an internal buffer
    while True:
        status = ctypes.c_byte()    # variable to store buffer status
        dwf.FDwfAnalogInStatus(device_handle, ctypes.c_bool(True), ctypes.byref(status))
    
        # check internal buffer status
        if status.value == constants.DwfStateDone.value:
                # exit loop when ready
                break
    
    # copy buffer
    buffer = (ctypes.c_double * buffer_size)()   # create an empty buffer
    dwf.FDwfAnalogInStatusData(device_handle, ctypes.c_int(channel - 1), buffer, ctypes.c_int(buffer_size))
    
    # calculate aquisition time
    time = range(0, buffer_size)
    time = [moment / sampling_frequency for moment in time]
    
    # convert into list
    buffer = [float(element) for element in buffer]
    return buffer, time
