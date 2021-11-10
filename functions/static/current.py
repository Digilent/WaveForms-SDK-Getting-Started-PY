def set_current(device_handle, current):
    """
        limit the output current of the DIO lines

        parameters: - device handle
                    - current limit in mA: possible values are 2, 4, 6, 8, 12 and 16mA
    """
    # clamp current
    current = max(2, min(16, current))

    # round
    current = round(current)

    # discard odd values
    if current % 2 != 0:
        current -= 1

    # discard unavailable even values
    if current == 10:
        current = 12
    elif current == 14:
        current = 16

    # set limit  
    dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(0), ctypes.c_int(4), ctypes.c_double(current))
    return
