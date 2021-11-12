def close(device_handle):
    """
        reset the i2c interface
    """
    dwf.FDwfDigitalI2cReset(device_handle)
    return
