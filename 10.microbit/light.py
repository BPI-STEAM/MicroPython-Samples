from time import sleep_ms


class Intensity():
    dither = 5

    def __init__(self, pin):
        self.old, self.new, self.eliminate = 0, 0, 0

        from machine import ADC, Pin
        self.adc = ADC(Pin(pin, Pin.IN))
        self.adc.atten(ADC.ATTN_11DB) # 0-3.9V

    def read(self):
        self.old = self.new
        self.new = self.adc.read()
        return int(self.new / 4.095)

    # result > 0 to state up, < 0 to state down.
    def get_state(self):
        # print(self.new, self.old)
        tmp = self.new - self.old
        return 0 if abs(tmp) < self.eliminate else tmp

    def calibrate(self):
        self.eliminate = self.read() / Intensity.dither

class Gesture(object):
    idle, ing, end, = 0, 1, 2

    def __init__(self, PinLeft=36, PinRight=39, dither=5):
        Intensity.dither = dither
        self.l, self.r = Intensity(PinLeft), Intensity(PinRight)
        self.l_state, self.r_state = Gesture.idle, Gesture.idle

    def get_brightness(self):
        self.r.read()
        self.l.read()

    def get_gesture(self, delay=30):
        sleep_ms(delay)
        self.get_brightness()
        l_state, r_state = self.l.get_state(), self.r.get_state()
        result = []

        if l_state < 0 and r_state < 0:
            self.l_state, self.r_state = Gesture.ing,  Gesture.ing

        if self.l_state == Gesture.ing and l_state == 0 and r_state < 0:
                self.l_state = Gesture.end

        if self.l_state == Gesture.end and l_state > 0 and r_state == 0:
            self.l_state = Gesture.idle
            result.append('left')

        if self.r_state == Gesture.ing and l_state < 0 and r_state == 0:
            self.r_state = Gesture.end

        if self.r_state == Gesture.end and  l_state == 0 and r_state > 0:
            self.r_state = Gesture.idle
            result.append('right')

        if l_state == 0 and r_state == 0:
            self.l_state = self.r_state = Gesture.idle
            self.l.calibrate()
            self.r.calibrate()

        return None if len(result) != 1 else result[0]

def unit_test():
    print('\n\
        g = Gesture()\n\
        while True:\n\
            res = g.get_gesture()\n\
            if res != None:\n\
                print(res)\n\
    ')
    g = Gesture()
    while True:
        res = g.get_gesture()
        if res != None:
            print(res)

if __name__ == '__main__':
    unit_test()
