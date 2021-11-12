def exchange(device_handle, data, count, cs):
    """
        sends and receives data using the SPI interface
        
        parameters: - device handle
                    - data of type string, int, or list of characters/integers
                    - count (number of bytes to receive)
                    - chip select line number
        
        return:     - string containing the received bytes
    """
    # cast data
    if type(data) == int:
        data = "".join(chr(data))
    elif type(data) == list:
        data = "".join(chr(element) for element in data)

    # enable the chip select line
    dwf.FDwfDigitalSpiSelect(device_handle, ctypes.c_int(cs), ctypes.c_int(0))

    # create buffer to write
    tx_buff = (ctypes.c_ubyte * len(data)).from_buffer_copy(data)

    # create buffer to store data
    rx_buff = (ctypes.c_ubyte*count)()

    # write to MOSI and read from MISO
    dwf.FDwfDigitalSpiWriteRead(device_handle, ctypes.c_int(1), ctypes.c_int(8), tx_buff, ctypes.c_int(len(tx_buff)), rx_buff, ctypes.c_int(len(rx_buff)))

    # disable the chip select line
    dwf.FDwfDigitalSpiSelect(device_handle, ctypes.c_int(cs), ctypes.c_int(1))

    # decode data
    data = list(rx_buff.value)
    data = "".join(chr(element) for element in data)

    return data
