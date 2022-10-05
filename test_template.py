from WF_SDK import device, error       # import instruments

"""-----------------------------------------------------------------------"""

try:
    # connect to the device
    device_data = device.open()

    """-----------------------------------"""

    # use instruments here


    """-----------------------------------"""

    # close the connection
    device.close(device_data)

except error as e:
    print(e)
    # close the connection
    device.close(device.data)
