def spy(device_handle, count = 16):
    """
        receives data from I2C
        
        parameters: - device handle
                    - count (number of bytes to receive), default is 16
        
        return:     - class containing the received data: start, address, direction, message, stop
                    - error message or empty string
    """
    # variable to store the errors
    error = ""

    # variable to store the data
    class message:
        start = ""
        address = 0
        direction = ""
        data = ""
        stop = ""

    # start the interfcae
    dwf.FDwfDigitalI2cSpyStart(device_handle)

    # read data
    start = ctypes.c_int()
    stop = ctypes.c_int()
    data = (ctypes.c_ubyte * count)()
    count = ctypes.c_int(count)
    nak = ctypes.c_int()
    if dwf.FDwfDigitalI2cSpyStatus(device_handle, ctypes.byref(start), ctypes.byref(stop), ctypes.byref(data), ctypes.byref(count), ctypes.byref(nak)) == 0:
        error = "Communication with the device failed."
    
    # decode data
    if start.value != 0:

        # start condition
        if start.value == 1:
            message.start = "Start"
        elif start.value == 2:
            message.start = "Restart"

        # get address
        message.address = hex(data[0] >> 1)

        # decide message direction
        if data[0] & 1 == 0:
            message.direction = "Write"
        else:
            message.direction = "Read"
        
        # get message
        message.data = [str(bin(element))[3:] for element in data]
        message.data = [int(element, 2) for element in message.data]
        message.data = "".join(chr(element) for element in message.data)

        if stop.value != 0:
            message.stop = "Stop"

    # check for not acknowledged
    if nak.value != 0 and error == "":
        error = "NAK: index " + str(nak.value)
    
    return message, error
