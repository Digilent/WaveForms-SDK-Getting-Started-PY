# user defined variables
buffer_size = 4096            # data points in a recording
trigger_enable = False        # enable/disable the trigger
trigger_position = 0          # how many bits should be read before the trigger event
trigger_timeout = 2           # in seconds
class tr_set:             # trigger set conditions
    low_pin = 0               # trigger when DIO0 becomes LOW and
    high_pin = 4              # DIO4 becomes HIGH and
    rising_pin = None         # 
    falling_pin = 12          # a falling edge on DIO12 is detected
class tr_reset:           # trigger reset conditions
    low_pin = 3               # reset trigger when DIO3 becomes LOW and
    high_pin = None           # 
    rising_pin = 15           # a rising edge on DIO15 is detected
    falling_pin = None        # 
class tr_len:             # trigger sequence length constraints
    length_min = 1e-03        # trigger only on sequences longer than 1ms (between 0s-20s)
    length_max = 20           # trigger only on sequences shorter than 20s (between 0s-20s)


# set trigger source to digital I/O lines, or turn it off
if trigger_enable:
    dwf.FDwfDigitalInTriggerSourceSet(hdwf, constants.trigsrcDetectorDigitalIn)
else:
    dwf.FDwfDigitalInTriggerSourceSet(hdwf, constants.trigsrcNone)
 
# set starting position and prefill
trigger_position = ctypes.c_int(min(buffer_size - 1, max(0, trigger_position)))
dwf.FDwfDigitalInTriggerPositionSet(hdwf, trigger_position)
dwf.FDwfDigitalInTriggerPrefillSet(hdwf, trigger_position)
 
# trigger set condition
# create bitmasks
if tr_set.low_pin == None:
    tr_set.low_pin = ctypes.c_int(0) 
else:
    tr_set.low_pin = ctypes.c_int(1 << tr_set.low_pin)
if tr_set.high_pin == None:
    tr_set.high_pin = ctypes.c_int(0) 
else:
    tr_set.high_pin = ctypes.c_int(1 << tr_set.high_pin)
if tr_set.rising_pin == None:
    tr_set.rising_pin = ctypes.c_int(0) 
else:
    tr_set.rising_pin = ctypes.c_int(1 << tr_set.rising_pin)
if tr_set.falling_pin == None:
    tr_set.falling_pin = ctypes.c_int(0) 
else:
    tr_set.falling_pin = ctypes.c_int(1 << tr_set.falling_pin)
# set things up
dwf.FDwfDigitalInTriggerSet(hdwf, tr_set.low_pin, tr_set.high_pin, tr_set.rising_pin, tr_set.falling_pin)
 
# trigger reset condition
# create bitmasks
if tr_reset.low_pin == None:
    tr_reset.low_pin = ctypes.c_int(0) 
else:
    tr_reset.low_pin = ctypes.c_int(1 << tr_reset.low_pin)
if tr_reset.high_pin == None:
    tr_reset.high_pin = ctypes.c_int(0) 
else:
    tr_reset.high_pin = ctypes.c_int(1 << tr_reset.high_pin)
if tr_reset.rising_pin == None:
    tr_reset.rising_pin = ctypes.c_int(0) 
else:
    tr_reset.rising_pin = ctypes.c_int(1 << tr_reset.rising_pin)
if tr_reset.falling_pin == None:
    tr_reset.falling_pin = ctypes.c_int(0) 
else:
    tr_reset.falling_pin = ctypes.c_int(1 << tr_reset.falling_pin)
# set things up
dwf.FDwfDigitalInTriggerResetSet(hdwf, tr_reset.low_pin, tr_reset.high_pin, tr_reset.rising_pin, tr_reset.falling_pin)
 
# set auto triggering
dwf.FDwfDigitalInTriggerAutoTimeoutSet(hdwf, ctypes.c_double(trigger_timeout))
 
# set sequence length to activate trigger
dwf.FDwfDigitalInTriggerLengthSet(hdwf, ctypes.c_double(tr_len.length_min), ctypes.c_double(tr_len.length_max), ctypes.c_int(0))
