# user defined variables
channel = 1                 # the selected scope channel (1-4)
buffer_size = 8192          # data points
sampling_frequency = 20e06  # Hz


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
buffer = (ctypes.c_double * buffer_size)()   # create an empty buffer
dwf.FDwfAnalogInStatusData(hdwf, ctypes.c_int(channel - 1), buffer, ctypes.c_int(buffer_size))
 
# calculate aquisition time
time = range(0, buffer_size)
time = [moment / sampling_frequency for moment in time]
 
# convert into list
buffer = [float(element) for element in buffer]


# results
# "buffer" contains a list with the recorded voltages
# "time" contains a list with the time moments for each voltage in seconds (with the same index as "buffer")
