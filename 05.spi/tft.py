# MicroPython ST7735 TFT display HAL

import time
from st7735 import ST7735

class TFT(ST7735):

    def __init__(self, width, height, spi, dc, cs, rst, bl=None):
        """
        SPI      - SPI Bus (CLK/MOSI/MISO)
        DC       - RS/DC data/command flag
        CS       - Chip Select, enable communication
        RST/RES  - Reset
        BL/Lite  - Backlight control
        """

        # self.tab = tab
        self.spi = spi
        self.dc  = dc
        self.cs  = cs
        self.rst = rst
        self.bl  = bl

        # ST7735 init
        super().__init__(width, height)

    # ST7735 HAL
    def init(self):
        """
        Define your init for different display tab color versions.
        """
        raise NotImplementedError

        # self.clear()
        # self.power(True)

    def reset(self):
        """
        Hard reset the display.
        """
        self.dc.value(0)
        self.rst.value(1)
        time.sleep_ms(500)
        self.rst.value(0)
        time.sleep_ms(500)
        self.rst.value(1)
        time.sleep_ms(500)

    def backlight(self, state=None):
        """
        Get or set the backlight status if the pin is available.
        """
        if self.bl is None:
            return None
        else:
            if state is None:
                return self.backlight_on
            self.bl.value(1 if state else 0)
            self.backlight_on = state

    def write_pixels(self, count, color):
        """
        Write pixels to the display.
        count - total number of pixels
        color - 16-bit RGB value
        """
        self.dc.value(1)
        self.cs.value(0)
        for _ in range(count):
            self.spi.write(color)
        self.cs.value(1)

    def write_cmd(self, cmd):
        """
        Display command write implementation using SPI.
        """
        self.dc.value(0)
        self.cs.value(0)
        self.spi.write(cmd)
        self.cs.value(1)

    def write_data(self, data):
        """
        Display data write implementation using SPI.
        """
        self.dc.value(1)
        self.cs.value(0)
        self.spi.write(data)
        self.cs.value(1)

class TFT_GREEN(TFT):

    def __init__(self, width, height, spi, dc, cs, rst, bl=None):
        super().__init__(width, height, spi, dc, cs, rst, bl)

    def init(self):
        # set column and row margins
        self.margin_row = 1
        self.margin_col = 2

        # hard reset first
        self.reset()

        self.write_cmd(bytearray([TFT.CMD_SWRESET]))
        time.sleep_ms(150)
        self.write_cmd(bytearray([TFT.CMD_SLPOUT]))
        time.sleep_ms(255)

        # TODO: optimize data streams and delays
        self.write_cmd(bytearray([TFT.CMD_FRMCTR1]))
        self.write_data(bytearray([0x01, 0x2C, 0x2D]))
        self.write_cmd(bytearray([TFT.CMD_FRMCTR2]))
        self.write_data(bytearray([0x01, 0x2C, 0x2D, 0x01, 0x2C, 0x2D]))
        time.sleep_ms(10)

        self.write_cmd(bytearray([TFT.CMD_INVCTR]))
        self.write_data(bytearray([0x07]))

        self.write_cmd(bytearray([TFT.CMD_PWCTR1]))
        self.write_data(bytearray([0xA2, 0x02, 0x84]))
        self.write_cmd(bytearray([TFT.CMD_PWCTR2]))
        self.write_data(bytearray([0xC5]))
        self.write_cmd(bytearray([TFT.CMD_PWCTR3]))
        self.write_data(bytearray([0x8A, 0x00]))
        self.write_cmd(bytearray([TFT.CMD_PWCTR4]))
        self.write_data(bytearray([0x8A, 0x2A]))
        self.write_cmd(bytearray([TFT.CMD_PWCTR5]))
        self.write_data(bytearray([0x8A, 0xEE]))

        self.write_cmd(bytearray([TFT.CMD_VMCTR1]))
        self.write_data(bytearray([0x0E]))

        self.write_cmd(bytearray([TFT.CMD_INVOFF]))
        self.write_cmd(bytearray([TFT.CMD_MADCTL]))
        self.write_data(bytearray([0x00])) # RGB

        self.write_cmd(bytearray([TFT.CMD_COLMOD]))
        self.write_data(bytearray([0x05]))

        self.write_cmd(bytearray([TFT.CMD_CASET]))
        self.write_data(bytearray([0x00, 0x01, 0x00, 127]))

        self.write_cmd(bytearray([TFT.CMD_RASET]))
        self.write_data(bytearray([0x00, 0x01, 0x00, 119]))

        self.write_cmd(bytearray([TFT.CMD_GMCTRP1]))
        self.write_data(bytearray([0x02, 0x1c, 0x07, 0x12, 0x37, 0x32,
            0x29, 0x2d, 0x29, 0x25, 0x2b, 0x39, 0x00, 0x01, 0x03, 0x10]))

        self.write_cmd(bytearray([TFT.CMD_GMCTRN1]))
        self.write_data(bytearray([0x03, 0x1d, 0x07, 0x06, 0x2e, 0x2c,
            0x29, 0x2d, 0x2e, 0x2e, 0x37, 0x3f, 0x00, 0x00, 0x02, 0x10]))

        self.write_cmd(bytearray([TFT.CMD_NORON]))
        time.sleep_ms(10)

        self.write_cmd(bytearray([TFT.CMD_DISPON]))
        time.sleep_ms(100)