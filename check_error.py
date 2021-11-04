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
