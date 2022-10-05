from WF_SDK import device, error       # import instruments

"""-----------------------------------------------------------------------"""

try:
    # connect to the device
    device_data = device.open()

    """-----------------------------------"""

    filename = device_data.name + ".txt"
    with open(filename, "wt") as f:

        # print device information
        print("WaveForms version: " + device_data.version + "\n", file=f)

        # print device name
        print("Device name: " + device_data.name + "\n", file=f)

        # print analog input information
        print("Analog input information:", file=f)
        print("\tchannels: " + str(device_data.analog.input.channel_count), file=f)
        print("\tmaximum buffer size: " + str(device_data.analog.input.max_buffer_size), file=f)
        print("\tADC resolution: " + str(device_data.analog.input.max_resolution) + " bits", file=f)
        print("\trange settable from " + str(device_data.analog.input.min_range) + "V to " +
                                        str(device_data.analog.input.max_range) + "V in " +
                                        str(device_data.analog.input.steps_range) + " steps", file=f)
        print("\toffset settable from " + str(device_data.analog.input.min_offset) + "V to " +
                                        str(device_data.analog.input.max_offset) + "V in " +
                                        str(device_data.analog.input.steps_offset) + " steps\n", file=f)

        # print analog output information
        print("Analog output information:", file=f)
        for channel_index in range(device_data.analog.output.channel_count):
            print("\tchannel " + str(channel_index) + ":", file=f)
            for node_index in range(device_data.analog.output.node_count[channel_index]):
                print("\t\tnode " + str(node_index) + ":", file=f)
                print("\t\t\tnode type: " + device_data.analog.output.node_type[channel_index][node_index], file=f)
                print("\t\t\tmaximum buffer size: " + str(device_data.analog.output.max_buffer_size[channel_index][node_index]), file=f)
                print("\t\t\tamplitude settable from: " + str(device_data.analog.output.min_amplitude[channel_index][node_index]) + "V to " +
                                                        str(device_data.analog.output.max_amplitude[channel_index][node_index]) + "V", file=f)
                print("\t\t\toffset settable from: " + str(device_data.analog.output.min_offset[channel_index][node_index]) + "V to " +
                                                    str(device_data.analog.output.max_offset[channel_index][node_index]) + "V", file=f)
                print("\t\t\tfrequency settable from: " + str(device_data.analog.output.min_frequency[channel_index][node_index]) + "Hz to " +
                                                        str(device_data.analog.output.max_frequency[channel_index][node_index]) + "Hz\n", file=f)

        # print analog IO information
        print("Analog IO information:", file=f)
        for channel_index in range(device_data.analog.IO.channel_count):
            print("\tchannel " + str(channel_index) + ":", file=f)
            print("\t\tchannel name: " + device_data.analog.IO.channel_name[channel_index], file=f)
            print("\t\tchannel label: " + device_data.analog.IO.channel_label[channel_index], file=f)
            for node_index in range(device_data.analog.IO.node_count[channel_index]):
                print("\t\tnode " + str(node_index) + ":", file=f)
                print("\t\t\tnode name: " + device_data.analog.IO.node_name[channel_index][node_index], file=f)
                print("\t\t\tunit of measurement: " + device_data.analog.IO.node_unit[channel_index][node_index], file=f)
                print("\t\t\tsettable from: " + str(device_data.analog.IO.min_set_range[channel_index][node_index]) + " to " +
                                                str(device_data.analog.IO.max_set_range[channel_index][node_index]) + " in " +
                                                str(device_data.analog.IO.set_steps[channel_index][node_index]) + " steps", file=f)
                print("\t\t\treadable between: " + str(device_data.analog.IO.min_read_range[channel_index][node_index]) + " to " +
                                                str(device_data.analog.IO.max_read_range[channel_index][node_index]) + " in " +
                                                str(device_data.analog.IO.read_steps[channel_index][node_index]) + " steps\n", file=f)


        # print digital input information
        print("Digital input information:", file=f)
        print("\tchannels: " + str(device_data.digital.input.channel_count), file=f)
        print("\tmaximum buffer size: " + str(device_data.digital.input.max_buffer_size) + "\n", file=f)

        # print digital output information
        print("Digital output information:", file=f)
        print("\tchannels: " + str(device_data.digital.output.channel_count), file=f)
        print("\tmaximum buffer size: " + str(device_data.digital.output.max_buffer_size), file=f)

    """-----------------------------------"""

    # close the connection
    device.close(device_data)

except error as e:
    print(e)
    # close the connection
    device.close(device.data)
