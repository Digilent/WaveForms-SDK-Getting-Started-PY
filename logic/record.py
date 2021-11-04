# user defined variables
sampling_frequency = 100e06   # sampling frequency of the instrument in Hz
buffer_size = 4096            # data points in a recording
channel = 5                   # the desired DIO line (between 0-15)


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
buffer = (ctypes.c_uint16 * buffer_size)()
dwf.FDwfDigitalInStatusData(hdwf, buffer, ctypes.c_int(2 * buffer_size))
 
# convert buffer to list of lists of integers
buffer = [int(element) for element in buffer]
result = [[] for _ in range(16)]
for data in buffer:
    for index in range(16):
        result[index].append(data & (1 << index))
 
# calculate acquisition time
time = range(0, buffer_size)
time = [moment / sampling_frequency for moment in time]
 
# get channel specific data
buffer = result[channel]


# results
# "buffer" contains a list with the recorded logic values
# "time" contains a list with the time moments for each value in seconds (with the same index as "buffer")
