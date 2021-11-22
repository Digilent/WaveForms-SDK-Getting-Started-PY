def read(device_handle):
    """
        receives data from UART
        
        parameters: - device handle

        return:     - integer list containing the received bytes
                    - error message or empty string
    """
    # variable to store results
    error = ""
    rx_data = []

    # create empty string buffer
    data = (ctypes.c_ubyte * 8193)()

    # character counter
    count = ctypes.c_int(0)

    # parity flag
    parity_flag= ctypes.c_int(0)

    # read up to 8k characters
    dwf.FDwfDigitalUartRx(device_handle, data, ctypes.c_int(ctypes.sizeof(data)-1), ctypes.byref(count), ctypes.byref(parity_flag))

    # append current data chunks
    for index in range(0, count.value):
        rx_data.append(int(data[index]))

    # ensure data integrity
    while count.value > 0:
        # create empty string buffer
        data = (ctypes.c_ubyte * 8193)()

        # character counter
        count = ctypes.c_int(0)

        # parity flag
        parity_flag= ctypes.c_int(0)

        # read up to 8k characters
        dwf.FDwfDigitalUartRx(device_handle, data, ctypes.c_int(ctypes.sizeof(data)-1), ctypes.byref(count), ctypes.byref(parity_flag))
        # append current data chunks
        for index in range(0, count.value):
            rx_data.append(int(data[index]))

        # check for not acknowledged
        if error == "":
            if parity_flag.value < 0:
                error = "Buffer overflow"
            elif parity_flag.value > 0:
                error = "Parity error: index {}".format(parity_flag.value)

    return rx_data, error
