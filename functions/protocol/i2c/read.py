def read(device_handle, count, address):
    """
        receives data from I2C
        
        parameters: - device handle
                    - count (number of bytes to receive)
                    - address (8-bit address of the slave device)
        
        return:     - integer list containing the received bytes
                    - error message or empty string
    """
    # create buffer to store data
    buffer = (ctypes.c_ubyte * count)()

    # receive
    nak = ctypes.c_int()
    dwf.FDwfDigitalI2cRead(device_handle, ctypes.c_int(address << 1), buffer, ctypes.c_int(count), ctypes.byref(nak))

    # decode data
    data = [int(element) for element in buffer]

    # check for not acknowledged
    if nak.value != 0:
        return data, "NAK: index " + str(nak.value)
    
    return data, ""
