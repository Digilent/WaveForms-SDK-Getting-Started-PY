from WF_SDK import device, scope, wavegen, tools, error   # import instruments

import matplotlib.pyplot as plt   # needed for plotting
from time import sleep            # needed for delays

"""-----------------------------------------------------------------------"""

try:
    # connect to the device
    device_data = device.open()

    """-----------------------------------"""

    # handle devices without analog I/O channels
    if device_data.name != "Digital Discovery":

        # initialize the scope with default settings
        scope.open(device_data)

        # set up triggering on scope channel 1
        scope.trigger(device_data, enable=True, source=scope.trigger_source.analog, channel=1, level=0)

        # generate a 10KHz sine signal with 2V amplitude on channel 1
        wavegen.generate(device_data, channel=1, function=wavegen.function.sine, offset=0, frequency=10e03, amplitude=2)

        sleep(1)    # wait 1 second

        # record data with the scopeon channel 1
        buffer = scope.record(device_data, channel=1)

        # limit displayed data size
        length = len(buffer)
        if length > 10000:
            length = 10000
        buffer = buffer[0:length]

        # generate buffer for time moments
        time = []
        for index in range(len(buffer)):
            time.append(index * 1e03 / scope.data.sampling_frequency)   # convert time to ms

        # plot
        plt.plot(time, buffer)
        plt.xlabel("time [ms]")
        plt.ylabel("voltage [V]")
        plt.show()

        """-----------------------------------"""

        # compute the spectrum from 0Hz to 100KHz
        start_frequency = 0
        stop_frequency = 100e03
        spectrum = tools.spectrum(buffer, tools.window.flat_top, scope.data.sampling_frequency, start_frequency, stop_frequency)

        # calculate frequency domain data
        frequency = []
        length = len(spectrum)
        step = (stop_frequency - start_frequency) / (length - 1)
        for index in range(length):
            frequency.append((start_frequency + index * step) / 1e06)   # convert frequency in MHz
        
        # plot
        plt.plot(frequency, spectrum)
        plt.xlabel("frequency [MHz]")
        plt.ylabel("magnitude [dBV]")
        plt.show()

        """-----------------------------------"""

        # reset the scope
        scope.close(device_data)

        # reset the wavegen
        wavegen.close(device_data)

    """-----------------------------------"""

    # close the connection
    device.close(device_data)

except error as e:
    print(e)
    # close the connection
    device.close(device.data)
