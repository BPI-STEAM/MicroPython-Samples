# MicroPython ST7735 TFT display driver

class ST7735(object):

    # command definitions
    CMD_NOP     = const(0x00) # No Operation
    CMD_SWRESET = const(0x01) # Software reset
    CMD_RDDID   = const(0x04) # Read Display ID
    CMD_RDDST   = const(0x09) # Read Display Status

    CMD_SLPIN   = const(0x10) # Sleep in & booster off
    CMD_SLPOUT  = const(0x11) # Sleep out & booster on
    CMD_PTLON   = const(0x12) # Partial mode on
    CMD_NORON   = const(0x13) # Partial off (Normal)

    CMD_INVOFF  = const(0x20) # Display inversion off
    CMD_INVON   = const(0x21) # Display inversion on
    CMD_DISPOFF = const(0x28) # Display off
    CMD_DISPON  = const(0x29) # Display on
    CMD_CASET   = const(0x2A) # Column address set
    CMD_RASET   = const(0x2B) # Row address set
    CMD_RAMWR   = const(0x2C) # Memory write
    CMD_RAMRD   = const(0x2E) # Memory read

    CMD_PTLAR   = const(0x30) # Partial start/end address set
    CMD_COLMOD  = const(0x3A) # Interface pixel format
    CMD_MADCTL  = const(0x36) # Memory data access control

    CMD_RDID1   = const(0xDA) # Read ID1
    CMD_RDID2   = const(0xDB) # Read ID2
    CMD_RDID3   = const(0xDC) # Read ID3
    CMD_RDID4   = const(0xDD) # Read ID4

    # panel function commands
    CMD_FRMCTR1 = const(0xB1) # In normal mode (Full colors)
    CMD_FRMCTR2 = const(0xB2) # In Idle mode (8-colors)
    CMD_FRMCTR3 = const(0xB3) # In partial mode + Full colors
    CMD_INVCTR  = const(0xB4) # Display inversion control

    CMD_PWCTR1  = const(0xC0) # Power control settings
    CMD_PWCTR2  = const(0xC1) # Power control settings
    CMD_PWCTR3  = const(0xC2) # In normal mode (Full colors)
    CMD_PWCTR4  = const(0xC3) # In Idle mode (8-colors)
    CMD_PWCTR5  = const(0xC4) # In partial mode + Full colors
    CMD_VMCTR1  = const(0xC5) # VCOM control

    CMD_GMCTRP1 = const(0xE0)
    CMD_GMCTRN1 = const(0xE1)

    # colors
    COLOR_BLACK   = const(0x0000)
    COLOR_BLUE    = const(0x001F)
    COLOR_RED     = const(0xF800)
    COLOR_GREEN   = const(0x07E0)
    COLOR_CYAN    = const(0x07FF)
    COLOR_MAGENTA = const(0xF81F)
    COLOR_YELLOW  = const(0xFFE0)
    COLOR_WHITE   = const(0xFFFF)

    def __init__(self, width, height):
        # self.tab        = tab
        self.width        = width
        self.height       = height
        self.power_on     = True
        self.inverted     = False
        self.backlight_on = True

        # default margins, set yours in HAL init
        self.margin_row = 0
        self.margin_col = 0

    def _set_window(self, x0, y0, x1, y1):
        """
        Set window frame boundaries.

        Any pixels written to the display will start from this area.
        """
        # set row XSTART/XEND
        self.write_cmd(bytearray([CMD_RASET]))
        self.write_data(bytearray(
            [0x00, y0 + self.margin_row, 0x00, y1 + self.margin_row])
        )

        # set column XSTART/XEND
        self.write_cmd(bytearray([CMD_CASET]))
        self.write_data(bytearray(
            [0x00, x0 + self.margin_col, 0x00, x1 + self.margin_col])
        )

        # write addresses to RAM
        self.write_cmd(bytearray([CMD_RAMWR]))

    def power(self, state=None):
        """
        Get/set display power.
        """
        if state is None:
            return self.power_on
        self.write_cmd(bytearray([CMD_DISPON if state else CMD_DISPOFF]))
        self.power_on = state

    def clear(self, color=COLOR_WHITE):
        """
        Clear the display filling it with color.
        """
        self.rect(0, 0, self.width, self.height, color)

    def invert(self, state=None):
        """
        Get/set display color inversion.
        """
        if state is None:
            return self.inverted
        self.write_cmd(bytearray([CMD_INVON if state else CMD_INVOFF]))
        self.inverted = state

    def rgbcolor(self, r, g, b):
        """
        Pack 24-bit RGB into 16-bit value.
        """
        return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)

    def pixel(self, x, y, color):
        """
        Draw a single pixel on the display with given color.
        """
        self._set_window(x, y, x + 1, y + 1)
        self.write_pixels(1, bytearray([color >> 8, color]))

    def rect(self, x, y, w, h, color):
        """
        Draw a rectangle with specified coordinates/size and fill with color.
        """
        # check the coordinates and trim if necessary
        if (x >= self.width) or (y >= self.height):
            return
        if (x + w - 1) >= self.width:
            w = self.width - x
        if (y + h - 1) >= self.height:
            h = self.height - y

        self._set_window(x, y, x + w - 1, y + h - 1)
        self.write_pixels((w*h), bytearray([color >> 8, color]))

    def line(self, x0, y0, x1, y1, color):
        # line is vertical
        if x0 == x1:
            # use the smallest y
            start, end = (x1, y1) if y1 < y0 else (x0, y0)
            self.vline(start, end, abs(y1 - y0) + 1, color)

        # line is horizontal
        elif y0 == y1:
            # use the smallest x
            start, end = (x1, y1) if x1 < x0 else (x0, y0)
            self.hline(start, end, abs(x1 - x0) + 1, color)

        else:
            # Bresenham's algorithm
            dx = abs(x1 - x0)
            dy = abs(y1 - y0)
            inx = 1 if x1 - x0 > 0 else -1
            iny = 1 if y1 - y0 > 0 else -1

            # steep line
            if (dx >= dy):
                dy <<= 1
                e = dy - dx
                dx <<= 1
                while (x0 != x1):
                    # draw pixels
                    self.pixel(x0, y0, color)
                    if (e >= 0):
                        y0 += iny
                        e -= dx
                    e += dy
                    x0 += inx

            # not steep line
            else:
                dx <<= 1
                e = dx - dy
                dy <<= 1
                while(y0 != y1):
                    # draw pixels
                    self.pixel(x0, y0, color)
                    if (e >= 0):
                        x0 += inx
                        e -= dy
                    e += dx
                    y0 += iny

    def hline(self, x, y, w, color):
        if (x >= self.width) or (y >= self.height):
            return
        if (x + w - 1) >= self.width:
            w = self.width - x

        self._set_window(x, y, x + w - 1, y)
        self.write_pixels(x+w-1, bytearray([color >> 8, color]))

    def vline(self, x, y, h, color):
        if (x >= self.width) or (y >= self.height):
            return
        if (y + h -1) >= self.height:
            h = self.height - y

        self._set_window(x, y, x, y + h - 1)
        self.write_pixels(y+h-1, bytearray([color >> 8, color]))

    def text(self, x, y, string, font, color, size=1):
        """
        Draw text at a given position using the user font.
        Font can be scaled with the size parameter.
        """
        if font is None:
            return

        width = size * font['width'] + 1

        px = x
        for c in string:
            self.char(px, y, c, font, color, size, size)
            px += width

            # wrap the text to the next line if it reaches the end
            if px + width > self.width:
                y += font['height'] * size + 1
                px = x

    def char(self, x, y, char, font, color, sizex=1, sizey=1):
        """
        Draw a character at a given position using the user font.

        Font is a data dictionary, can be scaled with sizex and sizey.
        """
        if font is None:
            return

        startchar = font['start']
        endchar = font['end']
        ci = ord(char)

        if (startchar <= ci <= endchar):
            width = font['width']
            height = font['height']
            ci = (ci - startchar) * width

            ch = font['data'][ci:ci + width]

            # no font scaling
            px = x
            if (sizex <= 1 and sizey <= 1):
                for c in ch:
                    py = y
                    for _ in range(height):
                        if c & 0x01:
                            self.pixel(px, py, color)
                        py += 1
                        c >>= 1
                    px += 1

            # scale to given sizes
            else:
                for c in ch:
                    py = y
                    for _ in range(height):
                        if c & 0x01:
                            self.rect(px, py, sizex, sizey, color)
                        py += sizey
                        c >>= 1
                    px += sizex
        else:
            # character not found in this font
            return

    def init(self):
        """
        HAL: Init your "tab" version of the display.
        """
        raise NotImplementedError

    def reset(self):
        """
        HAL: Display reset command.
        """
        raise NotImplementedError

    def backlight(self, state):
        """
        HAL: Toggle display backlight depending on given state.
        """
        raise NotImplementedError

    def write_pixels(self, count, color):
        """
        HAL: Write individual pixels to the display.
        """
        raise NotImplementedError

    def write_cmd(self, cmd):
        """
        HAL: Write a command to the display.
        """
        raise NotImplementedError

    def write_data(self, data):
        """
        HAL: Write data to the display.
        """
        raise NotImplementedError
