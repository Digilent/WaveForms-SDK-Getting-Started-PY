# user defined variables
pin = 2          # select a DIO line - DIO2 in this case
output = True    # set True for output, False for input


# load current state of the output enable buffer
mask = ctypes.c_uint16()
dwf.FDwfDigitalIOOutputEnableGet(hdwf, ctypes.byref(mask))
 
# convert mask to list
mask = list(bin(mask.value)[2:].zfill(16))
 
# set bit in mask
mask[15 - pin] = "1" if output else mask[15 - pin] = "0"
 
# convert mask to number
mask = "".join(element for element in mask)
mask = int(mask, 2)
 
# set the pin to output
dwf.FDwfDigitalIOOutputEnableSet(hdwf, ctypes.c_int(mask))
