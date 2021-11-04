# user defined variables
frequency = 10e03                                     # signal frequency in Hz
channel = 3                                           # select a DIO line - DIO3 in this case
function = constants.DwfDigitalOutTypePulse           # possible: DwfDigitalOutTypePulse, DwfDigitalOutTypeCustom, DwfDigitalOutTypeRandom
wait_time = 0                                         # in seconds
repeat = 0                                            # repeat count, 0 means infinite
trigger_enabled = False                               # enable/disable trigger in repeat cycle
trigger_source = constants.trigsrcNone                # possible: trigsrcDetectorDigitalIn, trigsrcNone, trigsrcDetectorAnalogIn,
                                                                # trigsrcExternal1, trigsrcExternal2, trigsrcExternal3, trigsrcExternal4
trigger_edge = constants.DwfTriggerSlopeRise          # possible: DwfTriggerSlopeRise, DwfTriggerSlopeFall, DwfTriggerSlopeEither
duty_cycle = 50                                       # duty cycle of the signal in percentage, used only if function = constants.DwfDigitalOutTypePulse
data = [1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0]           # custom data list, used only if function = constants.DwfDigitalOutTypeCustom


# get internal clock frequency
internal_frequency = ctypes.c_double()
dwf.FDwfDigitalOutInternalClockInfo(hdwf, ctypes.byref(internal_frequency))
 
# get counter value range
counter_limit = ctypes.c_uint()
dwf.FDwfDigitalOutCounterInfo(hdwf, ctypes.c_int(0), ctypes.c_int(0), ctypes.byref(counter_limit))
 
# calculate the divider for the given signal frequency
divider = int(-(-(internal_frequency.value / frequency) // counter_limit.value))
 
# enable the respective channel
dwf.FDwfDigitalOutEnableSet(hdwf, ctypes.c_int(channel), ctypes.c_int(1))
 
# set output type
dwf.FDwfDigitalOutTypeSet(hdwf, ctypes.c_int(channel), function)
 
# set frequency
dwf.FDwfDigitalOutDividerSet(hdwf, ctypes.c_int(channel), ctypes.c_int(divider))
 
# set wait time
dwf.FDwfDigitalOutWaitSet(hdwf, ctypes.c_double(wait_time))
 
# set repeat count
dwf.FDwfDigitalOutRepeatSet(hdwf, ctypes.c_int(repeat))
 
# enable triggering
dwf.FDwfDigitalOutRepeatTriggerSet(hdwf, ctypes.c_int(trigger_enabled))
 
# set trigger source
if not trigger_enabled:
    dwf.FDwfDigitalOutTriggerSourceSet(hdwf, trigger_source)
 
# set trigger slope
dwf.FDwfDigitalOutTriggerSlopeSet(hdwf, trigger_edge)
 
# set PWM signal duty cycle
if function == constants.DwfDigitalOutTypePulse:
    # set duty cycle
    # calculate counter steps to get the required frequency
    steps = int(round(internal_frequency.value / frequency / divider))
    # calculate steps for low and high parts of the period
    high_steps = int(steps * duty_cycle / 100)
    low_steps = int(steps - high_steps)
    dwf.FDwfDigitalOutCounterSet(hdwf, ctypes.c_int(channel), ctypes.c_int(low_steps), ctypes.c_int(high_steps))
 
# load custom signal data
elif function == constants.DwfDigitalOutTypeCustom:
    # format data
    buffer = (ctypes.c_ubyte * ((len(data) + 7) >> 3))(0)
    for index in range(len(data)):
        if data[index] != 0:
            buffer[index >> 3] |= 1 << (index & 7)
 
    # load data
    dwf.FDwfDigitalOutDataSet(hdwf, ctypes.c_int(channel), ctypes.byref(buffer), ctypes.c_int(len(data)))
 
# start generating the signal
dwf.FDwfDigitalOutConfigure(hdwf, ctypes.c_int(True))
