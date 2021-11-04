# user defined variables
channel = 1                           # select wavegen channel 1 or 2
function_type = constants.funcSine    # possible: funcCustom, funcSine, funcSquare, funcTriangle, funcNoise, funcDC, funcPulse, 
                                                # funcTrapezium, funcSinePower, funcRampUp, funcRampDown
data = [0.9, 3.2, 5, 1.3, -0.5, -3.2] # custom data list - used only if function=constants.funcCustom
frequency = 10e3                      # signal frequency in Hz
amplitude = 2                         # signal amplitude in Volts
offset = 0                            # signal offset in Volts
symmetry = 50                         # signal symmetry in percentage
run_time = 0                          # run time in seconds, 0 means infinite
wait_time = 0                         # time before generation starts in seconds
repeat = 0                            # repeat count, 0 means infinite


# enable channel
channel = ctypes.c_int(channel - 1)
dwf.FDwfAnalogOutNodeEnableSet(hdwf, channel, constants.AnalogOutNodeCarrier, ctypes._bool(True))
 
# set function type
dwf.FDwfAnalogOutNodeFunctionSet(hdwf, channel, constants.AnalogOutNodeCarrier, function_type)
 
# load data if the function type is custom
if function_type == constants.funcCustom:
    data_length = len(data)
    buffer = (ctypes.c_double * data_length)()
    for index in range(0, len(buffer)):
        buffer[index] = ctypes.c_double(data[index])
    dwf.FDwfAnalogOutNodeDataSet(hdwf, channel, constants.AnalogOutNodeCarrier, buffer, ctypes.c_int(data_length))
 
# set frequency
dwf.FDwfAnalogOutNodeFrequencySet(hdwf, channel, constants.AnalogOutNodeCarrier, ctypes.c_double(frequency))
 
# set amplitude or DC voltage
dwf.FDwfAnalogOutNodeAmplitudeSet(hdwf, channel, constants.AnalogOutNodeCarrier, ctypes.c_double(amplitude))
 
# set offset
dwf.FDwfAnalogOutNodeOffsetSet(hdwf, channel, constants.AnalogOutNodeCarrier, ctypes.c_double(offset))
 
# set symmetry
dwf.FDwfAnalogOutNodeSymmetrySet(hdwf, channel, constants.AnalogOutNodeCarrier, ctypes.c_double(symmetry))
 
# set running time limit
dwf.FDwfAnalogOutRunSet(hdwf, channel, ctypes.c_double(run_time))
 
# set wait time before start
dwf.FDwfAnalogOutWaitSet(hdwf, channel, ctypes.c_double(wait_time))
 
# set number of repeating cycles
dwf.FDwfAnalogOutRepeatSet(hdwf, channel, ctypes.c_int(repeat))
 
# start
dwf.FDwfAnalogOutConfigure(hdwf, channel, ctypes.c_bool(True))
