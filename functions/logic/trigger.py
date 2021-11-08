def trigger(device_handle, enable, channel, buffer_size=4096, position=0, timeout=0, rising_edge=True, length_min=0, length_max=20, count=1):
    """
        set up triggering

        parameters: - device handle
                    - enable - True or False to enable, or disable triggering
                    - channel - the selected DIO line number to use as trigger source
                    - buffer size, the default is 4096
                    - position - prefill size, the default is 0
                    - timeout - auto trigger time, the default is 0
                    - rising_edge - set True for rising edge, False for falling edge, the default is rising edge
                    - length_min - trigger sequence minimum time in seconds, the default is 0
                    - length_max - trigger sequence maximum time in seconds, the default is 20
                    - count - nt count, the default is 1
    """
    # set trigger source to digital I/O lines, or turn it off
    if enable:
        dwf.FDwfDigitalInTriggerSourceSet(device_handle, constants.trigsrcDetectorDigitalIn)
    else:
        dwf.FDwfDigitalInTriggerSourceSet(device_handle, constants.trigsrcNone)
    
    # set starting position and prefill
    position = min(buffer_size, max(0, position))
    dwf.FDwfDigitalInTriggerPositionSet(device_handle, ctypes.c_int(buffer_size - position))
    dwf.FDwfDigitalInTriggerPrefillSet(device_handle, ctypes.c_int(position))

    # set trigger condition
    channel = ctypes.c_int(1 << channel)
    if rising_edge:
        dwf.FDwfDigitalInTriggerSet(device_handle, channel, ctypes.c_int(0), ctypes.c_int(0), ctypes.c_int(0))
        dwf.FDwfDigitalInTriggerResetSet(device_handle, ctypes.c_int(0), ctypes.c_int(0), ctypes.c_int(0), channel)
    else:
        dwf.FDwfDigitalInTriggerSet(device_handle, ctypes.c_int(0), channel, ctypes.c_int(0), ctypes.c_int(0))
        dwf.FDwfDigitalInTriggerResetSet(device_handle, ctypes.c_int(0), ctypes.c_int(0), channel, ctypes.c_int(0))
    
    # set auto triggering
    dwf.FDwfDigitalInTriggerAutoTimeoutSet(device_handle, ctypes.c_double(timeout))
    
    # set sequence length to activate trigger
    dwf.FDwfDigitalInTriggerLengthSet(device_handle, ctypes.c_double(length_min), ctypes.c_double(length_max), ctypes.c_int(0))

    # set event counter
    dwf.FDwfDigitalInTriggerCountSet(device_handle, ctypes.c_int(count), ctypes.c_int(0))
    return
