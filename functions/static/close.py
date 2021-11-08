def close(device_handle):
    """
        reset the instrument
    """
    dwf.FDwfDigitalIOReset(device_handle)
    return
