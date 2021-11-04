""" INITIALIZE THE WAVEFORMS SDK """

import ctypes                     # import the C compatible data types
import dwfconstants as constants  # import every constant
from sys import platform          # this is needed to check the OS type

# load the dynamic library (the path is OS specific)
if platform.startswith("win"):
    # on Windows
    dwf = ctypes.cdll.dwf
elif platform.startswith("darwin"):
    # on macOS
    dwf = ctypes.cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    # on Linux
    dwf = ctypes.cdll.LoadLibrary("libdwf.so")

"""-----------------------------------------------------------------------"""

""" OPEN THE FIRST DEVICE """

# this is the device handle - it will be used by all functions to "address" the connected device
hdwf = ctypes.c_int()

# connect to the first available device
dwf.FDwfDeviceOpen(ctypes.c_int(-1), ctypes.byref(hdwf))

"""-----------------------------------------------------------------------"""

""" CHECK FOR CONNECTION ERRORS """

# if the device handle is empty after a connection attempt
if hdwf.value == constants.hdwfNone.value:
    # check for errors
    err_nr = ctypes.c_int()            # variable for error number
    dwf.FDwfGetLastError(ctypes.byref(err_nr))  # get error number
 
    # if there is an error
    if err_nr != constants.dwfercNoErc:
        # display it and quit
        err_msg = ctypes.create_string_buffer(512)        # variable for the error message
        dwf.FDwfGetLastErrorMsg(err_msg)                  # get the error message
        print("Error: " + err_msg.value.decode("ascii"))  # display error message
        quit()                                            # exit the program

"""-----------------------------------------------------------------------"""

# use instruments here

"""-----------------------------------------------------------------------"""

""" CLOSE THE DEVICE """

# close the opened connection
dwf.FDwfDeviceClose(hdwf)
