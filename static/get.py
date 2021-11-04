# user defined variables
pin = 5          # select a DIO line - DIO5 in this case


# load internal buffer with current state of the pins
dwf.FDwfDigitalIOStatus(hdwf)
 
# get the current state of the pins
data = ctypes.c_uint32()  # variable for this current state
dwf.FDwfDigitalIOInputStatus(hdwf, ctypes.byref(data))
 
# convert the state to a 16 character binary string
data = list(bin(data.value)[2:].zfill(16))
 
# check the required bit
state = True if data[15 - pin] != "0" else state = False


# results
# "state" is True if the pin is HIGH, or is False, if the pin is LOW
