def close(device_handle):
    """
        reset the instrument
    """
    dwf.FDwfDigitalOutReset(device_handle)
    return
