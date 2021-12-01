""" PATTERN GENERATOR CONTROL FUNCTIONS: generate, close """

import ctypes                     # import the C compatible data types
from sys import platform, path    # this is needed to check the OS type and get the PATH
from os import sep                # OS specific file path separators

# load the dynamic library, get constants path (the path is OS specific)
if platform.startswith("win"):
    # on Windows
    dwf = ctypes.cdll.dwf
    constants_path = "C:" + sep + "Program Files (x86)" + sep + "Digilent" + sep + "WaveFormsSDK" + sep + "samples" + sep + "py"
elif platform.startswith("darwin"):
    # on macOS
    lib_path = sep + "Library" + sep + "Frameworks" + sep + "dwf.framework" + sep + "dwf"
    dwf = ctypes.cdll.LoadLibrary(lib_path)
    constants_path = sep + "Applications" + sep + "WaveForms.app" + sep + "Contents" + sep + "Resources" + sep + "SDK" + sep + "samples" + sep + "py"
else:
    # on Linux
    dwf = ctypes.cdll.LoadLibrary("libdwf.so")
    constants_path = sep + "usr" + sep + "share" + sep + "digilent" + sep + "waveforms" + sep + "samples" + sep + "py"

# import constants
path.append(constants_path)
import dwfconstants as constants

"""-----------------------------------------------------------------------"""

class function:
    """ function names """
    pulse = constants.DwfDigitalOutTypePulse
    custom = constants.DwfDigitalOutTypeCustom
    random = constants.DwfDigitalOutTypeRandom

"""-----------------------------------------------------------------------"""

class trigger_source:
    """ trigger source names """
    none = constants.trigsrcNone
    analog = constants.trigsrcDetectorAnalogIn
    digital = constants.trigsrcDetectorDigitalIn
    external = [None, constants.trigsrcExternal1, constants.trigsrcExternal2, constants.trigsrcExternal3, constants.trigsrcExternal4]

"""-----------------------------------------------------------------------"""

def generate(device_handle, channel, function, frequency, duty_cycle=50, data=[], wait=0, repeat=0, trigger_enabled=False, trigger_source=trigger_source.none, trigger_edge_rising=True):
    """
        generate a logic signal
        
        parameters: - channel - the selected DIO line number
                    - function - possible: pulse, custom, random
                    - frequency in Hz
                    - duty cycle in percentage, used only if function = pulse, default is 50%
                    - data list, used only if function = custom, default is empty
                    - wait time in seconds, default is 0 seconds
                    - repeat count, default is infinite (0)
                    - trigger_enabled - include/exclude trigger from repeat cycle
                    - trigger_source - possible: none, analog, digital, external[1-4]
                    - trigger_edge_rising - True means rising, False means falling, None means either, default is rising
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
        if trigger_edge_rising == True:
            # rising edge
            dwf.FDwfDigitalOutTriggerSlopeSet(device_handle, constants.DwfTriggerSlopeRise)
        elif trigger_edge_rising == False:
            # falling edge
            dwf.FDwfDigitalOutTriggerSlopeSet(device_handle, constants.DwfTriggerSlopeFall)
        elif trigger_edge_rising == None:
            # either edge
            dwf.FDwfDigitalOutTriggerSlopeSet(device_handle, constants.DwfTriggerSlopeEither)

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
