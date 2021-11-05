def close(device_handle):
    """
        close a specific device
    """
    dwf.FDwfDeviceClose(device_handle)
    return
