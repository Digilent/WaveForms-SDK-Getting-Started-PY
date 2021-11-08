""" WAVEFORM GENERATOR CONTROL FUNCTIONS: generate, close """

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

def generate(device_handle, channel, function, offset, frequency=1e03, amplitude=1, symmetry=50, wait=0, run_time=0, repeat=0, data=[]):
    """
        generate an analog signal

        parameters: - device handle
                    - the selected wavegen channel (1-2)
                    - function - possible: funcCustom, funcSine, funcSquare, funcTriangle, funcNoise, funcDC, funcPulse, funcTrapezium, funcSinePower, funcRampUp, funcRampDown
                    - offset voltage in Volts
                    - frequency in Hz, default is 1KHz
                    - amplitude in Volts, default is 1V
                    - signal symmetry in percentage, default is 50%
                    - wait time in seconds, default is 0s
                    - run time in seconds, default is infinite (0)
                    - repeat count, default is infinite (0)
                    - data - list of voltages, used only if function=constants.funcCustom, default is empty
    """
    # enable channel
    channel = ctypes.c_int(channel - 1)
    dwf.FDwfAnalogOutNodeEnableSet(device_handle, channel, constants.AnalogOutNodeCarrier, ctypes.c_bool(True))
    
    # set function type
    dwf.FDwfAnalogOutNodeFunctionSet(device_handle, channel, constants.AnalogOutNodeCarrier, function)
    
    # load data if the function type is custom
    if function == constants.funcCustom:
        data_length = len(data)
        buffer = (ctypes.c_double * data_length)()
        for index in range(0, len(buffer)):
            buffer[index] = ctypes.c_double(data[index])
        dwf.FDwfAnalogOutNodeDataSet(device_handle, channel, constants.AnalogOutNodeCarrier, buffer, ctypes.c_int(data_length))
    
    # set frequency
    dwf.FDwfAnalogOutNodeFrequencySet(device_handle, channel, constants.AnalogOutNodeCarrier, ctypes.c_double(frequency))
    
    # set amplitude or DC voltage
    dwf.FDwfAnalogOutNodeAmplitudeSet(device_handle, channel, constants.AnalogOutNodeCarrier, ctypes.c_double(amplitude))
    
    # set offset
    dwf.FDwfAnalogOutNodeOffsetSet(device_handle, channel, constants.AnalogOutNodeCarrier, ctypes.c_double(offset))
    
    # set symmetry
    dwf.FDwfAnalogOutNodeSymmetrySet(device_handle, channel, constants.AnalogOutNodeCarrier, ctypes.c_double(symmetry))
    
    # set running time limit
    dwf.FDwfAnalogOutRunSet(device_handle, channel, ctypes.c_double(run_time))
    
    # set wait time before start
    dwf.FDwfAnalogOutWaitSet(device_handle, channel, ctypes.c_double(wait))
    
    # set number of repeating cycles
    dwf.FDwfAnalogOutRepeatSet(device_handle, channel, ctypes.c_int(repeat))
    
    # start
    dwf.FDwfAnalogOutConfigure(device_handle, channel, ctypes.c_bool(True))
    return

"""-----------------------------------------------------------------------"""

def close(device_handle):
    """
        reset the wavegen
    """
    dwf.FDwfAnalogOutReset(device_handle)
    return
