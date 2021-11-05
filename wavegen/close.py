def close(device_handle):
    """
        reset the wavegen
    """
    dwf.FDwfAnalogOutReset(device_handle)
    return
