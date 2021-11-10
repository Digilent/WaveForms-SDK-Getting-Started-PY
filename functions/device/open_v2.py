def open(device=None):
    """
        open a specific device

        parameters: - device type: None (first device), "Analog Discovery", "Analog Discovery 2", "Analog Discovery Studio", "Digital Discovery" and "Analog Discovery Pro 3X50"
    """
    # check required device
    if device != None:
        # get connected devices list
        device_count = ctypes.c_int()
        dwf.FDwfEnum(ctypes.c_int(0), ctypes.byref(device_count))

        # decode required device type
        if device == "Analog Discovery":
            device_type = constants.devidDiscovery
        elif device == "Analog Discovery 2" or device == "Analog Discovery Studio":
            device_type = constants.devidDiscovery2
        elif device == "Digital Discovery":
            device_type = constants.devidDDiscovery
        elif device == "Analog Discovery Pro 3x50":
            device_type = constants.devidADP3X50
        else:
            print("Error: No such device")
            quit()

        # go through the list of devices
        index = -1
        for device_index in range(0, device_count.value):
            # get device type
            device_id = ctypes.c_int()
            device_rev = ctypes.c_int()
            dwf.FDwfEnumDeviceType(ctypes.c_int(device_index), ctypes.byref(device_id), ctypes.byref(device_rev))

            # save index on match
            if device_id.value == device_type.value:
                index = device_index
                break

        # check for mathces
        if index == -1:
            print("Error: No " + device + " is connected")
            quit()
        
    else:
        # connect to the first device
        index = -1

    # this is the device handle - it will be used by all functions to "address" the connected device
    device_handle = ctypes.c_int()

    # connect to the first available device
    dwf.FDwfDeviceOpen(ctypes.c_int(index), ctypes.byref(device_handle))
    return device_handle
