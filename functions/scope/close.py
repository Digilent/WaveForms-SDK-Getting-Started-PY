def close(device_handle):
    """
        reset the scope
    """
    dwf.FDwfAnalogInReset(device_handle)
    return
