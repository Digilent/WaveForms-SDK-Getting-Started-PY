""" PROTOCOL: UART CONTROL FUNCTIONS: open, read, write, close """

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
from WF_SDK.device import check_error, warning

"""-----------------------------------------------------------------------"""

def open(device_data, rx, tx, baud_rate=9600, parity=None, data_bits=8, stop_bits=1):
    """
        initializes UART communication
        
        parameters: - device data
                    - rx (DIO line used to receive data)
                    - tx (DIO line used to send data)
                    - baud_rate (communication speed, default is 9600 bits/s)
                    - parity possible: None (default), True means even, False means odd
                    - data_bits (default is 8)
                    - stop_bits (default is 1)
    """
    # set baud rate
    if dwf.FDwfDigitalUartRateSet(device_data.handle, ctypes.c_double(baud_rate)) == 0:
        check_error()

    # set communication channels
    if dwf.FDwfDigitalUartTxSet(device_data.handle, ctypes.c_int(tx)) == 0:
        check_error()
    if dwf.FDwfDigitalUartRxSet(device_data.handle, ctypes.c_int(rx)) == 0:
        check_error()

    # set data bit count
    if dwf.FDwfDigitalUartBitsSet(device_data.handle, ctypes.c_int(data_bits)) == 0:
        check_error()

    # set parity bit requirements
    if parity == True:
        parity = 2
    elif parity == False:
        parity = 1
    else:
        parity = 0
    if dwf.FDwfDigitalUartParitySet(device_data.handle, ctypes.c_int(parity)) == 0:
        check_error()

    # set stop bit count
    if dwf.FDwfDigitalUartStopSet(device_data.handle, ctypes.c_double(stop_bits)) == 0:
        check_error()

    # initialize channels with idle levels

    # dummy read
    dummy_buffer = ctypes.create_string_buffer(0)
    dummy_buffer = ctypes.c_int(0)
    dummy_parity_flag = ctypes.c_int(0)
    if dwf.FDwfDigitalUartRx(device_data.handle, dummy_buffer, ctypes.c_int(0), ctypes.byref(dummy_buffer), ctypes.byref(dummy_parity_flag)) == 0:
        check_error()

    # dummy write
    if dwf.FDwfDigitalUartTx(device_data.handle, dummy_buffer, ctypes.c_int(0)) == 0:
        check_error()
    return

"""-----------------------------------------------------------------------"""

def read(device_data):
    """
        receives data from UART
        
        parameters: - device data

        return:     - integer list containing the received bytes
    """
    # variable to store results
    rx_data = []

    # create empty string buffer
    data = (ctypes.c_ubyte * 8193)()

    # character counter
    count = ctypes.c_int(0)

    # parity flag
    parity_flag= ctypes.c_int(0)

    # read up to 8k characters
    if dwf.FDwfDigitalUartRx(device_data.handle, data, ctypes.c_int(ctypes.sizeof(data)-1), ctypes.byref(count), ctypes.byref(parity_flag)) == 0:
        check_error()

    # append current data chunks
    for index in range(0, count.value):
        rx_data.append(int(data[index]))

    # ensure data integrity
    while count.value > 0:
        # create empty string buffer
        data = (ctypes.c_ubyte * 8193)()

        # character counter
        count = ctypes.c_int(0)

        # parity flag
        parity_flag= ctypes.c_int(0)

        # read up to 8k characters
        if dwf.FDwfDigitalUartRx(device_data.handle, data, ctypes.c_int(ctypes.sizeof(data)-1), ctypes.byref(count), ctypes.byref(parity_flag)) == 0:
            check_error()
        # append current data chunks
        for index in range(0, count.value):
            rx_data.append(int(data[index]))

        # check for not acknowledged
        if parity_flag.value < 0:
            raise warning("Buffer overflow", "read", "protocol/uart")
        elif parity_flag.value > 0:
            raise warning("Parity error: index {}".format(parity_flag.value), "read", "protocol/uart")
    return rx_data

"""-----------------------------------------------------------------------"""

def write(device_data, data):
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
    if dwf.FDwfDigitalUartTx(device_data.handle, data, ctypes.c_int(ctypes.sizeof(data)-1)) == 0:
        check_error()

    return

"""-----------------------------------------------------------------------"""

def close(device_data):
    """
        reset the uart interface
    """
    if dwf.FDwfDigitalUartReset(device_data.handle) == 0:
        check_error()
    return
