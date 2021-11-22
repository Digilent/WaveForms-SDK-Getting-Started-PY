def write(device_handle, data, address):
    """
        send data through I2C
        
        parameters: - device handle
                    - data of type string, int, or list of characters/integers
                    - address (8-bit address of the slave device)
                    
        returns:    - error message or empty string
    """
    # cast data
    if type(data) == int:
        data = "".join(chr(data))
    elif type(data) == list:
        data = "".join(chr(element) for element in data)

    # encode the string into a string buffer
    data = bytes(data, "utf-8")
    buffer = (ctypes.c_ubyte * len(data))()
    for index in range(0, len(buffer)):
        buffer[index] = ctypes.c_ubyte(data[index])

    # send
    nak = ctypes.c_int()
    dwf.FDwfDigitalI2cWrite(device_handle, ctypes.c_int(address << 1), buffer, ctypes.c_int(ctypes.sizeof(buffer)), ctypes.byref(nak))

    # check for not acknowledged
    if nak.value != 0:
        return "NAK: index " + str(nak.value)
    
    return ""
