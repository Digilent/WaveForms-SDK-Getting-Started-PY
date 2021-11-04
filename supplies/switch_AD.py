# user defined variables
positive_state = True       # True = on, False = off
negative_state = False      # True = on, False = off
master_state = True         # True = on, False = off


# enable/disable the positive supply
dwf.FDwfAnalogIOChannelNodeSet(hdwf, ctypes.c_int(0), ctypes.c_int(0), ctypes.c_int(positive_state))
 
# enable the negative supply
dwf.FDwfAnalogIOChannelNodeSet(hdwf, ctypes.c_int(1), ctypes.c_int(0), ctypes.c_int(negative_state))
 
# start/stop the supplies - master switch
dwf.FDwfAnalogIOEnableSet(hdwf, ctypes.c_int(master_state))
