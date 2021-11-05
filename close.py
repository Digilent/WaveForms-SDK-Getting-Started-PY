def close(device_handle):
    """
        close a specific device
    """
    # close the opened connection
    dwf.FDwfDeviceClose(device_handle)
    return
