""" PATTERN GENERATOR CONTROL FUNCTIONS: generate, close """

import ctypes                     # import the C compatible data types
import dwfconstants as constants  # import every constant
from sys import platform          # this is needed to check the OS type

# load the dynamic library (the path is OS specific)
if platform.startswith("win"):
    # on Windows
    dwf = ctypes.cdll.dwf
elif platform.startswith("darwin"):
    # on macOS
    dwf = ctypes.cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    # on Linux
    dwf = ctypes.cdll.LoadLibrary("libdwf.so")

"""-----------------------------------------------------------------------"""

def generate(device_handle, channel, function, frequency, duty_cycle=50, data=[], wait=0, repeat=0, trigger_enabled=False, trigger_source=constants.trigsrcNone, trigger_edge=constants.DwfTriggerSlopeRise):
    """
        generate a logic signal
        
        parameters: - channel - the selected DIO line number
                    - function - possible: DwfDigitalOutTypePulse, DwfDigitalOutTypeCustom, DwfDigitalOutTypeRandom
                    - frequency in Hz
                    - duty cycle in percentage, used only if function = constants.DwfDigitalOutTypePulse, default is 50%
                    - data list, used only if function = constants.DwfDigitalOutTypeCustom, default is empty
                    - wait time in seconds, default is 0 seconds
                    - repeat count, default is infinite (0)
                    - trigger_enabled - include/exclude trigger from repeat cycle
                    - trigger_source - possible: trigsrcDetectorDigitalIn, trigsrcNone, trigsrcDetectorAnalogIn, trigsrcExternal1, trigsrcExternal2, trigsrcExternal3, trigsrcExternal4
                    - trigger_edge - possible: DwfTriggerSlopeRise, DwfTriggerSlopeFall, DwfTriggerSlopeEither
    """
    # get internal clock frequency
    internal_frequency = ctypes.c_double()
    dwf.FDwfDigitalOutInternalClockInfo(device_handle, ctypes.byref(internal_frequency))
    
    # get counter value range
    counter_limit = ctypes.c_uint()
    dwf.FDwfDigitalOutCounterInfo(device_handle, ctypes.c_int(0), ctypes.c_int(0), ctypes.byref(counter_limit))
    
    # calculate the divider for the given signal frequency
    divider = int(-(-(internal_frequency.value / frequency) // counter_limit.value))
    
    # enable the respective channel
    dwf.FDwfDigitalOutEnableSet(device_handle, ctypes.c_int(channel), ctypes.c_int(1))
    
    # set output type
    dwf.FDwfDigitalOutTypeSet(device_handle, ctypes.c_int(channel), function)
    
    # set frequency
    dwf.FDwfDigitalOutDividerSet(device_handle, ctypes.c_int(channel), ctypes.c_int(divider))
    
    # set wait time
    dwf.FDwfDigitalOutWaitSet(device_handle, ctypes.c_double(wait))
    
    # set repeat count
    dwf.FDwfDigitalOutRepeatSet(device_handle, ctypes.c_int(repeat))
    
    # enable triggering
    dwf.FDwfDigitalOutRepeatTriggerSet(device_handle, ctypes.c_int(trigger_enabled))
    
    if not trigger_enabled:
        # set trigger source
        dwf.FDwfDigitalOutTriggerSourceSet(device_handle, trigger_source)
    
        # set trigger slope
        dwf.FDwfDigitalOutTriggerSlopeSet(device_handle, trigger_edge)
    
    # set PWM signal duty cycle
    if function == constants.DwfDigitalOutTypePulse:
        # calculate counter steps to get the required frequency
        steps = int(round(internal_frequency.value / frequency / divider))
        # calculate steps for low and high parts of the period
        high_steps = int(steps * duty_cycle / 100)
        low_steps = int(steps - high_steps)
        dwf.FDwfDigitalOutCounterSet(device_handle, ctypes.c_int(channel), ctypes.c_int(low_steps), ctypes.c_int(high_steps))
    
    # load custom signal data
    elif function == constants.DwfDigitalOutTypeCustom:
        # format data
        buffer = (ctypes.c_ubyte * ((len(data) + 7) >> 3))(0)
        for index in range(len(data)):
            if data[index] != 0:
                buffer[index >> 3] |= 1 << (index & 7)
    
        # load data
        dwf.FDwfDigitalOutDataSet(device_handle, ctypes.c_int(channel), ctypes.byref(buffer), ctypes.c_int(len(data)))
    
    # start generating the signal
    dwf.FDwfDigitalOutConfigure(device_handle, ctypes.c_int(True))
    return

"""-----------------------------------------------------------------------"""

def close(device_handle):
    """
        reset the instrument
    """
    dwf.FDwfDigitalOutReset(device_handle)
    return
