def trigger(device_handle, enable, source=constants.trigsrcNone, channel=1, timeout=0, edge_rising=True, level=0):
    """
        set up triggering

        parameters: - device handle
                    - enable / disable triggering with True/False
                    - trigger source - possible: none, analog, digital, external[1-4]
                    - trigger channel - possible options: 1-4 for analog, or 0-15 for digital
                    - auto trigger timeout in seconds, default is 0
                    - trigger edge rising - True means rising, False means falling, default is rising
                    - trigger level in Volts, default is 0V
    """
    if enable and source != constants.trigsrcNone:
        # enable/disable auto triggering
        dwf.FDwfAnalogInTriggerAutoTimeoutSet(device_handle, ctypes.c_double(timeout))

        # set trigger source
        dwf.FDwfAnalogInTriggerSourceSet(device_handle, source)

        # set trigger channel
        if source == constants.trigsrcDetectorAnalogIn:
            channel -= 1    # decrement analog channel index
        dwf.FDwfAnalogInTriggerChannelSet(device_handle, ctypes.c_int(channel))

        # set trigger type
        dwf.FDwfAnalogInTriggerTypeSet(device_handle, constants.trigtypeEdge)

        # set trigger level
        dwf.FDwfAnalogInTriggerLevelSet(device_handle, ctypes.c_double(level))

        # set trigger edge
        if edge_rising:
            # rising edge
            dwf.FDwfAnalogInTriggerConditionSet(device_handle, constants.trigcondRisingPositive)
        else:
            # falling edge
            dwf.FDwfAnalogInTriggerConditionSet(device_handle, constants.trigcondFallingNegative)
    else:
        # turn off the trigger
        dwf.FDwfAnalogInTriggerSourceSet(device_handle, constants.trigsrcNone)
    return
