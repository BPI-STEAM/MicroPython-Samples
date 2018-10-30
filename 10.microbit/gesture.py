
class gesture():
    from machine import ADC, Pin
    from light import LightIntensity
    from time import sleep_ms
    def __init__(self):
        self.LightL = LightIntensity(36)
        self.LightR = LightIntensity(39)
        self.idle = 0
        self.running = 1
        self.finish = 2
        self.left=0
        self.right=0

    def get_brightness(self):
        self.right_last = self.right_new
        self.right_new = self.LightR.read()
        self.left_last = self.left_new
        self.left_new = self.LightL.read()
       
    def set_threshold(self):  # 设置阈值
        self.threshold = self.right_last*0.1

    def is_rightorleft(self,dir):
        self.right=0
        self.left=0
        self.right_new = self.right_last = self.LightR.read()
        self.left_new = self.left_last = self.LightL.read()
        status = 0
        
        while True:
            if status == self.idle:
                count = 0
                self.get_brightness()
                self.set_threshold()
                print('right_new=%d' % self.right_new)
                sleep_ms(20)
                if dir:
                    if self.right_last-self.right_new > self.threshold and self.left_new-self.right_new > self.threshold:
                        status = self.running
                else:
                    if self.left_last-self.left_new > self.threshold and self.right_new-self.left_new > self.threshold:
                        status = self.running
            elif status == self.running:
                self.get_brightness()
                print('left_new=%d' % self.left_new)
                sleep_ms(20)
                count += 1
                if count > 10:
                    status = self.idle
                if dir:
                    if self.left_last-self.left_new > self.threshold:
                        status = self.finish
                else:
                    if self.right_last-self.right_new > self.threshold:
                        status = self.finish
            elif status == self.finish:
               return True

    def direction():
        return True


def unit_test():
    print('\n\
        from machine import Pin\n\
        t=gesture()\n\
        LED = Pin(18, Pin.OUT)\n\
        LED.value(0)\n\
        if(t.is_rightorleft(0)):\n\
            LED.value(1)\n\
    ')
    from machine import Pin
    t=gesture()
    LED = Pin(18, Pin.OUT)
    LED.value(0)
    if(t.is_rightorleft(0)):
        LED.value(1)

if __name__ == '__main__':
    unit_test()
