def open(device=None):
    """
        open a specific device

        parameters: - device type: None (first device), "Analog Discovery", "Analog Discovery 2", "Analog Discovery Studio", "Digital Discovery" and "Analog Discovery Pro 3X50"
    
        returns:    - the device handle
                    - the device name
    """
    device_names = [("Analog Discovery", constants.devidDiscovery), ("Analog Discovery 2", constants.devidDiscovery2),
                    ("Analog Discovery Studio", constants.devidDiscovery2), ("Digital Discovery", constants.devidDDiscovery),
                    ("Analog Discovery Pro 3X50", constants.devidADP3X50)]
    
    # decode device names
    device_type = constants.enumfilterAll
    for pair in device_names:
        if pair[0] == device:
            device_type = pair[1]
            break

    # count devices
    device_count = ctypes.c_int()
    dwf.FDwfEnum(device_type, ctypes.byref(device_count))

    # check for connected devices
    if device_count.value <= 0:
        if device_type.value == 0:
            print("Error: There are no connected devices")
        else:
            print("Error: There is no " + device + " connected")
        quit()

    # this is the device handle - it will be used by all functions to "address" the connected device
    device_handle = ctypes.c_int(0)

    # connect to the first available device
    index = 0
    while device_handle.value == 0 and index < device_count.value:
        dwf.FDwfDeviceOpen(ctypes.c_int(index), ctypes.byref(device_handle))
        index += 1  # increment the index and try again if the device is busy

    # check connected device type
    device_name = ""
    if device_handle.value != 0:
        device_id = ctypes.c_int()
        device_rev = ctypes.c_int()
        dwf.FDwfEnumDeviceType(ctypes.c_int(index - 1), ctypes.byref(device_id), ctypes.byref(device_rev))

        # decode device id
        for pair in device_names:
            if pair[1].value == device_id.value:
                device_name = pair[0]
                break

    return device_handle, device_name
