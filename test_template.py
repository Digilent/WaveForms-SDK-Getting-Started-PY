from WF_SDK import device       # import instruments

"""-----------------------------------------------------------------------"""

# connect to the device
device_data = device.open()

# check for connection errors
device.check_error(device_data)

"""-----------------------------------"""

# use instruments here


"""-----------------------------------"""

# close the connection
device.close(device_data)
