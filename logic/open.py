# user defined variables
sampling_frequency = 100e06   # sampling frequency of the instrument in Hz
buffer_size = 4096            # data points in a recording


# get internal clock frequency
internal_frequency = ctypes.c_double()
dwf.FDwfDigitalInInternalClockInfo(hdwf, ctypes.byref(internal_frequency))
 
# set clock frequency divider (needed for lower frequency input signals)
dwf.FDwfDigitalInDividerSet(hdwf, ctypes.c_int(int(internal_frequency.value / sampling_frequency)))
 
# set 16-bit sample format
dwf.FDwfDigitalInSampleFormatSet(hdwf, ctypes.c_int(16))
 
# set buffer size
dwf.FDwfDigitalInBufferSizeSet(hdwf, ctypes.c_int(buffer_size))
