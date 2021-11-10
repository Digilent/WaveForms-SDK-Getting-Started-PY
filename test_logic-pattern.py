from WF_SDK import device, logic, pattern   # import instruments

import matplotlib.pyplot as plt   # needed for plotting

"""-----------------------------------------------------------------------"""

# connect to the device
device_handle, device_name = device.open()

# check for connection errors
device.check_error(device_handle)

"""-----------------------------------"""

# initialize the logic analyzer with default settings
logic.open(device_handle)

# set up triggering on DIO0 falling edge
logic.trigger(device_handle, enable=True, channel=0, rising_edge=False)

# generate a 100KHz PWM signal with 30% duty cycle on DIO0
pattern.generate(device_handle, channel=0, function=pattern.function.pulse, frequency=100e03, duty_cycle=30)

# record a logic signal on DIO0
buffer, time = logic.record(device_handle, channel=0)

# plot
time = [moment * 1e06 for moment in time]   # convert time to μs
plt.plot(time, buffer)
plt.xlabel("time [μs]")
plt.ylabel("logic value")
plt.yticks([0, 1])
plt.show()

# reset the logic analyzer
logic.close(device_handle)

# reset the pattern generator
pattern.close(device_handle)

"""-----------------------------------"""

# close the connection
device.close(device_handle)
