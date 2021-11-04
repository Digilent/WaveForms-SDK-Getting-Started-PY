# user defined variables
channel = 1         # the selected scope channel (1-4)


# set up the instrument
dwf.FDwfAnalogInConfigure(hdwf, ctypes.c_bool(False), ctypes.c_bool(False))
 
# read data to an internal buffer
dwf.FDwfAnalogInStatus(hdwf, ctypes.c_bool(False), ctypes.c_int(0))
 
# extract data from that buffer
voltage = ctypes.c_double()   # variable to store the measured voltage
dwf.FDwfAnalogInStatusSample(hdwf, ctypes.c_int(channel - 1), ctypes.byref(voltage))
 
# store the result as float
voltage = voltage.value


# results
# "voltage" contains the measured voltage in Volts
