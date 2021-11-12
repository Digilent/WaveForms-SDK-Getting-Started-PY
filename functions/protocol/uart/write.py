def write(device_handle, data):
    """
        send data through UART
        
        parameters: - data of type string, int, or list of characters/integers
    """
    # cast data
    if type(data) == int:
        data = "".join(chr(data))
    elif type(data) == list:
        data = "".join(chr(element) for element in data)

    # encode the string into a string buffer
    data = ctypes.create_string_buffer(data.encode("UTF-8"))

    # send text, trim zero ending
    dwf.FDwfDigitalUartTx(device_handle, data, ctypes.c_int(ctypes.sizeof(data)-1))

    return
