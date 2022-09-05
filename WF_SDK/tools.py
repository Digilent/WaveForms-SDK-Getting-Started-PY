""" TOOLS: spectrum """

import ctypes                     # import the C compatible data types
from sys import platform, path    # this is needed to check the OS type and get the PATH
from os import sep                # OS specific file path separators
from math import log10, sqrt      # import necessary math functions

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

class window:
    """ FFT windows """
    rectangular = constants.DwfWindowRectangular
    triangular = constants.DwfWindowTriangular
    hamming = constants.DwfWindowHamming
    hann = constants.DwfWindowHann
    cosine = constants.DwfWindowCosine
    blackman_harris = constants.DwfWindowBlackmanHarris
    flat_top = constants.DwfWindowFlatTop
    kaiser = constants.DwfWindowKaiser

"""-----------------------------------------------------------------------"""

def spectrum(buffer, window, sample_rate, frequency_start, frequency_stop):
    """
        calculates the spectrum of a signal

        parameters: - buffer: list of data points in the signal
                    - window type: rectangular, triangular, hamming, hann, cosine, blackman_harris, flat_top, kaiser
                    - sample rate of the signal in Hz
                    - starting frequency of the spectrum in Hz
                    - end frequency of the spectrum in Hz
    """
    # get and apply window
    buffer_length = len(buffer)
    window_buffer = (ctypes.c_double * buffer_length)()   # create an empty buffer
    dwf.FDwfSpectrumWindow(window_buffer, ctypes.c_int(buffer_length), window, ctypes.c_double(1), ctypes.c_double(0))
    for index in range(buffer_length):
        buffer[index] *= float(window_buffer[index])

    # get the spectrum
    spectrum_length = int(buffer_length / 2 + 1)
    c_spectrum = (ctypes.c_double * spectrum_length)()   # create an empty buffer
    c_buffer = (ctypes.c_double * buffer_length)()
    for index in range(0, len(buffer)):
        c_buffer[index] = ctypes.c_double(buffer[index])
    frequency_start = max(frequency_start * 2.0 / sample_rate, 0.0)
    frequency_stop = min(frequency_stop * 2.0 / sample_rate, 1.0)
    dwf.FDwfSpectrumTransform(c_buffer, ctypes.c_int(buffer_length), c_spectrum, ctypes.c_int(0), ctypes.c_int(spectrum_length), ctypes.c_double(frequency_start), ctypes.c_double(frequency_stop))
    spectrum = []
    for index in range(spectrum_length):
        spectrum.append(20.0 * log10(float(c_spectrum[index]) / sqrt(2)))
    return spectrum
