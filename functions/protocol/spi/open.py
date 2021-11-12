def open(device_handle, cs, sck, miso=None, mosi=None, clk_frequency=1e06, mode=0, order=True):
    """
        initializes SPI communication

        parameters: - device handle
                    - cs (DIO line used for chip select)
                    - sck (DIO line used for serial clock)
                    - miso (DIO line used for master in - slave out, optional)
                    - mosi (DIO line used for master out - slave in, optional)
                    - frequency (communication frequency in Hz, default is 1MHz)
                    - mode (SPI mode: 0: CPOL=0, CPHA=0; 1: CPOL-0, CPHA=1; 2: CPOL=1, CPHA=0; 3: CPOL=1, CPHA=1)
                    - order (endianness, True means MSB first - default, False means LSB first)
    """
    # set the clock frequency
    dwf.FDwfDigitalSpiFrequencySet(device_handle, ctypes.c_double(clk_frequency))

    # set the clock pin
    dwf.FDwfDigitalSpiClockSet(device_handle, ctypes.c_int(sck))

    if mosi != None:
        # set the mosi pin
        dwf.FDwfDigitalSpiDataSet(device_handle, ctypes.c_int(0), ctypes.c_int(mosi))

        # set the initial state
        dwf.FDwfDigitalSpiIdleSet(device_handle, ctypes.c_int(0), constants.DwfDigitalOutIdleZet)

    if miso != None:
        # set the miso pin
        dwf.FDwfDigitalSpiDataSet(device_handle, ctypes.c_int(1), ctypes.c_int(miso))

        # set the initial state
        dwf.FDwfDigitalSpiIdleSet(device_handle, ctypes.c_int(1), constants.DwfDigitalOutIdleZet)

    # set the SPI mode
    dwf.FDwfDigitalSpiModeSet(device_handle, ctypes.c_int(mode))

    # set endianness
    if order:
        # MSB first
        dwf.FDwfDigitalSpiOrderSet(device_handle, ctypes.c_int(1))
    else:
        # LSB first
        dwf.FDwfDigitalSpiOrderSet(device_handle, ctypes.c_int(0))

    # set the cs pin HIGH
    dwf.FDwfDigitalSpiSelect(device_handle, ctypes.c_int(cs), ctypes.c_int(1))

    # dummy write
    dwf.FDwfDigitalSpiWriteOne(device_handle, ctypes.c_int(1), ctypes.c_int(0), ctypes.c_int(0))
    
    return
