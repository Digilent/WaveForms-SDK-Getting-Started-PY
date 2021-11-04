# this is the device handle - it will be used by all functions to "address" the connected device
hdwf = ctypes.c_int()

# connect to the first available device
dwf.FDwfDeviceOpen(ctypes.c_int(-1), ctypes.byref(hdwf))
