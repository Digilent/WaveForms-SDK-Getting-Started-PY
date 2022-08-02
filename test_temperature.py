from WF_SDK import device       # import instruments
from time import sleep          # for delays

"""-----------------------------------------------------------------------"""

# connect to the device
device_data = device.open()

# check for connection errors
device.check_error(device_data)

"""-----------------------------------"""

# use instruments here
try:
    while True:
        temp = device.temperature(device_data)  # get board temperature
        print("board temperature: " + str(round(temp, 2)) + "°C")   # display temperature
        sleep(0.5)  # delay
except KeyboardInterrupt:
    pass    # exit on Ctrl+C

"""-----------------------------------"""

# close the connection
device.close(device_data)
