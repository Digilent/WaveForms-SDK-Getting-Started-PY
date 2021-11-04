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

""" INITIALIZE THE SCOPE """

# user defined variables
scope_offset_voltage = 0          # Volts
scope_amplitude_range = 5         # Volts
scope_buffer_size = 8192          # data points
scope_sampling_frequency = 20e06  # Hz


# enable all channels
dwf.FDwfAnalogInChannelEnableSet(hdwf, ctypes.c_int(0), ctypes.c_bool(True))
 
# set offset voltage (in Volts)
dwf.FDwfAnalogInChannelOffsetSet(hdwf, ctypes.c_int(0), ctypes.c_double(scope_offset_voltage))
 
# set range (maximum signal amplitude in Volts)
dwf.FDwfAnalogInChannelRangeSet(hdwf, ctypes.c_int(0), ctypes.c_double(scope_amplitude_range))
 
# set the buffer size (data point in a recording)
dwf.FDwfAnalogInBufferSizeSet(hdwf, ctypes.c_int(scope_buffer_size))
 
# set the acquisition frequency (in Hz)
dwf.FDwfAnalogInFrequencySet(hdwf, ctypes.c_double(scope_sampling_frequency))
 
# disable averaging (for more info check the documentation)
dwf.FDwfAnalogInChannelFilterSet(hdwf, ctypes.c_int(-1), constants.filterDecimate)

"""-----------------------------------------------------------------------"""

""" SET UP TRIGGERING """

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

"""-----------------------------------------------------------------------"""

""" GENERATE A SIGNAL """

# user defined variables
wavegen_channel = 1                           # select wavegen channel 1 or 2
wavegen_function_type = constants.funcSine    # possible: funcCustom, funcSine, funcSquare, funcTriangle, funcNoise, funcDC, funcPulse, 
                                                        # funcTrapezium, funcSinePower, funcRampUp, funcRampDown
wavegen_data = [0.9, 3.2, 5, 1.3, -0.5, -3.2] # custom data list - used only if function=constants.funcCustom
wavegen_frequency = 10e3                      # signal frequency in Hz
wavegen_amplitude = 2                         # signal amplitude in Volts
wavegen_offset = 0                            # signal offset in Volts
wavegen_symmetry = 50                         # signal symmetry in percentage
wavegen_run_time = 0                          # run time in seconds, 0 means infinite
wavegen_wait_time = 0                         # time before generation starts in seconds
wavegen_repeat = 0                            # repeat count, 0 means infinite


# enable channel
channel = ctypes.c_int(wavegen_channel - 1)
dwf.FDwfAnalogOutNodeEnableSet(hdwf, channel, constants.AnalogOutNodeCarrier, ctypes.c_bool(True))
 
# set function type
dwf.FDwfAnalogOutNodeFunctionSet(hdwf, channel, constants.AnalogOutNodeCarrier, wavegen_function_type)
 
# load data if the function type is custom
if wavegen_function_type == constants.funcCustom:
    data_length = len(wavegen_data)
    buffer = (ctypes.c_double * data_length)()
    for index in range(0, len(buffer)):
        buffer[index] = ctypes.c_double(wavegen_data[index])
    dwf.FDwfAnalogOutNodeDataSet(hdwf, channel, constants.AnalogOutNodeCarrier, buffer, ctypes.c_int(data_length))
 
# set frequency
dwf.FDwfAnalogOutNodeFrequencySet(hdwf, channel, constants.AnalogOutNodeCarrier, ctypes.c_double(wavegen_frequency))
 
# set amplitude or DC voltage
dwf.FDwfAnalogOutNodeAmplitudeSet(hdwf, channel, constants.AnalogOutNodeCarrier, ctypes.c_double(wavegen_amplitude))
 
# set offset
dwf.FDwfAnalogOutNodeOffsetSet(hdwf, channel, constants.AnalogOutNodeCarrier, ctypes.c_double(wavegen_offset))
 
# set symmetry
dwf.FDwfAnalogOutNodeSymmetrySet(hdwf, channel, constants.AnalogOutNodeCarrier, ctypes.c_double(wavegen_symmetry))
 
# set running time limit
dwf.FDwfAnalogOutRunSet(hdwf, channel, ctypes.c_double(wavegen_run_time))
 
# set wait time before start
dwf.FDwfAnalogOutWaitSet(hdwf, channel, ctypes.c_double(wavegen_wait_time))
 
# set number of repeating cycles
dwf.FDwfAnalogOutRepeatSet(hdwf, channel, ctypes.c_int(wavegen_repeat))
 
# start
dwf.FDwfAnalogOutConfigure(hdwf, channel, ctypes.c_bool(True))

"""-----------------------------------------------------------------------"""

""" RECORD THE SIGNAL """

# user defined variables
scope_channel = 1                 # the selected scope channel (1-4)


# set up the instrument
dwf.FDwfAnalogInConfigure(hdwf, ctypes.c_bool(False), ctypes.c_bool(True))
 
# read data to an internal buffer
while True:
    status = ctypes.c_byte()    # variable to store buffer status
    dwf.FDwfAnalogInStatus(hdwf, ctypes.c_bool(True), ctypes.byref(status))
 
    # check internal buffer status
    if status.value == constants.DwfStateDone.value:
            # exit loop when ready
            break
 
# copy buffer
buffer = (ctypes.c_double * scope_buffer_size)()   # create an empty buffer
dwf.FDwfAnalogInStatusData(hdwf, ctypes.c_int(scope_channel - 1), buffer, ctypes.c_int(scope_buffer_size))
 
# calculate aquisition time
time = range(0, scope_buffer_size)
time = [moment / scope_sampling_frequency for moment in time]
 
# convert into list
buffer = [float(element) for element in buffer]


# results
# "buffer" contains a list with the recorded voltages
# "time" contains a list with the time moments for each voltage in seconds (with the same index as "buffer")

"""-----------------------------------------------------------------------"""

""" DISPLAY THE RECORDED SIGNAL """

time = [moment * 1e03 for moment in time]   # convert time to ms

# plot
plt.plot(time, buffer)
plt.xlabel("time [ms]")
plt.ylabel("voltage [V]")
plt.show()

"""-----------------------------------------------------------------------"""

""" RESET THE SCOPE """

# reset the scope
dwf.FDwfAnalogInReset(hdwf)

"""-----------------------------------------------------------------------"""

""" RESET THE WAVEGEN """

# reset the wavegen
dwf.FDwfAnalogOutReset(hdwf)

"""-----------------------------------------------------------------------"""

""" CLOSE THE DEVICE """

# close the opened connection
dwf.FDwfDeviceClose(hdwf)
