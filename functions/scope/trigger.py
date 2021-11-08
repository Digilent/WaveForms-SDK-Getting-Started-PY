def trigger(device_handle, enable, source=constants.trigsrcNone, channel=0, timeout=0, type=constants.trigtypeTransition, edge=constants.trigcondRisingPositive, level=0):
    """
        set up triggering

        parameters: - device handle
                    - enable / disable triggering with True/False
                    - trigger source - possible: trigsrcNone, trigsrcDetectorAnalogIn, trigsrcDetectorDigitalIn, trigsrcExternal1, trigsrcExternal2, trigsrcExternal3, trigsrcExternal4
                    - trigger channel - possible options: 0-3 for trigsrcDetectorAnalogIn, or 0-15 for trigsrcDetectorDigitalIn
                    - auto trigger timeout in seconds, default is 0
                    - event type - possible: trigtypeEdge, trigtypePulse, trigtypeTransition, default is transition
                    - trigger edge - possible: trigcondRisingPositive, rigcondFallingNegative, default is rising
                    - trigger level in Volts, default is 0V
    """
    if enable and source != constants.trigsrcNone:
        # enable/disable auto triggering
        dwf.FDwfAnalogInTriggerAutoTimeoutSet(device_handle, ctypes.c_double(timeout))

        # set trigger source
        dwf.FDwfAnalogInTriggerSourceSet(device_handle, source)

        # set trigger channel
        dwf.FDwfAnalogInTriggerChannelSet(device_handle, ctypes.c_int(channel))

        # set trigger type
        dwf.FDwfAnalogInTriggerTypeSet(device_handle, type)

        # set trigger level
        dwf.FDwfAnalogInTriggerLevelSet(device_handle, ctypes.c_double(level))

        # set trigger edge
        dwf.FDwfAnalogInTriggerConditionSet(device_handle, edge)
    else:
        # turn off the trigger
        dwf.FDwfAnalogInTriggerSourceSet(device_handle, constants.trigsrcNone)
    return
