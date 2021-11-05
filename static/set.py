def set_state(device_handle, channel, state):
    """
        set a DIO line as input, or as output

        parameters: - device handle
                    - selected DIO channel number
                    - True means HIGH, False means LOW
    """
    # load current state of the output state buffer
    mask = ctypes.c_uint16()
    dwf.FDwfDigitalIOOutputGet(device_handle, ctypes.byref(mask))
    
    # convert mask to list
    mask = list(bin(mask.value)[2:].zfill(16))
    
    # set bit in mask
    if state:
        mask[15 - channel] = "1"
    else:
        mask[15 - channel] = "0"
    
    # convert mask to number
    mask = "".join(element for element in mask)
    mask = int(mask, 2)
    
    # set the pin state
    dwf.FDwfDigitalIOOutputSet(device_handle, ctypes.c_int(mask))
    return
