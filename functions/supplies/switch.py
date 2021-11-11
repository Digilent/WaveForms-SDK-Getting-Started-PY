def switch(device_handle, device_name, master_state, positive_state, negative_state, positive_voltage, negative_voltage):
    """
        turn the power supplies on/off

        parameters: - device handle
                    - device name
                    - master switch - True = on, False = off
                    - positive supply switch - True = on, False = off
                    - negative supply switch - True = on, False = off
                    - positive supply voltage in Volts
                    - negative supply voltage in Volts
    """
    if device_name == "Analog Discovery":
        switch_fixed(device_handle, master_state, positive_state, negative_state)
    elif device_name == "Analog Discovery 2" or device_name == "Analog Discovery Studio":
        switch_variable(device_handle, master_state, positive_state, negative_state, positive_voltage, negative_voltage)
    elif device_name == "Digital Discovery" or device_name == "Analog Discovery Pro 3X50":
        switch_digital(device_handle, master_state, positive_voltage)
    return
