def open(device_handle, sda, scl, clk_rate=100e03, stretching=True):
    """
        initializes I2C communication

        parameters: - device handle
                    - sda (DIO line used for data)
                    - scl (DIO line used for clock)
                    - rate (clock frequency in Hz, default is 100KHz)
                    - stretching (enables/disables clock stretching)

        returns:    - error message or empty string
    """
    # reset the interface
    dwf.FDwfDigitalI2cReset(device_handle)

    # clock stretching
    if stretching:
        dwf.FDwfDigitalI2cStretchSet(device_handle, ctypes.c_int(1))
    else:
        dwf.FDwfDigitalI2cStretchSet(device_handle, ctypes.c_int(0))

    # set clock frequency
    dwf.FDwfDigitalI2cRateSet(device_handle, ctypes.c_double(clk_rate))

    #  set communication lines
    dwf.FDwfDigitalI2cSclSet(device_handle, ctypes.c_int(scl))
    dwf.FDwfDigitalI2cSdaSet(device_handle, ctypes.c_int(sda))

    # check bus
    nak = ctypes.c_int()
    dwf.FDwfDigitalI2cClear(device_handle, ctypes.byref(nak))
    if nak.value == 0:
        return "Error: I2C bus lockup"


    # write 0 bytes
    dwf.FDwfDigitalI2cWrite(device_handle, ctypes.c_int(0), ctypes.c_int(0), ctypes.c_int(0), ctypes.byref(nak))
    if nak.value != 0:
        return "NAK: index " + str(nak.value)
    
    return ""
