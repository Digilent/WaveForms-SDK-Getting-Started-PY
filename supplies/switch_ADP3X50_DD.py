# user defined variables
master_state = True         # True = on, False = off
voltage = 2.5               # in Volts


# set supply voltage
voltage = max(1.2, min(3.3, voltage))
dwf.FDwfAnalogIOChannelNodeSet(hdwf, ctypes.c_int(0), ctypes.c_int(0), ctypes.c_double(voltage))
 
# start/stop the supplies - master switch
dwf.FDwfAnalogIOEnableSet(hdwf, ctypes.c_int(master_state))
