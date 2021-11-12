def open(device_handle, rx, tx, baud_rate=9600, parity=None, data_bits=8, stop_bits=1):
    """
        initializes UART communication
        
        parameters: - device handle
                    - rx (DIO line used to receive data)
                    - tx (DIO line used to send data)
                    - baud_rate (communication speed, default is 9600 bits/s)
                    - parity possible: None (default), True means even, False means odd
                    - data_bits (default is 8)
                    - stop_bits (default is 1)
    """
    # set baud rate
    dwf.FDwfDigitalUartRateSet(device_handle, ctypes.c_double(baud_rate))

    # set communication channels
    dwf.FDwfDigitalUartTxSet(device_handle, ctypes.c_int(tx))
    dwf.FDwfDigitalUartRxSet(device_handle, ctypes.c_int(rx))

    # set data bit count
    dwf.FDwfDigitalUartBitsSet(device_handle, ctypes.c_int(data_bits))

    # set parity bit requirements
    if parity == True:
        parity = 2
    elif parity == False:
        parity = 1
    else:
        parity = 0
    dwf.FDwfDigitalUartParitySet(device_handle, ctypes.c_int(parity))

    # set stop bit count
    dwf.FDwfDigitalUartStopSet(device_handle, ctypes.c_double(stop_bits))

    # initialize channels with idle levels

    # dummy read
    dummy_buffer = ctypes.create_string_buffer(0)
    dummy_buffer = ctypes.c_int(0)
    dummy_parity_flag = ctypes.c_int(0)
    dwf.FDwfDigitalUartRx(device_handle, dummy_buffer, ctypes.c_int(0), ctypes.byref(dummy_buffer), ctypes.byref(dummy_parity_flag))

    # dummy write
    dwf.FDwfDigitalUartTx(device_handle, dummy_buffer, ctypes.c_int(0))
    
    return
