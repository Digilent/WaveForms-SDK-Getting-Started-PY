# user defined variables
buffer_size = 4096            # data points in a recording
trigger_enable = True         # enable/disable the trigger
trigger_position = 0          # how many bits should be read before the trigger event
trigger_timeout = 2           # in seconds
trigger_pin = 0               # DIO line used as trigger
trigger_edge_rising = True    # set True for rising edge, False for falling edge
trigger_length_min = 0        # trigger only on sequences longer than 0s (between 0s-20s)
trigger_length_max = 20       # trigger only on sequences shorter than 20s (between 0s-20s)
trigger_count = 1             # trigger event counter


# set trigger source to digital I/O lines, or turn it off
if trigger_enable:
    dwf.FDwfDigitalInTriggerSourceSet(hdwf, constants.trigsrcDetectorDigitalIn)
else:
    dwf.FDwfDigitalInTriggerSourceSet(hdwf, constants.trigsrcNone)
 
# set starting position and prefill
trigger_position = min(buffer_size, max(0, trigger_position))
dwf.FDwfDigitalInTriggerPositionSet(hdwf, ctypes.c_int(buffer_size - trigger_position))
dwf.FDwfDigitalInTriggerPrefillSet(hdwf, ctypes.c_int(trigger_position))

# set trigger condition
trigger_pin = ctypes.c_int(1 << trigger_pin)
if trigger_edge_rising:
    dwf.FDwfDigitalInTriggerSet(hdwf, ctypes.c_int(0), trigger_pin, ctypes.c_int(0), ctypes.c_int(0))
    dwf.FDwfDigitalInTriggerResetSet(hdwf, ctypes.c_int(0), ctypes.c_int(0), trigger_pin, ctypes.c_int(0))
else:
    dwf.FDwfDigitalInTriggerSet(hdwf, trigger_pin, ctypes.c_int(0), ctypes.c_int(0), ctypes.c_int(0))
    dwf.FDwfDigitalInTriggerResetSet(hdwf, ctypes.c_int(0), ctypes.c_int(0), ctypes.c_int(0), trigger_pin)
 
# set auto triggering
dwf.FDwfDigitalInTriggerAutoTimeoutSet(hdwf, ctypes.c_double(trigger_timeout))
 
# set sequence length to activate trigger
dwf.FDwfDigitalInTriggerLengthSet(hdwf, ctypes.c_double(trigger_length_min), ctypes.c_double(trigger_length_max), ctypes.c_int(0))

# set event counter
dwf.FDwfDigitalInTriggerCountSet(hdwf, ctypes.c_int(trigger_count), ctypes.c_int(0))
