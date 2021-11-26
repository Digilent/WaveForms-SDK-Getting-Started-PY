def switch(device_handle, supplies_state):
    """
        turn the power supplies on/off

        parameters: - device handle
                    - class containing supplies data:
                        - device_name
                        - master_state
                        - state and/or positive_state and negative_state
                        - voltage and/or positive_voltage and negative_voltage
                        - current and/or positive_current and negative_current

        returns:    - True on success, False on error
    """
    if supplies_state.device_name == "Analog Discovery":
        # switch fixed supplies on AD
        try:
            # switch both supplies
            switch_fixed(device_handle, supplies_state.master_state, supplies_state.positive_state, supplies_state.negative_state)
            return True
        except:
            try:
                # switch only the positive supply
                switch_fixed(device_handle, supplies_state.master_state, supplies_state.state, False)
                return True
            except:
                return False

    elif supplies_state.device_name == "Analog Discovery 2" or supplies_state.device_name == "Analog Discovery Studio":
        # switch variable supplies on AD2
        try:
            # switch both supplies
            switch_variable(device_handle, supplies_state.master_state, supplies_state.positive_state, supplies_state.negative_state, supplies_state.positive_voltage, supplies_state.negative_voltage)
            return True
        except:
            # switch only the positive supply
            try:
                switch_variable(device_handle, supplies_state.master_state, supplies_state.state, False, supplies_state.voltage, 0)
                return True
            except:
                return False

    elif supplies_state.device_name == "Digital Discovery" or supplies_state.device_name == "Analog Discovery Pro 3X50":
        # switch the digital supply on DD, or ADP3x50
        try:
            if supplies_state.master_state == True:
                switch_digital(device_handle, supplies_state.state, supplies_state.voltage)
            elif supplies_state.master_state == False:
                switch_digital(device_handle, False, 3.3)
            return True
        except:
            return False

    elif supplies_state.device_name == "Analog Discovery Pro 5250":
        error_flag = False

        # switch the 6V supply on ADP5250
        try:
            if supplies_state.master_state == True:
                try:
                    # try to limit the current
                    switch_6V(device_handle, supplies_state.state, supplies_state.voltage, supplies_state.current)
                except:
                    try:
                        # try without current limitation
                        switch_6V(device_handle, supplies_state.state, supplies_state.voltage)
                    except:
                        error_flag = True
            elif supplies_state.master_state == False:
                switch_6V(device_handle, False, 0, 1)
        except:
            error_flag = True
        
        # switch the 25V supplies on ADP5250
        try:
            if supplies_state.master_state == True:
                try:
                   # try both suplpies with current limitation
                   switch_25V(device_handle, supplies_state.positive_state, supplies_state.negative_state, supplies_state.positive_voltage, supplies_state.negative_voltage, supplies_state.positive_current, supplies_state.negative_current)
                   return True
                except:
                    try:
                        # try both supplies without current limitation
                        switch_25V(device_handle, supplies_state.positive_state, supplies_state.negative_state, supplies_state.positive_voltage, supplies_state.negative_voltage)
                        return True
                    except:
                        if error_flag:
                            return False
                        else:
                            return True
            elif supplies_state.master_state == False:
                switch_25V(device_handle, False, False, 0, 0, 0.5, -0.5)
                return True
        except:
            if error_flag:
                return False
            else:
                return True

    return False
