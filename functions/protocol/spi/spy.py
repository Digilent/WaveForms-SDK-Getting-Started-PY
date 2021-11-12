def spy(device_handle, count, cs, sck, mosi=None, miso=None, word_size=8):
    """
        receives data from SPI

        parameters: - device handle
                    - count (number of bytes to receive)
                    - chip select line number
                    - serial clock line number
                    - master out - slave in - optional
                    - master in - slave out - optional
                    - word size in bits (default is 8)

        returns:    - class containing the received data: mosi, miso
                    - error message or empty string
    """
    # variable to store errors
    error = ""

    # create static data structure
    class message:
        mosi = 0
        miso = 0

    # record mode
    dwf.FDwfDigitalInAcquisitionModeSet(device_handle, constants.acqmodeRecord)

    # for sync mode set divider to -1 
    dwf.FDwfDigitalInDividerSet(device_handle, ctypes.c_int(-1))

    # 8 bit per sample format, DIO 0-7
    dwf.FDwfDigitalInSampleFormatSet(device_handle, ctypes.c_int(8))

    # continuous sampling 
    dwf.FDwfDigitalInTriggerPositionSet(device_handle, ctypes.c_int(-1))

    # in sync mode the trigger is used for sampling condition
    # trigger detector mask: low & high & (rising | falling)
    dwf.FDwfDigitalInTriggerSet(device_handle, ctypes.c_int(0), ctypes.c_int(0), ctypes.c_int((1 << sck) | (1 << cs)), ctypes.c_int(0))
    # sample on clock rising edge for sampling bits, or CS rising edge to detect frames

    # start detection
    dwf.FDwfDigitalInConfigure(device_handle, ctypes.c_bool(0), ctypes.c_bool(1))

    # fill buffer
    status = ctypes.c_byte()
    available = ctypes.c_int()
    lost = ctypes.c_int()
    corrupted = ctypes.c_int()
    dwf.FDwfDigitalInStatus(device_handle, ctypes.c_int(1), ctypes.byref(status))
    dwf.FDwfDigitalInStatusRecord(device_handle, ctypes.byref(available), ctypes.byref(lost), ctypes.byref(corrupted))

    # check data integrity
    if lost.value :
        error = "Samples were lost"
    if corrupted.value :
        error = "Samples could be corrupted"

    # limit data size
    if available.value > count :
        available = ctypes.c_int(count)
    
    # load data from internal buffer
    data = (ctypes.c_uint8 * available)()
    dwf.FDwfDigitalInStatusData(device_handle, data, available)

    # get message
    bit_count = 0
    for index in range(available.value):
        
        # CS low, active
        if (data[index] >> cs) & 1:
            # log leftover bits, frame not multiple of bit count
            if bit_count != 0:
                # convert data
                message.mosi = chr(message.mosi)
                message.miso = chr(message.miso)
                
                return message, error

        # CS low, active
        else:
            bit_count += 1  # increment bit count

            message.mosi <<= 1 # shift existing bits
            message.miso <<= 1

            # check outgoing data
            if (data[index] >> mosi) & 1:
                message.mosi |= 1
            
            # check incoming data
            if (data[index] >> miso) & 1:
                message.miso |= 1

            # got nBits of bits
            if bit_count >= word_size:
                # convert data
                message.mosi = chr(message.mosi)
                message.miso = chr(message.miso)

                return message, error

    # convert data
    message.mosi = chr(message.mosi)
    message.miso = chr(message.miso)

    return message, error
