from WF_SDK import device, supplies     # import instruments
from WF_SDK.protocol import spi         # import protocol instrument

from time import sleep          # needed for delays

"""-----------------------------------------------------------------------"""

# connect to the device
device_data = device.open()

# check for connection errors
device.check_error(device_data)

"""-----------------------------------"""

# define chip select lines
CLS_cs = 0
ALS_cs = 1

# start the power supplies
supplies_state = supplies.state()
supplies_state.master_state = True
supplies_state.state = True
supplies_state.voltage = 3.3
supplies.switch(device_data, supplies_state)

# initialize the spi interface on DIO0, DIO1, DIO2, DIO3 and DIO4
spi.open(device_data, CLS_cs, sck=2, miso=3, mosi=4)
spi.open(device_data, ALS_cs, sck=2, miso=3, mosi=4)

try:
    # repeat
    while True:
        # clear the screen and home cursor
        spi.write(device_data, "\x1b[j", CLS_cs)

        # display a message
        spi.write(device_data, "Lum: ", CLS_cs)

        # read the temperature
        message = spi.read(device_data, 2, ALS_cs)
        value = ((int(message[0]) << 3) | (int(message[1]) >> 4)) / 1.27

        # display the temperature
        spi.write(device_data, str(round(value, 2)), CLS_cs)

        # display a message
        spi.write(device_data, "%", CLS_cs)

        # delay 1s
        sleep(1)

except KeyboardInterrupt:
    # exit on Ctrl+C
    pass

# reset the interface
spi.close(device_data)

# stop and reset the power supplies
supplies_state.master_state = False
supplies.switch(device_data, supplies_state)
supplies.close(device_data)

"""-----------------------------------"""

# close the connection
device.close(device_data)
