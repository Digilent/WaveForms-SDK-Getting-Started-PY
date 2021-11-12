def close(device_handle):
    """
        reset the spi interface
    """
    dwf.FDwfDigitalSpiReset(device_handle)
    return
