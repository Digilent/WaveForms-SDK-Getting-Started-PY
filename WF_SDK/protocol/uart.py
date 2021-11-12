""" PROTOCOL: UART CONTROL FUNCTIONS: generate, close """

import ctypes                            # import the C compatible data types
import WF_SDK.dwfconstants as constants  # import every constant
from sys import platform                 # this is needed to check the OS type

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

def open(device_handle, rx, tx, baud_rate=9600, parity=None, data_bits=8, stop_bits=1):
    """
        initializes UART communication
        
        parameters: - device handle
                    - rx (DIO line used to receive data)
                    - tx (DIO line used to send data)
                    - baud_rate (communication speed, default is 9600 bits/s)
                    - parity possible: None (default), True means even, False means odd
                    - data_bits (default is 8)
                    - stop_bits (default is 1)
    """
    # set baud rate
    dwf.FDwfDigitalUartRateSet(device_handle, ctypes.c_double(baud_rate))

    # set communication channels
    dwf.FDwfDigitalUartTxSet(device_handle, ctypes.c_int(tx))
    dwf.FDwfDigitalUartRxSet(device_handle, ctypes.c_int(rx))

    # set data bit count
    dwf.FDwfDigitalUartBitsSet(device_handle, ctypes.c_int(data_bits))

    # set parity bit requirements
    if parity == True:
        parity = 2
    elif parity == False:
        parity = 1
    else:
        parity = 0
    dwf.FDwfDigitalUartParitySet(device_handle, ctypes.c_int(parity))

    # set stop bit count
    dwf.FDwfDigitalUartStopSet(device_handle, ctypes.c_double(stop_bits))

    # initialize channels with idle levels

    # dummy read
    dummy_buffer = ctypes.create_string_buffer(0)
    dummy_buffer = ctypes.c_int(0)
    dummy_parity_flag = ctypes.c_int(0)
    dwf.FDwfDigitalUartRx(device_handle, dummy_buffer, ctypes.c_int(0), ctypes.byref(dummy_buffer), ctypes.byref(dummy_parity_flag))

    # dummy write
    dwf.FDwfDigitalUartTx(device_handle, dummy_buffer, ctypes.c_int(0))
    
    return

"""-----------------------------------------------------------------------"""

def receive(device_handle):
    """
        receives data from UART
        
        parameters: - device handle

        return:     - string containing the received bytes
                    - error message or empty string
    """
    # variable to store errors
    error = ""

    # create empty string buffer
    data = ctypes.create_string_buffer(8193)

    # character counter
    count = ctypes.c_int(0)

    # parity flag
    parity_flag= ctypes.c_int(0)

    # read up to 8k characters
    dwf.FDwfDigitalUartRx(device_handle, data, ctypes.c_int(ctypes.sizeof(data)-1), ctypes.byref(count), ctypes.byref(parity_flag))

    data[count.value] = 0  # add zero ending
    
    # make a string from the string buffer
    data = list(data.value)
    previous_data_chunk = "".join(chr(element) for element in data)

    # ensure data integrity
    while count.value > 0:
        # create empty string buffer
        data = ctypes.create_string_buffer(8193)

        # character counter
        count = ctypes.c_int(0)

        # parity flag
        parity_flag= ctypes.c_int(0)

        # read up to 8k characters
        dwf.FDwfDigitalUartRx(device_handle, data, ctypes.c_int(ctypes.sizeof(data)-1), ctypes.byref(count), ctypes.byref(parity_flag))

        data[count.value] = 0  # add zero ending
        
        # make a string from the string buffer
        data = list(data.value)
        data = "".join(chr(element) for element in data)

        # attach to previous data
        previous_data_chunk = previous_data_chunk + data

        # check for not acknowledged
        if error == "":
            if parity_flag.value < 0:
                error = "Buffer overflow"
            elif parity_flag.value > 0:
                error = "Parity error: index {}".format(parity_flag.value)

    return previous_data_chunk, error

"""-----------------------------------------------------------------------"""

def write(device_handle, data):
    """
        send data through UART
        
        parameters: - data of type string, int, or list of characters/integers
    """
    # cast data
    if type(data) == int:
        data = "".join(chr(data))
    elif type(data) == list:
        data = "".join(chr(element) for element in data)

    # encode the string into a string buffer
    data = ctypes.create_string_buffer(data.encode("UTF-8"))

    # send text, trim zero ending
    dwf.FDwfDigitalUartTx(device_handle, data, ctypes.c_int(ctypes.sizeof(data)-1))

    return

"""-----------------------------------------------------------------------"""

def close(device_handle):
    """
        reset the uart interface
    """
    dwf.FDwfDigitalUartReset(device_handle)
    return
