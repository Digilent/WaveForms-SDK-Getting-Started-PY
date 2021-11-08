""" IMPORT ISNTRUMENT FUNCTIONS """

import WF_SDK.dwfconstants as constants  # import every constant
import WF_SDK.device as device           # device control functions

"""-----------------------------------------------------------------------"""

""" MAIN PROGRAM """

# connect to the device
device_handle = device.open()

# check for connection errors
device.check_error(device_handle)

# use instruments here

# close the connection
device.close(device_handle)
