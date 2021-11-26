from WF_SDK import device, static, supplies       # import instruments

from time import sleep                            # needed for delays

"""-----------------------------------------------------------------------"""

# connect to the device
device_handle, device_name = device.open()

# check for connection errors
device.check_error(device_handle)

"""-----------------------------------"""

# start the positive supply
class supplies_state:
    device_name = device_name
    master_state = True
    state = True
    voltage = 3.3
supplies.switch(device_handle, supplies_state)

# set maximum current
if device_name == "Digital Discovery" or device_name == "Analog Discovery Pro 3X50":
    static.set_current(device_handle, 16)

# set all pins as output
for index in range(16):
    static.set_mode(device_handle, index, True)

try:
    while True:
        # repeat
        mask = 1
        while mask < 0x10000:
            # go through possible states
            for index in range(16):
                # set the state of every DIO channel
                static.set_state(device_handle, index, not(mask & pow(2, index)))
            sleep(0.1)  # delay
            mask <<= 1  # switch mask

        while mask > 1:
            # go through possible states backward
            mask >>= 1  # switch mask
            for index in range(16):
                # set the state of every DIO channel
                static.set_state(device_handle, index, not(mask & pow(2, index)))
            sleep(0.1)  # delay

except KeyboardInterrupt:
    # stop if Ctrl+C is pressed
    pass

finally:
    # stop the static I/O
    static.close(device_handle)

    # stop and reset the power supplies
    supplies_state.master_state = False
    supplies.switch(device_handle, supplies_state)
    supplies.close(device_handle)

    """-----------------------------------"""

    # close the connection
    device.close(device_handle)
