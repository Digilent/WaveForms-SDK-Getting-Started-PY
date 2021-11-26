def open(device_handle):
    """
        initialize the digital multimeter
    """
    # enable the DMM
    dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(3), ctypes.c_int(0), ctypes.c_double(1.0))
    return
