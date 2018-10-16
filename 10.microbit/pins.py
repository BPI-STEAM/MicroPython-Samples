from utime import sleep_ms as sleep
from machine import Pin, ADC, DAC

class Pins():

    def __init__(self, pin):
        self.pin = pin
        self.adc = None

    def write_digital(self, v):
        Pin(self.pin, Pin.OUT).value(v)

    def read_digital(self):
        return Pin(self.pin, Pin.IN).value()

    def read_analog(self, ATTN = ADC.ATTN_0DB):
        if self.pin in [25]:
            print("This pin feature is not supported")
            return 0
        if self.adc is None:
            self.adc = ADC(Pin(self.pin, Pin.IN))
            self.adc.atten(ATTN)  # 0-3.9V
        return self.adc.read()

    def write_analog(self, value):
        DAC(Pin(self.pin)).write(value)

    def is_touched(self):
        return self.read_analog() > 3071

def unit_test():
    print('The unit test code is as follows')
    print('\n\
        pin13 = Pins(18)\n\
        while True:\n\
            pin13.write_digital(1)\n\
            sleep(20)\n\
            pin13.write_digital(0)\n\
            sleep(480)\n\
            print(\'pin1(P1).is_touched()\', pin1.is_touched());\n\
    ')
    pin13 = Pins(18)
    pin1 = Pins(32)
    while True:
        pin13.write_digital(1)
        sleep(20)
        pin13.write_digital(0)
        sleep(480)
        print('pin1(P1).is_touched()', pin1.is_touched());

if __name__ == '__main__':
    unit_test()
