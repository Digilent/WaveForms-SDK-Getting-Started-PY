def measure(device_handle, mode, ac=False, range=0, high_impedance=False):
    """
        measure a voltage/current/resistance/continuity/temperature

        parameters: - device handler
                    - mode: "voltage", "low current", "high current", "resistance", "continuity", "diode", "temperature"
                    - ac: True means AC value, False means DC value, default is DC
                    - range: voltage/current/resistance/temperature range, 0 means auto, default is auto
                    - high_impedance: input impedance for DC voltage measurement, False means 10MΩ, True means 10GΩ, default is 10MΩ
        
        returns:    - the measured value in V/A/Ω/°C, or None on error
    """
    # set voltage mode
    if mode == "voltage":
        # set coupling
        if ac:
            dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(3), ctypes.c_int(1), constants.DwfDmmACVoltage)
        else:
            dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(3), ctypes.c_int(1), constants.DwfDmmDCVoltage)

        # set input impedance
        if high_impedance:
            dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(3), ctypes.c_int(5), ctypes.c_double(1))
        else:
            dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(3), ctypes.c_int(5), ctypes.c_double(0))

    # set high current mode
    elif mode == "high current":
        # set coupling
        if ac:
            dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(3), ctypes.c_int(1), constants.DwfDmmACCurrent)
        else:
            dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(3), ctypes.c_int(1), constants.DwfDmmDCCurrent)

    # set low current mode
    elif mode == "low current":
        # set coupling
        if ac:
            dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(3), ctypes.c_int(1), constants.DwfDmmACLowCurrent)
        else:
            dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(3), ctypes.c_int(1), constants.DwfDmmDCLowCurrent)
            
    # set resistance mode
    elif mode == "resistance":
        dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(3), ctypes.c_int(1), constants.DwfDmmResistance)

    # set continuity mode
    elif mode == "continuity":
        dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(3), ctypes.c_int(1), constants.DwfDmmContinuity)

    # set diode mode
    elif mode == "diode":
        dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(3), ctypes.c_int(1), constants.DwfDmmDiode)

    # set temperature mode
    elif mode == "temperature":
        dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(3), ctypes.c_int(1), constants.DwfDmmTemperature)
        
    # set range
    dwf.FDwfAnalogIOChannelNodeSet(device_handle, ctypes.c_int(3), ctypes.c_int(2), ctypes.c_double(range))

    # fetch analog I/O status
    if dwf.FDwfAnalogIOStatus(device_handle) == 0:
        # signal error
        return None

    # get reading
    measurement = ctypes.c_double()
    dwf.FDwfAnalogIOChannelNodeStatus(device_handle, ctypes.c_int(3), ctypes.c_int(3), ctypes.byref(measurement))

    return measurement.value
