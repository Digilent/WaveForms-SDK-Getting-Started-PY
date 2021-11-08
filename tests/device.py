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

def open():
    """
        open the first available device
    """
    # this is the device handle - it will be used by all functions to "address" the connected device
    device_handle = ctypes.c_int()

    # connect to the first available device
    dwf.FDwfDeviceOpen(ctypes.c_int(-1), ctypes.byref(device_handle))
    return device_handle

"""-----------------------------------------------------------------------"""

def check_error(device_handle):
    """
        check for connection errors
    """
    # if the device handle is empty after a connection attempt
    if device_handle.value == constants.hdwfNone.value:
        # check for errors
        err_nr = ctypes.c_int()            # variable for error number
        dwf.FDwfGetLastError(ctypes.byref(err_nr))  # get error number
    
        # if there is an error
        if err_nr != constants.dwfercNoErc:
            # display it and quit
            err_msg = ctypes.create_string_buffer(512)        # variable for the error message
            dwf.FDwfGetLastErrorMsg(err_msg)                  # get the error message
            err_msg = err_msg.value.decode("ascii")           # format the message
            print("Error: " + err_msg)                        # display error message
            quit()                                            # exit the program
    return

"""-----------------------------------------------------------------------"""

def close(device_handle):
    """
        close a specific device
    """
    dwf.FDwfDeviceClose(device_handle)
    return
