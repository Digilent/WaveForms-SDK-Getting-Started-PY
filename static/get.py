def get_state(device_handle, channel):
    """
        get the state of a DIO line

        parameters: - device handle
                    - selected DIO channel number

        returns:    - True if the channel is HIGH, or False, if the channel is LOW
    """
    # load internal buffer with current state of the pins
    dwf.FDwfDigitalIOStatus(device_handle)
    
    # get the current state of the pins
    data = ctypes.c_uint32()  # variable for this current state
    dwf.FDwfDigitalIOInputStatus(device_handle, ctypes.byref(data))
    
    # convert the state to a 16 character binary string
    data = list(bin(data.value)[2:].zfill(16))
    
    # check the required bit
    if data[15 - channel] != "0":
        state = True
    else:
        state = False
    return state
