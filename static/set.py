# user defined variables
pin = 2          # select a DIO line - DIO2 in this case
state = True     # set True for HIGH, False for LOW


# load current state of the output state buffer
mask = ctypes.c_uint16()
dwf.FDwfDigitalIOOutputGet(hdwf, ctypes.byref(mask))
 
# convert mask to list
mask = list(bin(mask.value)[2:].zfill(16))
 
# set bit in mask
mask[15 - pin] = "1" if state else mask[15 - pin] = "0"
 
# convert mask to number
mask = "".join(element for element in mask)
mask = int(mask, 2)
 
# set the pin state
dwf.FDwfDigitalIOOutputSet(hdwf, ctypes.c_int(mask))
