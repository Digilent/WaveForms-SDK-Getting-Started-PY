from WF_SDK import device, supplies     # import instruments
from WF_SDK.protocol import i2c         # import protocol instrument

from time import sleep          # needed for delays

"""-----------------------------------------------------------------------"""

# connect to the device
device_handle, device_name = device.open()

# check for connection errors
device.check_error(device_handle)

"""-----------------------------------"""

# define i2c addresses
CLS_address = 0x48
TMP2_address = 0x4B

# start the power supplies
class supplies_state:
    device_name = device_name
    master_state = True
    state = True
    voltage = 3.3
supplies.switch(device_handle, supplies_state)
sleep(0.1)    # delay

# initialize the i2c interface on DIO0 and DIO1
i2c.open(device_handle, sda=0, scl=1)

# initialize the PMOD TMP2 (set output size to 16-bit)
i2c.write(device_handle, [0x03, 0x80], TMP2_address)

# save custom character
i2c.write(device_handle, "\x1b[7;5;7;0;0;0;0;0;0d", CLS_address)   # define character
i2c.write(device_handle, "\x1b[3p", CLS_address) # load character table

try:
    # repeat
    while True:
        # clear the screen and home cursor
        i2c.write(device_handle, [0x1B, 0x5B, 0x6A], CLS_address)

        # display a message
        i2c.write(device_handle, "Temp: ", CLS_address)

        # read the temperature
        message, error = i2c.read(device_handle, 2, TMP2_address)   # read 2 bytes
        value = (int(message[0]) << 8) | int(message[1])    # create integer from received bytes
        if ((value >> 15) & 1) == 0:
            value /= 128    # decode positive numbers
        else:
            value = (value - 65535) / 128   # decode negative numbers

        # display the temperature
        i2c.write(device_handle, str(round(value, 2)), CLS_address)

        # display a message
        i2c.write(device_handle, 0, CLS_address)
        i2c.write(device_handle, "C", CLS_address)

        # delay 1s
        sleep(1)

except KeyboardInterrupt:
    # exit on Ctrl+C
    pass

# reset the interface
i2c.close(device_handle)

# stop and reset the power supplies
supplies_state.master_state = False
supplies.switch(device_handle, supplies_state)
supplies.close(device_handle)

"""-----------------------------------"""

# close the connection
device.close(device_handle)
