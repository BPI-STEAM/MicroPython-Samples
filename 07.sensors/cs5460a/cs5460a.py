from machine import Pin, SPI
import utime

class cs5460a(object):
    def __init__(self, spi, cs=4, rst=2):
        self.spi = spi
        self.cs = Pin(cs, Pin.OUT)
        self.rst = Pin(rst, Pin.OUT)
        self.FLOAT24 = 16777216.0  # 2^24
        self.VOLTAGE_MULTIPLIER = (1 / self.FLOAT24 * 385)
        self.CURRENT_MULTIPLIER = (1 / self.FLOAT24 * 11.66)
        self.POWER_MULTIPLIER = (1 / self.FLOAT24 * 1.024 * 385 * 11.66 * 2)

    def read(self, addr):
        b = bytearray([0xfe, 0xfe, 0xfe])
        buf = bytearray(3)
        self.cs.value(0)
        self.spi.write(bytearray([addr]))
        self.spi.write_readinto(b, buf)
        self.cs.value(1)
        # print(buf[0],buf[1],buf[2])
        return buf

    def write(self, addr, data):
        self.cs.value(0)
        self.spi.write(bytearray([addr]))
        self.spi.write(data)
        self.cs.value(1)
        # print('write_ok')

    def cs5460a_init(self):
        self.rst.value(0)
        utime.sleep_ms(50)
        self.rst.value(1)  # reset the  cs5460a

        self.cs.value(0)
        self.spi.write(bytearray([0xa0]))
        self.cs.value(1)  # the command of the power_up

        self.write(0x40, bytearray([0x00, 0x00, 0x61]))  # set
        self.write(0x48, bytearray([0x46, 0xfa, 0xcb]))
        self.write(0x44, bytearray([0x42, 0x66, 0xb4]))

        self.cs.value(0)
        self.spi.write(bytearray([0xe8]))
        self.cs.value(1)  # start to convert

    def conv(self, true_power):
        if true_power[0] > 0x80:
            a = bytearray([~true_power[0]])
            a[0] &= 0x7f
            # print(a)
            b = bytearray([~true_power[1]])
            # print(b)
            c = bytearray([~true_power[2]])
            # print(c)
            temp = ((c[0] + b[0] * 256 + a[0] * 65536) + 1)
        else:
            temp = ((true_power[0] + true_power[0] * 256 + true_power[0] * 65536) + 1)
        return temp


def unit_test():
    vspi = SPI(-1, sck=Pin(18), mosi=Pin(23), miso=Pin(19), baudrate=2000000)  # -1 software spi
    ts = cs5460a(vspi)
    ts.cs5460a_init()  # 初始化

    while True:
        utime.sleep_ms(1000)
        k = ts.read(0x1e)
        print(k)
        voltage = ts.read(0x18)
        current = ts.read(0x16)
        true_power = ts.read(0x14)
        temp1 = (current[2] + current[1] * 256 + current[0] * 65536)
        temp2 = (voltage[2] + voltage[1] * 256 + voltage[0] * 65536)
        t = ts.conv(true_power)
        A = ts.CURRENT_MULTIPLIER * temp1
        V = ts.VOLTAGE_MULTIPLIER * temp2
        P = ts.POWER_MULTIPLIER * t
        print('current=%.2f A' % A)
        print('voltage=%.2f V' % V)
        print('ture_power=%.2f W' % P)


if __name__ == '__main__':
    unit_test()