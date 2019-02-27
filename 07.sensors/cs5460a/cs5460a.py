from machine import Pin, SPI

from micropython import const

CS5460A_RMS_VOLTAGE = const(0x18)

CS5460A_RMS_CURRENT = const(0x16)

CS5460A_TRUE_POWER = const(0x14)

CS5460A_CFG_READ = const(0x00)  # //reg read: config

CS5460A_CFG_READ_IGN = const(0x04)  # //reg read: Ign

CS5460A_CFG_READ_VGN = const(0x08)  # //reg read: Vgn

CS5460A_CFG_READ_CYCLE = const(0x0a)  # //reg read: cycle count

CS5460A_CFG_POWER_UP = const(0xa0)  # // power-up/halt

CS5460A_CFG_GAIN = const(0x40)  # // reg write: config. PGA Gain 10x, IHPF=1, VHPF=1

CS5460A_CFG_GAIN1 = const(0x01)

CS5460A_CFG_GAIN2 = const(0x00)

CS5460A_CFG_GAIN3 = const(0x61)

CS5460A_CFG_IGN= const(0x44)  # // reg write: Ign [current chan gain].

CS5460A_CFG_IGN1 = const(0x40)

CS5460A_CFG_IGN2 = const(0x00)

CS5460A_CFG_IGN3 = const(0x00)

CS5460A_CFG_VGN = const(0x48)  # reg write: Vgn [voltage chan gain]

CS5460A_CFG_VGN1 = const(0x41)

CS5460A_CFG_VGN2 = const(0xA0)

CS5460A_CFG_VGN3 = const(0xEA)

CS5460A_START_CONV = const(0xe8) #command : start convert


class cs5460a(object):
    import utime
    def __init__(self, spi, cs=2, rst=4):
        self.spi = spi
        self.cs = Pin(cs, Pin.OUT)
        self.rst = Pin(rst, Pin.OUT)
        self.FLOAT24 = 16777216.0  # 2^24
        self.VOLTAGE_MULTIPLIER = (1 / self.FLOAT24 * 367)
        self.CURRENT_MULTIPLIER = (1 / self.FLOAT24 * 11.66)
        self.POWER_MULTIPLIER = (1 / self.FLOAT24 * 1.024 * 367 * 11.66 * 2)

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

    def cs5460a_setup(self):
        self.rst.value(0)
        utime.sleep_ms(50)
        self.rst.value(1)  # reset the  cs5460a

        self.cs.value(0)
        self.spi.write(bytearray([CS5460A_CFG_POWER_UP]))
        self.cs.value(1)  # the command of the power_up

        self.write(CS5460A_CFG_GAIN, bytearray([CS5460A_CFG_GAIN1, CS5460A_CFG_GAIN2, CS5460A_CFG_GAIN3]))  # set
        self.write(CS5460A_CFG_VGN , bytearray([CS5460A_CFG_VGN1, CS5460A_CFG_VGN2, CS5460A_CFG_VGN3]))#V
        self.write(CS5460A_CFG_IGN, bytearray([CS5460A_CFG_IGN1, CS5460A_CFG_IGN2, CS5460A_CFG_IGN3]))#A

        self.cs.value(0)
        self.spi.write(bytearray([CS5460A_START_CONV]))
        self.cs.value(1)  # start to convert

    def _conv(self, true_power):
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

    def read_u(self):
        voltage = self.read(CS5460A_RMS_VOLTAGE)
        temp = (voltage[2] + voltage[1] * 256 + voltage[0] * 65536)
        V = self.VOLTAGE_MULTIPLIER * temp
        return V

    def read_i(self):
        current = self.read(CS5460A_RMS_CURRENT)
        temp = (current[2] + current[1] * 256 + current[0] * 65536)
        A = self.CURRENT_MULTIPLIER * temp
        return A

    def read_p(self):
        true_power = self.read(CS5460A_TRUE_POWER)
        temp = self._conv(true_power)
        P = self.POWER_MULTIPLIER * temp
        return P


from machine import Pin
import utime

p = Pin(18, Pin.OUT)
p.value(1)


def unit_test():
    vspi = SPI(-1, sck=Pin(5), mosi=Pin(23), miso=Pin(19), baudrate=2000000)  # -1 software spi
    ts = cs5460a(vspi)
    ts.cs5460a_setup()  # 初始化

    while True:
        utime.sleep_ms(1000)
        k = ts.read(0x1e)
        # print(k)
        # current=ts.read(0x16)
        # temp = (current[2] + current[1] * 256 + current[0] * 65536)/16777216
        # print(temp)
        V = ts.read_u()
        A = ts.read_i()
        P = ts.read_p()
        print('current=%.2f A' % A)
        print('voltage=%.2f V' % V)
        print('ture_power=%.2f W' % P)


if __name__ == '__main__':
    unit_test()
