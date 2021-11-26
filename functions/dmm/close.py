def close(device_handle):
    """
        reset the instrument
    """
    # disable the DMM
    dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(3), ctypes.c_int(0), ctypes.c_double(0))
    # reset the instrument
    dwf.FDwfAnalogIOReset(device_handle)
    return
