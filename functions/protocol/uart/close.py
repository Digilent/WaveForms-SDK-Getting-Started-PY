def close(device_handle):
    """
        reset the uart interface
    """
    dwf.FDwfDigitalUartReset(device_handle)
    return
