def close(device_handle):
    """
        reset the supplies
    """
    dwf.FDwfAnalogIOReset(device_handle)
    return
