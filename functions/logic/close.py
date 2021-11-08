def close(device_handle):
    """
        reset the instrument
    """
    dwf.FDwfDigitalInReset(device_handle)
    return
