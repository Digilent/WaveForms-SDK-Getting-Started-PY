from WF_SDK import device, error    # import instruments
from time import sleep              # for delays

"""-----------------------------------------------------------------------"""

try:
    # connect to the device
    device_data = device.open()

    """-----------------------------------"""

    # use instruments here
    try:
        while True:
            print("board temperature: " + str(device.temperature(device_data)))             # get board temperature
            sleep(0.5)  # delay
    except KeyboardInterrupt:
        pass    # exit on Ctrl+C

    """-----------------------------------"""

    # close the connection
    device.close(device_data)

except error as e:
    print(e)
    # close the connection
    device.close(device.data)
