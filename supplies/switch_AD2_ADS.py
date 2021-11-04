# user defined variables
positive_state = True       # True = on, False = off
negative_state = False      # True = on, False = off
master_state = True         # True = on, False = off
positive_voltage = 4.32     # in Volts
negative_voltage = -1.27    # in Volts


# set positive voltage
positive_voltage = max(0, min(5, positive_voltage))
dwf.FDwfAnalogIOChannelNodeSet(hdwf, ctypes.c_int(0), ctypes.c_int(1), ctypes.c_double(positive_voltage))
 
# set negative voltage
negative_voltage = max(-5, min(0, negative_voltage))
dwf.FDwfAnalogIOChannelNodeSet(hdwf, ctypes.c_int(1), ctypes.c_int(1), ctypes.c_double(negative_voltage))

# enable/disable the positive supply
dwf.FDwfAnalogIOChannelNodeSet(hdwf, ctypes.c_int(0), ctypes.c_int(0), ctypes.c_int(positive_state))
 
# enable the negative supply
dwf.FDwfAnalogIOChannelNodeSet(hdwf, ctypes.c_int(1), ctypes.c_int(0), ctypes.c_int(negative_state))
 
# start/stop the supplies - master switch
dwf.FDwfAnalogIOEnableSet(hdwf, ctypes.c_int(master_state))
