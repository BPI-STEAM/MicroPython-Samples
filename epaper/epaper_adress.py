"""
MicroPython Waveshare 2.13" Black/White/Red GDEW0213Z16 e-paper display driver
https://github.com/mcauser/micropython-waveshare-epaper
"""

# also works for black/white/yellow GDEW0213C38?

from micropython import const

# Display resolution
EPD_WIDTH = const(104)
EPD_HEIGHT = const(212)
# Display commands
PANEL_SETTING = const(0x00)
POWER_SETTING = const(0x01)
POWER_OFF = const(0x02)
# POWER_OFF_SEQUENCE_SETTING     = const(0x03)
POWER_ON = const(0x04)
# POWER_ON_MEASURE               = const(0x05)
BOOSTER_SOFT_START = const(0x06)
# DEEP_SLEEP                     = const(0x07)
DATA_START_TRANSMISSION_1 = const(0x10)
# DATA_STOP                      = const(0x11)
DISPLAY_REFRESH = const(0x12)
DATA_START_TRANSMISSION_2 = const(0x13)
# VCOM_LUT                       = const(0x20) # VCOM LUT(LUTC) (45-byte command, structure of bytes 2~7 repeated)
# W2W_LUT                        = const(0x21) # W2W LUT (LUTWW) (43-byte command, structure of bytes 2~7 repeated 7 times)
# B2W_LUT                        = const(0x22) # B2W LUT (LUTBW / LUTR) (43-byte command, structure of bytes 2~7 repeated 7 times)
# W2B_LUT                        = const(0x23) # W2B LUT (LUTWB / LUTW) (43-byte command, structure of bytes 2~7 repeated 7 times)
# B2B_LUT                        = const(0x24) # B2B LUT (LUTBB / LUTB) (43-byte command, sturcture of bytes 2~7 repeated 7 times)
# PLL_CONTROL                    = const(0x30)
# TEMPERATURE_SENSOR_CALIBRATION = const(0x40)
# TEMPERATURE_SENSOR_SELECTION   = const(0x41)
# TEMPERATURE_SENSOR_WRITE       = const(0x42)
# TEMPERATURE_SENSOR_READ        = const(0x43)
VCOM_AND_DATA_INTERVAL_SETTING = const(0x50)
# LOW_POWER_DETECTION            = const(0x51)
# TCON_SETTING                   = const(0x60)
RESOLUTION_SETTING = const(0x61)
# GET_STATUS                     = const(0x71) # partial update status, i2c status, data received, power status, busy
# AUTO_MEASURE_VCOM              = const(0x80)
# VCOM_VALUE                     = const(0x81)
VCM_DC_SETTING = const(0x82)
# PARTIAL_WINDOW                 = const(0x90)
# PARTIAL_IN                     = const(0x91)
# PARTIAL_OUT                    = const(0x92)
# PROGRAM_MODE                   = const(0xA0)
# ACTIVE_PROGRAM                 = const(0xA1)
# READ_OTP_DATA                  = const(0xA2)
# POWER_SAVING                   = const(0xE3)
# Display orientation
ROTATE_0 = const(0)
ROTATE_90 = const(1)
ROTATE_180 = const(2)
ROTATE_270 = const(3)
BUSY = const(0)  # 0=busy, 1=idle
