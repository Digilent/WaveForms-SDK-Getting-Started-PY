def set_mode(device_handle, channel, output):
    """
        set a DIO line as input, or as output

        parameters: - device handle
                    - selected DIO channel number
                    - True means output, False means input
    """
    # load current state of the output enable buffer
    mask = ctypes.c_uint16()
    dwf.FDwfDigitalIOOutputEnableGet(device_handle, ctypes.byref(mask))
    
    # convert mask to list
    mask = list(bin(mask.value)[2:].zfill(16))
    
    # set bit in mask
    if output:
        mask[15 - channel] = "1"
    else:
        mask[15 - channel] = "0"
    
    # convert mask to number
    mask = "".join(element for element in mask)
    mask = int(mask, 2)
    
    # set the pin to output
    dwf.FDwfDigitalIOOutputEnableSet(device_handle, ctypes.c_int(mask))
    return
