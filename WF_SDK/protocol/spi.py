""" PROTOCOL: SPI CONTROL FUNCTIONS: open, read, write, exchange, spy, close """

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

class state:
    """ stores the state of the instrument """
    on = False
    off = True

"""-----------------------------------------------------------------------"""

def open(device_data, cs, sck, miso=None, mosi=None, clk_frequency=1e06, mode=0, order=True):
    """
        initializes SPI communication

        parameters: - device data
                    - cs (DIO line used for chip select)
                    - sck (DIO line used for serial clock)
                    - miso (DIO line used for master in - slave out, optional)
                    - mosi (DIO line used for master out - slave in, optional)
                    - frequency (communication frequency in Hz, default is 1MHz)
                    - mode (SPI mode: 0: CPOL=0, CPHA=0; 1: CPOL-0, CPHA=1; 2: CPOL=1, CPHA=0; 3: CPOL=1, CPHA=1)
                    - order (endianness, True means MSB first - default, False means LSB first)
    """
    # set the clock frequency
    dwf.FDwfDigitalSpiFrequencySet(device_data.handle, ctypes.c_double(clk_frequency))

    # set the clock pin
    dwf.FDwfDigitalSpiClockSet(device_data.handle, ctypes.c_int(sck))

    if mosi != None:
        # set the mosi pin
        dwf.FDwfDigitalSpiDataSet(device_data.handle, ctypes.c_int(0), ctypes.c_int(mosi))

        # set the initial state
        dwf.FDwfDigitalSpiIdleSet(device_data.handle, ctypes.c_int(0), constants.DwfDigitalOutIdleZet)

    if miso != None:
        # set the miso pin
        dwf.FDwfDigitalSpiDataSet(device_data.handle, ctypes.c_int(1), ctypes.c_int(miso))

        # set the initial state
        dwf.FDwfDigitalSpiIdleSet(device_data.handle, ctypes.c_int(1), constants.DwfDigitalOutIdleZet)

    # set the SPI mode
    dwf.FDwfDigitalSpiModeSet(device_data.handle, ctypes.c_int(mode))

    # set endianness
    if order:
        # MSB first
        dwf.FDwfDigitalSpiOrderSet(device_data.handle, ctypes.c_int(1))
    else:
        # LSB first
        dwf.FDwfDigitalSpiOrderSet(device_data.handle, ctypes.c_int(0))

    # set the cs pin HIGH
    dwf.FDwfDigitalSpiSelect(device_data.handle, ctypes.c_int(cs), ctypes.c_int(1))

    # dummy write
    dwf.FDwfDigitalSpiWriteOne(device_data.handle, ctypes.c_int(1), ctypes.c_int(0), ctypes.c_int(0))
    
    state.on = True
    state.off = False
    return

"""-----------------------------------------------------------------------"""

def read(device_data, count, cs):
    """
        receives data from SPI

        parameters: - device data
                    - count (number of bytes to receive)
                    - chip select line number

        return:     - integer list containing the received bytes
    """
    # enable the chip select line
    dwf.FDwfDigitalSpiSelect(device_data.handle, ctypes.c_int(cs), ctypes.c_int(0))

    # create buffer to store data
    buffer = (ctypes.c_ubyte*count)()

    # read array of 8 bit elements
    dwf.FDwfDigitalSpiRead(device_data.handle, ctypes.c_int(1), ctypes.c_int(8), buffer, ctypes.c_int(len(buffer)))

    # disable the chip select line
    dwf.FDwfDigitalSpiSelect(device_data.handle, ctypes.c_int(cs), ctypes.c_int(1))

    # decode data
    data = [int(element) for element in buffer]

    return data

"""-----------------------------------------------------------------------"""

def write(device_data, data, cs):
    """
        send data through SPI

        parameters: - device data
                    - data of type string, int, or list of characters/integers
                    - chip select line number
    """
    # cast data
    if type(data) == int:
        data = "".join(chr(data))
    elif type(data) == list:
        data = "".join(chr(element) for element in data)

    # enable the chip select line
    dwf.FDwfDigitalSpiSelect(device_data.handle, ctypes.c_int(cs), ctypes.c_int(0))

    # create buffer to write
    data = bytes(data, "utf-8")
    buffer = (ctypes.c_ubyte * len(data))()
    for index in range(0, len(buffer)):
        buffer[index] = ctypes.c_ubyte(data[index])

    # write array of 8 bit elements
    dwf.FDwfDigitalSpiWrite(device_data.handle, ctypes.c_int(1), ctypes.c_int(8), buffer, ctypes.c_int(len(buffer)))

    # disable the chip select line
    dwf.FDwfDigitalSpiSelect(device_data.handle, ctypes.c_int(cs), ctypes.c_int(1))

    return

"""-----------------------------------------------------------------------"""

def exchange(device_data, data, count, cs):
    """
        sends and receives data using the SPI interface
        
        parameters: - device data
                    - data of type string, int, or list of characters/integers
                    - count (number of bytes to receive)
                    - chip select line number
        
        return:     - integer list containing the received bytes
    """
    # cast data
    if type(data) == int:
        data = "".join(chr(data))
    elif type(data) == list:
        data = "".join(chr(element) for element in data)

    # enable the chip select line
    dwf.FDwfDigitalSpiSelect(device_data.handle, ctypes.c_int(cs), ctypes.c_int(0))

    # create buffer to write
    data = bytes(data, "utf-8")
    tx_buffer = (ctypes.c_ubyte * len(data))()
    for index in range(0, len(tx_buffer)):
        tx_buffer[index] = ctypes.c_ubyte(data[index])

    # create buffer to store data
    rx_buffer = (ctypes.c_ubyte*count)()

    # write to MOSI and read from MISO
    dwf.FDwfDigitalSpiWriteRead(device_data.handle, ctypes.c_int(1), ctypes.c_int(8), tx_buffer, ctypes.c_int(len(tx_buffer)), rx_buffer, ctypes.c_int(len(rx_buffer)))

    # disable the chip select line
    dwf.FDwfDigitalSpiSelect(device_data.handle, ctypes.c_int(cs), ctypes.c_int(1))

    # decode data
    data = [int(element) for element in rx_buffer]

    return data

"""-----------------------------------------------------------------------"""

def spy(device_data, count, cs, sck, mosi=None, miso=None, word_size=8):
    """
        receives data from SPI

        parameters: - device data
                    - count (number of bytes to receive)
                    - chip select line number
                    - serial clock line number
                    - master out - slave in - optional
                    - master in - slave out - optional
                    - word size in bits (default is 8)

        returns:    - class containing the received data: mosi, miso
                    - error message or empty string
    """
    # variable to store errors
    error = ""

    # create static data structure
    class message:
        mosi = 0
        miso = 0

    # record mode
    dwf.FDwfDigitalInAcquisitionModeSet(device_data.handle, constants.acqmodeRecord)

    # for sync mode set divider to -1 
    dwf.FDwfDigitalInDividerSet(device_data.handle, ctypes.c_int(-1))

    # 8 bit per sample format, DIO 0-7
    dwf.FDwfDigitalInSampleFormatSet(device_data.handle, ctypes.c_int(8))

    # continuous sampling 
    dwf.FDwfDigitalInTriggerPositionSet(device_data.handle, ctypes.c_int(-1))

    # in sync mode the trigger is used for sampling condition
    # trigger detector mask: low & high & (rising | falling)
    dwf.FDwfDigitalInTriggerSet(device_data.handle, ctypes.c_int(0), ctypes.c_int(0), ctypes.c_int((1 << sck) | (1 << cs)), ctypes.c_int(0))
    # sample on clock rising edge for sampling bits, or CS rising edge to detect frames

    # start detection
    dwf.FDwfDigitalInConfigure(device_data.handle, ctypes.c_bool(0), ctypes.c_bool(1))

    # fill buffer
    status = ctypes.c_byte()
    available = ctypes.c_int()
    lost = ctypes.c_int()
    corrupted = ctypes.c_int()
    dwf.FDwfDigitalInStatus(device_data.handle, ctypes.c_int(1), ctypes.byref(status))
    dwf.FDwfDigitalInStatusRecord(device_data.handle, ctypes.byref(available), ctypes.byref(lost), ctypes.byref(corrupted))

    # check data integrity
    if lost.value :
        error = "Samples were lost"
    if corrupted.value :
        error = "Samples could be corrupted"

    # limit data size
    if available.value > count :
        available = ctypes.c_int(count)
    
    # load data from internal buffer
    data = (ctypes.c_uint8 * available)()
    dwf.FDwfDigitalInStatusData(device_data.handle, data, available)

    # get message
    bit_count = 0
    for index in range(available.value):
        
        # CS low, active
        if (data[index] >> cs) & 1:
            # log leftover bits, frame not multiple of bit count
            if bit_count != 0:
                # convert data
                message.mosi = chr(message.mosi)
                message.miso = chr(message.miso)
                
                return message, error

        # CS low, active
        else:
            bit_count += 1  # increment bit count

            message.mosi <<= 1 # shift existing bits
            message.miso <<= 1

            # check outgoing data
            if (data[index] >> mosi) & 1:
                message.mosi |= 1
            
            # check incoming data
            if (data[index] >> miso) & 1:
                message.miso |= 1

            # got nBits of bits
            if bit_count >= word_size:
                # convert data
                message.mosi = chr(message.mosi)
                message.miso = chr(message.miso)

                return message, error

    # convert data
    message.mosi = chr(message.mosi)
    message.miso = chr(message.miso)

    return message, error

"""-----------------------------------------------------------------------"""

def close(device_data):
    """
        reset the spi interface
    """
    dwf.FDwfDigitalSpiReset(device_data.handle)
    state.on = False
    state.off = True
    return
