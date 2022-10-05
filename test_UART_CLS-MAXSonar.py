from WF_SDK import device, supplies, static, error, warning     # import instruments
from WF_SDK.protocol import uart                                # import protocol instrument

from time import sleep          # needed for delays

"""-----------------------------------------------------------------------"""

try:
    # connect to the device
    device_data = device.open()

    """-----------------------------------"""

    # define MAXSonar reset line
    reset = 2

    # define timeout iteration count
    timeout = 1000

    # start the power supplies
    supplies_data = supplies.data()
    supplies_data.master_state = True
    supplies_data.state = True
    supplies_data.voltage = 3.3
    supplies.switch(device_data, supplies_data)
    sleep(0.1)    # delay

    # initialize the reset line
    static.set_mode(device_data, reset, output=True)
    static.set_state(device_data, reset, False)

    # initialize the uart interface on DIO0 and DIO1
    uart.open(device_data, tx=0, rx=1, baud_rate=9600)

    try:
        # repeat
        while True:
            try:
                # clear the screen and home cursor
                uart.write(device_data, "\x1b[j")

                # display a message
                uart.write(device_data, "Dist: ")

                # read raw data
                static.set_state(device_data, reset, True)    # enable the device
                message = ""
                for _ in range(timeout):
                    # wait for data
                    message, error = uart.read(device_data)
                    if message != "":
                        # exit when data is received
                        break
                static.set_state(device_data, reset, False)    # disable the device

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
                uart.write(device_data, str(round(value, 2)))

                # display a message
                uart.write(device_data, "cm")

                # delay 1s
                sleep(1)
            
            except warning as w:
                print(w)

    except KeyboardInterrupt:
        # exit on Ctrl+C
        pass

    # reset the interface
    uart.close(device_data)

    # reset the static I/O
    static.set_mode(device_data, reset, output=False)
    static.set_state(device_data, reset, True)
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
