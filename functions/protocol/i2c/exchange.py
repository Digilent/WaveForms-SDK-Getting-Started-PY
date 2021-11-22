def exchange(device_handle, data, count, address):
    """
        sends and receives data using the I2C interface
        
        parameters: - device handle
                    - data of type string, int, or list of characters/integers
                    - count (number of bytes to receive)
                    - address (8-bit address of the slave device)
        
        return:     - integer list containing the received bytes
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
    data = bytes(data, "utf-8")
    tx_buffer = (ctypes.c_ubyte * len(data))()
    for index in range(0, len(tx_buffer)):
        tx_buffer[index] = ctypes.c_ubyte(data[index])

    # send and receive
    nak = ctypes.c_int()
    dwf.FDwfDigitalI2cWriteRead(device_handle, ctypes.c_int(address << 1), tx_buffer, ctypes.c_int(ctypes.sizeof(tx_buffer)), buffer, ctypes.c_int(count), ctypes.byref(nak))

    # decode data
    rec_data = [int(element) for element in buffer]

    # check for not acknowledged
    if nak.value != 0:
        return rec_data, "NAK: index " + str(nak.value)
    
    return rec_data, ""
