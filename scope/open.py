# user defined variables
offset_voltage = 0          # Volts
amplitude_range = 5         # Volts
buffer_size = 8192          # data points
sampling_frequency = 20e06  # Hz


# enable all channels
dwf.FDwfAnalogInChannelEnableSet(hdwf, ctypes.c_int(0), ctypes.c_bool(True))
 
# set offset voltage (in Volts)
dwf.FDwfAnalogInChannelOffsetSet(hdwf, ctypes.c_int(0), ctypes.c_double(offset_voltage))
 
# set range (maximum signal amplitude in Volts)
dwf.FDwfAnalogInChannelRangeSet(hdwf, ctypes.c_int(0), ctypes.c_double(amplitude_range))
 
# set the buffer size (data point in a recording)
dwf.FDwfAnalogInBufferSizeSet(hdwf, ctypes.c_int(buffer_size))
 
# set the acquisition frequency (in Hz)
dwf.FDwfAnalogInFrequencySet(hdwf, ctypes.c_double(sampling_frequency))
 
# disable averaging (for more info check the documentation)
dwf.FDwfAnalogInChannelFilterSet(hdwf, ctypes.c_int(-1), constants.filterDecimate)
