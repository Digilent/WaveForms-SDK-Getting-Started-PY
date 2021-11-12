def exchange(device_handle, data, count, address):
    """
        sends and receives data using the I2C interface
        
        parameters: - device handle
                    - data of type string, int, or list of characters/integers
                    - count (number of bytes to receive)
                    - address (8-bit address of the slave device)
        
        return:     - string containing the received bytes
                    - error message or empty string
    """
    # create buffer to store data
    buffer = (ctypes.c_ubyte * count)()

    # cast data
    if type(data) == int:
        data = "".join(chr(data))
    elif type(data) == list:
        data = "".join(chr(element) for element in data)

    # encode the string into a string buffer
    data = ctypes.create_string_buffer(data.encode("UTF-8"))

    # send and receive
    nak = ctypes.c_int()
    dwf.FDwfDigitalI2cWriteRead(device_handle, ctypes.c_int(address), data, ctypes.c_int(ctypes.sizeof(data)-1), buffer, ctypes.c_int(count), ctypes.byref(nak))

    # decode data
    rec_data = [str(bin(element))[2:] for element in buffer]
    rec_data = [int(element, 2) for element in rec_data]
    rec_data = "".join(chr(element) for element in rec_data)

    # check for not acknowledged
    if nak.value != 0:
        return rec_data, "NAK: index " + str(nak.value)
    
    return rec_data, ""
