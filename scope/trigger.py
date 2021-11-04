# user defined variables
trigger_timeout = 0                                  # auto trigger timeout - 0 disables autotriggering
trigger_source = constants.trigsrcDetectorAnalogIn   # possible: trigsrcNone, trigsrcDetectorAnalogIn, trigsrcDetectorDigitalIn, 
                                                               # trigsrcExternal1, trigsrcExternal2, trigsrcExternal3, trigsrcExternal4
trigger_channel = 0                                  # scope channel 1, possible options: 0-3 for trigsrcDetectorAnalogIn,
                                                               # or 0-15 for trigsrcDetectorDigitalIn
trigger_type = constants.trigtypeTransition          # possible: trigtypeEdge, trigtypePulse, trigtypeTransition
trigger_level = 0                                    # trigger level in Volts
trigger_edge = constants.trigcondRisingPositive      # possible: trigcondRisingPositive, rigcondFallingNegative


# enable/disable auto triggering
dwf.FDwfAnalogInTriggerAutoTimeoutSet(hdwf, ctypes.c_double(trigger_timeout))
 
# set trigger source
dwf.FDwfAnalogInTriggerSourceSet(hdwf, trigger_source)
 
# set trigger channel
dwf.FDwfAnalogInTriggerChannelSet(hdwf, ctypes.c_int(trigger_channel))
 
# set trigger type
dwf.FDwfAnalogInTriggerTypeSet(hdwf, trigger_type)
 
# set trigger level
dwf.FDwfAnalogInTriggerLevelSet(hdwf, ctypes.c_double(trigger_level))
 
# set trigger edge
dwf.FDwfAnalogInTriggerConditionSet(hdwf, trigger_edge)
