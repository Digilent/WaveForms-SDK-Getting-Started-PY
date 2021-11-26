from WF_SDK import device, supplies, static     # import instruments
from WF_SDK.protocol import uart                # import protocol instrument

from time import sleep          # needed for delays

"""-----------------------------------------------------------------------"""

# connect to the device
device_handle, device_name = device.open()

# check for connection errors
device.check_error(device_handle)

"""-----------------------------------"""

# define MAXSonar reset line
reset = 2

# define timeout iteration count
timeout = 1000

# start the power supplies
class supplies_state:
    device_name = device_name
    master_state = True
    state = True
    voltage = 3.3
supplies.switch(device_handle, supplies_state)
sleep(0.1)    # delay

# initialize the reset line
static.set_mode(device_handle, reset, output=True)
static.set_state(device_handle, reset, False)

# initialize the uart interface on DIO0 and DIO1
uart.open(device_handle, tx=0, rx=1, baud_rate=9600)

try:
    # repeat
    while True:
        # clear the screen and home cursor
        uart.write(device_handle, "\x1b[j")

        # display a message
        uart.write(device_handle, "Dist: ")

        # read raw data
        static.set_state(device_handle, reset, True)    # enable the device
        message = ""
        for _ in range(timeout):
            # wait for data
            message, error = uart.read(device_handle)
            if message != "":
                # exit when data is received
                break
        static.set_state(device_handle, reset, False)    # disable the device

        # convert raw data into distance
        try:
            if message[0] == 234:
                message.pop(0)    # remove first byte
                value = 0
                for element in message:
                    if element > 47 and element < 58:
                        # concatenate valid bytes
                        value = value * 10 + (element - 48)
                value *= 2.54   # convert to cm
        except:
            # error in message
            value = -1

        # display the distance
        uart.write(device_handle, str(round(value, 2)))

        # display a message
        uart.write(device_handle, "cm")

        # delay 1s
        sleep(1)

except KeyboardInterrupt:
    # exit on Ctrl+C
    pass

# reset the interface
uart.close(device_handle)

# reset the static I/O
static.set_mode(device_handle, reset, output=False)
static.set_state(device_handle, reset, True)
static.close(device_handle)

# stop and reset the power supplies
supplies_state.master_state = False
supplies.switch(device_handle, supplies_state)
supplies.close(device_handle)

"""-----------------------------------"""

# close the connection
device.close(device_handle)
