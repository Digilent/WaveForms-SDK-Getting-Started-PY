def exchange(device_handle, data, count, cs):
    """
        sends and receives data using the SPI interface
        
        parameters: - device handle
                    - data of type string, int, or list of characters/integers
                    - count (number of bytes to receive)
                    - chip select line number
        
        return:     - integer list containing the received bytes
    """
    # cast data
    if type(data) == int:
        data = "".join(chr(data))
    elif type(data) == list:
        data = "".join(chr(element) for element in data)

    # enable the chip select line
    dwf.FDwfDigitalSpiSelect(device_handle, ctypes.c_int(cs), ctypes.c_int(0))

    # create buffer to write
    data = bytes(data, "utf-8")
    tx_buffer = (ctypes.c_ubyte * len(data))()
    for index in range(0, len(tx_buffer)):
        tx_buffer[index] = ctypes.c_ubyte(data[index])

    # create buffer to store data
    rx_buffer = (ctypes.c_ubyte*count)()

    # write to MOSI and read from MISO
    dwf.FDwfDigitalSpiWriteRead(device_handle, ctypes.c_int(1), ctypes.c_int(8), tx_buffer, ctypes.c_int(len(tx_buffer)), rx_buffer, ctypes.c_int(len(rx_buffer)))

    # disable the chip select line
    dwf.FDwfDigitalSpiSelect(device_handle, ctypes.c_int(cs), ctypes.c_int(1))

    # decode data
    data = [int(element) for element in rx_buffer]

    return data
