""" INITIALIZE THE WAVEFORMS SDK """

import ctypes                     # import the C compatible data types
import dwfconstants as constants  # import every constant
from sys import platform          # this is needed to check the OS type

import matplotlib.pyplot as plt   # needed for plotting

# load the dynamic library (the path is OS specific)
if platform.startswith("win"):
    # on Windows
    dwf = ctypes.cdll.dwf
elif platform.startswith("darwin"):
    # on macOS
    dwf = ctypes.cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    # on Linux
    dwf = ctypes.cdll.LoadLibrary("libdwf.so")

"""-----------------------------------------------------------------------"""

""" OPEN THE FIRST DEVICE """

# this is the device handle - it will be used by all functions to "address" the connected device
hdwf = ctypes.c_int()

# connect to the first available device
dwf.FDwfDeviceOpen(ctypes.c_int(-1), ctypes.byref(hdwf))

"""-----------------------------------------------------------------------"""

""" CHECK FOR CONNECTION ERRORS """

# if the device handle is empty after a connection attempt
if hdwf.value == constants.hdwfNone.value:
    # check for errors
    err_nr = ctypes.c_int()            # variable for error number
    dwf.FDwfGetLastError(ctypes.byref(err_nr))  # get error number
 
    # if there is an error
    if err_nr != constants.dwfercNoErc:
        # display it and quit
        err_msg = ctypes.create_string_buffer(512)        # variable for the error message
        dwf.FDwfGetLastErrorMsg(err_msg)                  # get the error message
        print("Error: " + err_msg.value.decode("ascii"))  # display error message
        quit()                                            # exit the program

"""-----------------------------------------------------------------------"""

""" INITIALIZE THE LOGIC ANALYZER """

# user defined variables
logic_sampling_frequency = 100e06   # sampling frequency of the instrument in Hz
logic_buffer_size = 4096            # data points in a recording


# get internal clock frequency
internal_frequency = ctypes.c_double()
dwf.FDwfDigitalInInternalClockInfo(hdwf, ctypes.byref(internal_frequency))
 
# set clock frequency divider (needed for lower frequency input signals)
dwf.FDwfDigitalInDividerSet(hdwf, ctypes.c_int(int(internal_frequency.value / logic_sampling_frequency)))
 
# set 16-bit sample format
dwf.FDwfDigitalInSampleFormatSet(hdwf, ctypes.c_int(16))
 
# set buffer size
dwf.FDwfDigitalInBufferSizeSet(hdwf, ctypes.c_int(logic_buffer_size))

"""-----------------------------------------------------------------------"""

""" SET UP TRIGGERING """

# user defined variables
trigger_enable = True         # enable/disable the trigger
trigger_position = 0          # how many bits should be read before the trigger event
trigger_timeout = 2           # in seconds
trigger_pin = 0               # DIO line used as trigger
trigger_edge_rising = False   # set True for rising edge, False for falling edge
trigger_length_min = 0        # trigger only on sequences longer than 0s (between 0s-20s)
trigger_length_max = 20       # trigger only on sequences shorter than 20s (between 0s-20s)
trigger_count = 1             # trigger event counter


# set trigger source to digital I/O lines, or turn it off
if trigger_enable:
    dwf.FDwfDigitalInTriggerSourceSet(hdwf, constants.trigsrcDetectorDigitalIn)
else:
    dwf.FDwfDigitalInTriggerSourceSet(hdwf, constants.trigsrcNone)
 
# set starting position and prefill
trigger_position = min(logic_buffer_size, max(0, trigger_position))
dwf.FDwfDigitalInTriggerPositionSet(hdwf, ctypes.c_int(logic_buffer_size - trigger_position))
dwf.FDwfDigitalInTriggerPrefillSet(hdwf, ctypes.c_int(trigger_position))

# set trigger condition
trigger_pin = ctypes.c_int(1 << trigger_pin)
if trigger_edge_rising:
    dwf.FDwfDigitalInTriggerSet(hdwf, trigger_pin, ctypes.c_int(0), ctypes.c_int(0), ctypes.c_int(0))
    dwf.FDwfDigitalInTriggerResetSet(hdwf, ctypes.c_int(0), ctypes.c_int(0), ctypes.c_int(0), trigger_pin)
else:
    dwf.FDwfDigitalInTriggerSet(hdwf, ctypes.c_int(0), trigger_pin, ctypes.c_int(0), ctypes.c_int(0))
    dwf.FDwfDigitalInTriggerResetSet(hdwf, ctypes.c_int(0), ctypes.c_int(0), trigger_pin, ctypes.c_int(0))
 
# set auto triggering
dwf.FDwfDigitalInTriggerAutoTimeoutSet(hdwf, ctypes.c_double(trigger_timeout))
 
# set sequence length to activate trigger
dwf.FDwfDigitalInTriggerLengthSet(hdwf, ctypes.c_double(trigger_length_min), ctypes.c_double(trigger_length_max), ctypes.c_int(0))

# set event counter
dwf.FDwfDigitalInTriggerCountSet(hdwf, ctypes.c_int(trigger_count), ctypes.c_int(0))

"""-----------------------------------------------------------------------"""

""" GENERATE A PATTERN """

# user defined variables
pattern_frequency = 100e03                                    # signal frequency in Hz
pattern_channel = 0                                           # select a DIO line - DIO3 in this case
pattern_function = constants.DwfDigitalOutTypePulse           # possible: DwfDigitalOutTypePulse, DwfDigitalOutTypeCustom, DwfDigitalOutTypeRandom
pattern_wait_time = 0                                         # in seconds
pattern_repeat = 0                                            # repeat count, 0 means infinite
pattern_trigger_enabled = False                               # enable/disable trigger in repeat cycle
pattern_trigger_source = constants.trigsrcNone                # possible: trigsrcDetectorDigitalIn, trigsrcNone, trigsrcDetectorAnalogIn,
                                                                        # trigsrcExternal1, trigsrcExternal2, trigsrcExternal3, trigsrcExternal4
pattern_trigger_edge = constants.DwfTriggerSlopeRise          # possible: DwfTriggerSlopeRise, DwfTriggerSlopeFall, DwfTriggerSlopeEither
pattern_duty_cycle = 30                                       # duty cycle of the signal in percentage, used only if function = constants.DwfDigitalOutTypePulse
pattern_data = [1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0]           # custom data list, used only if function = constants.DwfDigitalOutTypeCustom


# get internal clock frequency
internal_frequency = ctypes.c_double()
dwf.FDwfDigitalOutInternalClockInfo(hdwf, ctypes.byref(internal_frequency))
 
# get counter value range
counter_limit = ctypes.c_uint()
dwf.FDwfDigitalOutCounterInfo(hdwf, ctypes.c_int(0), ctypes.c_int(0), ctypes.byref(counter_limit))
 
# calculate the divider for the given signal frequency
divider = int(-(-(internal_frequency.value / pattern_frequency) // counter_limit.value))
 
# enable the respective channel
dwf.FDwfDigitalOutEnableSet(hdwf, ctypes.c_int(pattern_channel), ctypes.c_int(1))
 
# set output type
dwf.FDwfDigitalOutTypeSet(hdwf, ctypes.c_int(pattern_channel), pattern_function)
 
# set frequency
dwf.FDwfDigitalOutDividerSet(hdwf, ctypes.c_int(pattern_channel), ctypes.c_int(divider))
 
# set wait time
dwf.FDwfDigitalOutWaitSet(hdwf, ctypes.c_double(pattern_wait_time))
 
# set repeat count
dwf.FDwfDigitalOutRepeatSet(hdwf, ctypes.c_int(pattern_repeat))
 
# enable triggering
dwf.FDwfDigitalOutRepeatTriggerSet(hdwf, ctypes.c_int(pattern_trigger_enabled))
 
# set trigger source
dwf.FDwfDigitalOutTriggerSourceSet(hdwf, pattern_trigger_source)
 
# set trigger slope
dwf.FDwfDigitalOutTriggerSlopeSet(hdwf, pattern_trigger_edge)
 
# set PWM signal duty cycle
if pattern_function == constants.DwfDigitalOutTypePulse:
    # set duty cycle
    # calculate counter steps to get the required frequency
    steps = int(round(internal_frequency.value / pattern_frequency / divider))
    # calculate steps for low and high parts of the period
    high_steps = int(steps * pattern_duty_cycle / 100)
    low_steps = int(steps - high_steps)
    dwf.FDwfDigitalOutCounterSet(hdwf, ctypes.c_int(pattern_channel), ctypes.c_int(low_steps), ctypes.c_int(high_steps))
 
# load custom signal data
elif pattern_function == constants.DwfDigitalOutTypeCustom:
    # format data
    buffer = (ctypes.c_ubyte * ((len(pattern_data) + 7) >> 3))(0)
    for index in range(len(pattern_data)):
        if pattern_data[index] != 0:
            buffer[index >> 3] |= 1 << (index & 7)
 
    # load data
    dwf.FDwfDigitalOutDataSet(hdwf, ctypes.c_int(pattern_channel), ctypes.byref(buffer), ctypes.c_int(len(pattern_data)))
 
# start generating the signal
dwf.FDwfDigitalOutConfigure(hdwf, ctypes.c_int(True))


"""-----------------------------------------------------------------------"""

""" RECORD A SIGNAL """

# user defined variables
logic_channel = 0             # the desired DIO line (between 0-15)


# set up the instrument
dwf.FDwfDigitalInConfigure(hdwf, ctypes.c_bool(False), ctypes.c_bool(True))
 
# read data to an internal buffer
while True:
    status = ctypes.c_byte()    # variable to store buffer status
    dwf.FDwfDigitalInStatus(hdwf, ctypes.c_bool(True), ctypes.byref(status))
 
    if status.value == constants.stsDone.value:
        # exit loop when finished
        break
 
# get samples
buffer = (ctypes.c_uint16 * logic_buffer_size)()
dwf.FDwfDigitalInStatusData(hdwf, buffer, ctypes.c_int(2 * logic_buffer_size))
 
# convert buffer to list of lists of integers
buffer = [int(element) for element in buffer]
result = [[] for _ in range(16)]
for data in buffer:
    for index in range(16):
        result[index].append(data & (1 << index))
 
# calculate acquisition time
time = range(0, logic_buffer_size)
time = [moment / logic_sampling_frequency for moment in time]
 
# get channel specific data
buffer = result[logic_channel]


# results
# "buffer" contains a list with the recorded logic values
# "time" contains a list with the time moments for each value in seconds (with the same index as "buffer")

"""-----------------------------------------------------------------------"""

""" DISPLAY THE RECORDED SIGNAL """

time = [moment * 1e06 for moment in time]   # convert time to μs

# plot
plt.plot(time, buffer)
plt.xlabel("time [μs]")
plt.ylabel("logic value")
plt.yticks([0, 1])
plt.show()

"""-----------------------------------------------------------------------"""

""" RESET THE LOGIC ANALYZER """

# reset the instrument
dwf.FDwfDigitalInReset(hdwf)

"""-----------------------------------------------------------------------"""

""" RESET THE PATTERN GENERATOR """

# reset the instrument
dwf.FDwfDigitalOutReset(hdwf)

"""-----------------------------------------------------------------------"""

""" CLOSE THE DEVICE """

# close the opened connection
dwf.FDwfDeviceClose(hdwf)
