from time import sleep_ms

class Sensegesture():
    idle = 0
    running = 1
    finish = 2

    def __init__(self, leftPin=36, rightpin=39):
        from light1 import LightIntensity
        self.LightL = LightIntensity(leftPin)
        self.LightR = LightIntensity(rightpin)

    def get_brightness(self):
        self.LightR.read()
        self.LightL.read()

    def set_threshold(self, val):  # 设置阈值
        self.threshold = self.LightR.new_val*val

    def is_right(self, runtime=10, interval=0.5):
        status = 0
        self.get_brightness()
        self.set_threshold(0.1)
        for t in range(runtime*40):
            if status == Sensegesture.idle:
                count = 0
                self.get_brightness()
                # print(self.threshold)
                # print('right_new=%d' % self.LightR.new_val)
                sleep_ms(20)
                if self.LightL.last_val-self.LightL.new_val > self.threshold and self.LightR.new_val-self.LightL.new_val > self.threshold:
                    status = self.running
            elif status == Sensegesture.running:
                self.get_brightness()
                # print(self.threshold)
                # print(self.LightL.last_val)
                # print('left_new=%d' % self.LightL.new_val)
                sleep_ms(20)
                count += 1
                if count > interval*40:
                    status = Sensegesture.idle
                if self.LightR.last_val-self.LightR.new_val > self.threshold:
                    status = self.finish
            elif status == Sensegesture.finish:
                return True
        return False

    def is_left(self, runtime=10, interval=0.5):
        status = 0
        self.get_brightness()
        self.set_threshold(0.1)
        for t in range(runtime*40):
            if status == Sensegesture.idle:
                count = 0
                self.get_brightness()
                # print('right_new=%d' % self.LightR.new_val)
                sleep_ms(20)
                if self.LightR.last_val-self.LightR.new_val > self.threshold and self.LightL.new_val-self.LightR.new_val > self.threshold:
                    status = Sensegesture.running
            elif status == Sensegesture.running:
                self.get_brightness()
                # print(self.threshold)
                # print(self.LightL.last_val)
                # print('left_new=%d' % self.LightL.new_val)
                sleep_ms(20)
                count += 1
                if count > interval*40:
                    status = Sensegesture.idle
                if self.LightL.last_val-self.LightL.new_val > self.threshold:
                    status = Sensegesture.finish

            elif status == Sensegesture.finish:
                return True
        return False

    def direction(self):
        return True


def unit_test():
    print('\n\
        from machine import Pin\n\
        t = Sensegesture()\n\
        LED = Pin(18, Pin.OUT)\n\
        LED.value(0)\n\
        if(t.is_right(runtime=15)):\n\
            LED.value(1)\n\
    ')
    from machine import Pin
    t = Sensegesture()
    LED = Pin(18, Pin.OUT)
    LED.value(0)
    if(t.is_right(runtime=15)):
        LED.value(1)


if __name__ == '__main__':
    unit_test()
