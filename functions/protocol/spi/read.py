def read(device_handle, count, cs):
    """
        receives data from SPI

        parameters: - device handle
                    - count (number of bytes to receive)
                    - chip select line number

        return:     - integer list containing the received bytes
    """
    # enable the chip select line
    dwf.FDwfDigitalSpiSelect(device_handle, ctypes.c_int(cs), ctypes.c_int(0))

    # create buffer to store data
    buffer = (ctypes.c_ubyte*count)()

    # read array of 8 bit elements
    dwf.FDwfDigitalSpiRead(device_handle, ctypes.c_int(1), ctypes.c_int(8), buffer, ctypes.c_int(len(buffer)))

    # disable the chip select line
    dwf.FDwfDigitalSpiSelect(device_handle, ctypes.c_int(cs), ctypes.c_int(1))

    # decode data
    data = [int(element) for element in buffer]

    return data
