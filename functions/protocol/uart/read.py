def receive(device_handle):
    """
        receives data from UART
        
        parameters: - device handle

        return:     - string containing the received bytes
                    - error message or empty string
    """
    # variable to store errors
    error = ""

    # create empty string buffer
    data = ctypes.create_string_buffer(8193)

    # character counter
    count = ctypes.c_int(0)

    # parity flag
    parity_flag= ctypes.c_int(0)

    # read up to 8k characters
    dwf.FDwfDigitalUartRx(device_handle, data, ctypes.c_int(ctypes.sizeof(data)-1), ctypes.byref(count), ctypes.byref(parity_flag))

    data[count.value] = 0  # add zero ending
    
    # make a string from the string buffer
    data = list(data.value)
    previous_data_chunk = "".join(chr(element) for element in data)

    # ensure data integrity
    while count.value > 0:
        # create empty string buffer
        data = ctypes.create_string_buffer(8193)

        # character counter
        count = ctypes.c_int(0)

        # parity flag
        parity_flag= ctypes.c_int(0)

        # read up to 8k characters
        dwf.FDwfDigitalUartRx(device_handle, data, ctypes.c_int(ctypes.sizeof(data)-1), ctypes.byref(count), ctypes.byref(parity_flag))

        data[count.value] = 0  # add zero ending
        
        # make a string from the string buffer
        data = list(data.value)
        data = "".join(chr(element) for element in data)

        # attach to previous data
        previous_data_chunk = previous_data_chunk + data

        # check for not acknowledged
        if error == "":
            if parity_flag.value < 0:
                error = "Buffer overflow"
            elif parity_flag.value > 0:
                error = "Parity error: index {}".format(parity_flag.value)

    return previous_data_chunk, error
