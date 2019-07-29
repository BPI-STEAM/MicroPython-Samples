

import gc
from epaper_adress import POWER_ON, EPD_WIDTH, EPD_HEIGHT, RESOLUTION_SETTING, VCOM_AND_DATA_INTERVAL_SETTING, PANEL_SETTING, BOOSTER_SOFT_START, DATA_START_TRANSMISSION_1, DATA_START_TRANSMISSION_2, DISPLAY_REFRESH, ROTATE_0, ROTATE_90, ROTATE_180, ROTATE_270, BUSY

from machine import Pin, SPI
import utime
from utime import sleep_ms
import ustruct


class EPD:

    def __init__(self, spi, cs, dc, rst, busy):

        self.spi = spi
        self.cs = cs
        self.dc = dc
        self.rst = rst
        self.busy = busy
        self.cs.init(self.cs.OUT, value=1)
        self.dc.init(self.dc.OUT, value=0)
        self.rst.init(self.rst.OUT, value=0)
        self.busy.init(self.busy.IN)
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT
        self.rotate = ROTATE_0

    def _command(self, command, data=None):
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([command]))
        self.cs(1)
        if data is not None:
            self._data(data)

    def _data(self, data):
        self.dc(1)
        self.cs(0)
        self.spi.write(data)
        self.cs(1)

    def init(self):
        self.reset()
        self._command(BOOSTER_SOFT_START, b'\x17\x17\x17')
        self._command(POWER_ON)
        self.wait_until_idle()

        # (128x296, LUT from OTP, B/W/R, scan up, shift right, booster on)
        self._command(PANEL_SETTING, b'\x8F')
        self._command(VCOM_AND_DATA_INTERVAL_SETTING, b'\x37')
        self._command(RESOLUTION_SETTING, b'\x68\x00\xD4')

    def wait_until_idle(self):
        while self.busy.value() == BUSY:
            sleep_ms(100)

    def reset(self):
        self.rst(0)
        sleep_ms(200)
        self.rst(1)
        sleep_ms(200)

    def display_frame(self, frame_buffer_black, frame_buffer_red):
        if (frame_buffer_black is not None):
            self._command(DATA_START_TRANSMISSION_1)
            sleep_ms(2)
            for i in range(0, self.width * self.height // 8):
                self._data(bytearray([frame_buffer_black[i]]))
            sleep_ms(2)

        if (frame_buffer_red is not None):
            self._command(DATA_START_TRANSMISSION_2)
            sleep_ms(2)
            for i in range(0, self.width * self.height // 8):
                self._data(bytearray([frame_buffer_red[i]]))

            sleep_ms(2)

        self._command(DISPLAY_REFRESH)
        self.wait_until_idle()

    def set_rotate(self, rotate):
        if (rotate == ROTATE_0):
            self.rotate = ROTATE_0
            self.width = EPD_WIDTH
            self.height = EPD_HEIGHT
        elif (rotate == ROTATE_90):
            self.rotate = ROTATE_90
            self.width = EPD_HEIGHT
            self.height = EPD_WIDTH
        elif (rotate == ROTATE_180):
            self.rotate = ROTATE_180
            self.width = EPD_WIDTH
            self.height = EPD_HEIGHT
        elif (rotate == ROTATE_270):
            self.rotate = ROTATE_270
            self.width = EPD_HEIGHT
            self.height = EPD_WIDTH

    def set_pixel(self, frame_buffer, x, y, colored):

        if (x < 0 or x >= self.width or y < 0 or y >= self.height):
            return

        if (self.rotate == ROTATE_0):
            self.set_absolute_pixel(frame_buffer, x, y, colored)

        elif (self.rotate == ROTATE_90):
            point_temp = x
            x = EPD_WIDTH - y
            y = point_temp
            self.set_absolute_pixel(frame_buffer, x, y, colored)

        elif (self.rotate == ROTATE_180):
            x = EPD_WIDTH - x
            y = EPD_HEIGHT - y
            self.set_absolute_pixel(frame_buffer, x, y, colored)

        elif (self.rotate == ROTATE_270):
            point_temp = x
            x = y
            y = EPD_HEIGHT - point_temp
            self.set_absolute_pixel(frame_buffer, x, y, colored)

    def set_absolute_pixel(self, frame_buffer, x, y, colored):

        # To avoid display orientation effects
        # use EPD_WIDTH instead of self.width
        # use EPD_HEIGHT instead of self.height

        if (x < 0 or x >= EPD_WIDTH or y < 0 or y >= EPD_HEIGHT):
            return

        if (colored):
            frame_buffer[(x + y * EPD_WIDTH) // 8] &= ~(0x80 >> (x % 8))
        else:
            frame_buffer[(x + y * EPD_WIDTH) // 8] |= 0x80 >> (x % 8)

    # def draw_string_at(self, frame_buffer, x, y, text, font, colored):
    #
    #     image = Image.new('1', (self.width, self.height))
    #
    #     draw = ImageDraw.Draw(image)
    #
    #     draw.text((x, y), text, font = font, fill = 255)
    #
    #     # Set buffer to value of Python Imaging Library image.
    #
    #     # Image must be in mode 1.
    #
    #     pixels = image.load()
    #
    #     for y in range(self.height):
    #
    #         for x in range(self.width):
    #
    #             # Set the bits for the column of pixels at the current position.
    #
    #             if pixels[x, y] is not 0:
    #
    #                 self.set_pixel(frame_buffer, x, y, colored)
    #

    def draw_line(self, frame_buffer, x0, y0, x1, y1, colored):

        # Bresenham algorithm

        dx = abs(x1 - x0)

        sx = 1 if x0 < x1 else -1

        dy = -abs(y1 - y0)

        sy = 1 if y0 < y1 else -1

        err = dx + dy

        while((x0 is not x1) and (y0 is not y1)):

            self.set_pixel(frame_buffer, x0, y0, colored)

            if (2 * err >= dy):

                err += dy

                x0 += sx

            if (2 * err <= dx):

                err += dx

                y0 += sy

    def draw_horizontal_line(self, frame_buffer, x, y, width, colored):

        for i in range(x, x + width):

            self.set_pixel(frame_buffer, i, y, colored)

    def draw_vertical_line(self, frame_buffer, x, y, height, colored):

        for i in range(y, y + height):

            self.set_pixel(frame_buffer, x, i, colored)

    def draw_rectangle(self, frame_buffer, x0, y0, x1, y1, colored):

        min_x = x0 if x1 > x0 else x1

        max_x = x1 if x1 > x0 else x0

        min_y = y0 if y1 > y0 else y1

        max_y = y1 if y1 > y0 else y0

        self.draw_horizontal_line(
            frame_buffer, min_x, min_y, max_x - min_x + 1, colored)

        self.draw_horizontal_line(
            frame_buffer, min_x, max_y, max_x - min_x + 1, colored)

        self.draw_vertical_line(frame_buffer, min_x,
                                min_y, max_y - min_y + 1, colored)

        self.draw_vertical_line(frame_buffer, max_x,
                                min_y, max_y - min_y + 1, colored)

    def draw_filled_rectangle(self, frame_buffer, x0, y0, x1, y1, colored):

        min_x = x0 if x1 > x0 else x1

        max_x = x1 if x1 > x0 else x0

        min_y = y0 if y1 > y0 else y1

        max_y = y1 if y1 > y0 else y0

        for i in range(min_x, max_x + 1):

            self.draw_vertical_line(
                frame_buffer, i, min_y, max_y - min_y + 1, colored)

    def draw_circle(self, frame_buffer, x, y, radius, colored):

        # Bresenham algorithm

        x_pos = -radius

        y_pos = 0

        err = 2 - 2 * radius

        if (x >= self.width or y >= self.height):

            return

        while True:

            self.set_pixel(frame_buffer, x - x_pos, y + y_pos, colored)

            self.set_pixel(frame_buffer, x + x_pos, y + y_pos, colored)

            self.set_pixel(frame_buffer, x + x_pos, y - y_pos, colored)

            self.set_pixel(frame_buffer, x - x_pos, y - y_pos, colored)

            e2 = err

            if (e2 <= y_pos):

                y_pos += 1

                err += y_pos * 2 + 1

                if(-x_pos == y_pos and e2 <= x_pos):

                    e2 = 0

            if (e2 > x_pos):

                x_pos += 1

                err += x_pos * 2 + 1

            if x_pos > 0:

                break

    def draw_filled_circle(self, frame_buffer, x, y, radius, colored):

        # Bresenham algorithm

        x_pos = -radius

        y_pos = 0

        err = 2 - 2 * radius

        if (x >= self.width or y >= self.height):

            return

        while True:

            self.set_pixel(frame_buffer, x - x_pos, y + y_pos, colored)

            self.set_pixel(frame_buffer, x + x_pos, y + y_pos, colored)

            self.set_pixel(frame_buffer, x + x_pos, y - y_pos, colored)

            self.set_pixel(frame_buffer, x - x_pos, y - y_pos, colored)

            self.draw_horizontal_line(
                frame_buffer, x + x_pos, y + y_pos, 2 * (-x_pos) + 1, colored)

            self.draw_horizontal_line(
                frame_buffer, x + x_pos, y - y_pos, 2 * (-x_pos) + 1, colored)

            e2 = err

            if (e2 <= y_pos):

                y_pos += 1

                err += y_pos * 2 + 1

                if(-x_pos == y_pos and e2 <= x_pos):

                    e2 = 0

            if (e2 > x_pos):

                x_pos += 1

                err += x_pos * 2 + 1

            if x_pos > 0:

                break

    # to wake call reset() or init()

    def sleep(self):

        self._command(VCOM_AND_DATA_INTERVAL_SETTING, b'\x37')

        self._command(VCM_DC_SETTING, b'\x00')  # to solve Vcom drop

        # gate switch to external
        self._command(POWER_SETTING, b'\x02\x00\x00\x00')

        self.wait_until_idle()

        self._command(POWER_OFF)

    def fill(self, buffer, value):
        for i in range(len(buffer)):
            buffer[i] = value

sck, miso, mosi, dc, cs, rst, busy = Pin(18), Pin(
    19), Pin(23), Pin(27), Pin(5), Pin(21), Pin(22)
spi = SPI(1, baudrate=4000000, polarity=0,
          phase=0, sck=sck, miso=miso, mosi=mosi)
e = EPD(spi, cs, dc, rst, busy)
e.init()

if __name__ == "__main__":

    import gc
    gc.collect()

    black_while = bytearray((104*212) // 8)
    red_while = bytearray((104*212) // 8)

    e._command(DATA_START_TRANSMISSION_1)
    utime.sleep_ms(2)

    e.fill(black_while, 0xFF)

    e.draw_circle(black_while, 30, 30, 25, True)

    e._data(black_while)  # 黑/白（00/FF）

    utime.sleep_ms(2)
    e._command(DATA_START_TRANSMISSION_2)
    utime.sleep_ms(2)

    e.fill(red_while, 0xFF)

    e._data(red_while)  # 红/白（00/FF）

    utime.sleep_ms(2)
    e._command(DISPLAY_REFRESH)
    e.wait_until_idle()

    print('tested 1')

    e._command(DATA_START_TRANSMISSION_1)
    utime.sleep_ms(2)

    e.fill(black_while, 0xFF)

    e.draw_circle(black_while, 30, 50, 30, True)

    e._data(black_while)  # 黑/白（00/FF）

    utime.sleep_ms(2)
    e._command(DATA_START_TRANSMISSION_2)
    utime.sleep_ms(2)

    e.fill(red_while, 0xFF)

    e._data(red_while)  # 红/白（00/FF）

    utime.sleep_ms(2)
    e._command(DISPLAY_REFRESH)
    e.wait_until_idle()

    print('tested 2')

    e._command(DATA_START_TRANSMISSION_1)
    utime.sleep_ms(2)

    e.fill(black_while, 0xFF)

    e._data(black_while)  # 黑/白（00/FF）

    utime.sleep_ms(2)
    e._command(DATA_START_TRANSMISSION_2)
    utime.sleep_ms(2)

    e.fill(red_while, 0xFF)

    e.draw_filled_circle(red_while, 50, 100, 40, True)

    e._data(red_while)  # 红/白（00/FF）

    utime.sleep_ms(2)
    e._command(DISPLAY_REFRESH)
    e.wait_until_idle()

    print('tested 3')
