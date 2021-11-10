def set_pull(device_handle, channel, direction):
    """
        pull a DIO line up, or down

        parameters: - device handle
                    - selected DIO channel number between 0-15
                    - direction: True means HIGH, False means LOW, None means idle
    """
    
    # encode direction
    if direction == True:
        direction = ctypes.c_double(1)
    elif direction == False:
        direction = ctypes.c_double(0)
    else:
        direction = ctypes.c_double(0.5)

    # get pull enable mask
    mask = ctypes.c_uint16()
    dwf.FDwfAnalogIOChannelNodeGet(device_handle, ctypes.c_int(0), ctypes.c_int(2), ctypes.byref(mask))

    # convert mask to list
    mask = list(bin(mask.value)[2:].zfill(16))
    
    # set bit in mask
    if direction.value == 0.5:
        mask[15 - channel] = "0"
    else:
        mask[15 - channel] = "1"
    
    # convert mask to number
    mask = "".join(element for element in mask)
    mask = int(mask, 2)

    # set pull enable mask
    dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(0), ctypes.c_int(2), ctypes.c_int(mask))
    
    # set direction if necessary
    if direction.value != 0.5:
        # get direction mask
        mask = ctypes.c_uint16()
        dwf.FDwfAnalogIOChannelNodeGet(device_handle, ctypes.c_int(0), ctypes.c_int(3), ctypes.byref(mask))

        # convert mask to list
        mask = list(bin(mask.value)[2:].zfill(16))
        
        # set bit in mask
        if direction.value == 1:
            mask[15 - channel] = "1"
        elif direction.value == 0:
            mask[15 - channel] = "0"
        
        # convert mask to number
        mask = "".join(element for element in mask)
        mask = int(mask, 2)

        # set direction mask
        dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(0), ctypes.c_int(3), ctypes.c_int(mask))

    return
