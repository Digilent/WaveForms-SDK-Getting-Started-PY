from WF_SDK import device, static, supplies, error  # import instruments

from time import sleep                              # needed for delays

"""-----------------------------------------------------------------------"""

try:
    # connect to the device
    device_data = device.open()

    """-----------------------------------"""

    # start the positive supply
    supplies_data = supplies.data()
    supplies_data.master_state = True
    supplies_data.state = True
    supplies_data.voltage = 3.3
    supplies.switch(device_data, supplies_data)

    # set maximum current
    if device_data.name == "Digital Discovery" or device_data.name == "Analog Discovery Pro 3X50":
        static.set_current(device_data, 16)

    # set all pins as output
    for index in range(16):
        static.set_mode(device_data, index, True)

    try:
        while True:
            # repeat
            mask = 1
            while mask < 0x10000:
                # go through possible states
                for index in range(16):
                    # set the state of every DIO channel
                    static.set_state(device_data, index, not(mask & pow(2, index)))
                sleep(0.1)  # delay
                mask <<= 1  # switch mask

            while mask > 1:
                # go through possible states backward
                mask >>= 1  # switch mask
                for index in range(16):
                    # set the state of every DIO channel
                    static.set_state(device_data, index, not(mask & pow(2, index)))
                sleep(0.1)  # delay

    except KeyboardInterrupt:
        # stop if Ctrl+C is pressed
        pass

    finally:
        # stop the static I/O
        static.close(device_data)

        # stop and reset the power supplies
        supplies_data.master_state = False
        supplies.switch(device_data, supplies_data)
        supplies.close(device_data)

        """-----------------------------------"""

        # close the connection
        device.close(device_data)

except error as e:
    print(e)
    # close the connection
    device.close(device.data)
