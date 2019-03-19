from machine import Pin, PWM

import time

class Motor:

    speed_1, speed_2 = 400, 400

    left_1, left_2, right_1, right_2 = Pin(15, Pin.OUT), Pin(12, Pin.OUT), Pin(14, Pin.OUT), Pin(25, Pin.OUT) # 4 6 7 8
    left_pwm, right_pwm = PWM(Pin(13), freq=256), PWM(Pin(26), freq=256) # 5 9

    def start(self):
        Motor.left_pwm.duty(Motor.speed_1)
        Motor.right_pwm.duty(Motor.speed_2)

    def stop(self):
        Motor.left_1.value(0)
        Motor.left_2.value(0)
        Motor.right_1.value(0)
        Motor.right_2.value(0)

    def next(self):
        Motor.left_1.value(0)
        Motor.left_2.value(1)
        Motor.right_1.value(0)
        Motor.right_2.value(1)

    def back(self):
        Motor.left_1.value(1)
        Motor.left_2.value(0)
        Motor.right_1.value(1)
        Motor.right_2.value(0)

    def left(self):
        Motor.left_1.value(0)
        Motor.left_2.value(1)
        Motor.right_1.value(1)
        Motor.right_2.value(0)

    def right(self):
        Motor.left_1.value(1)
        Motor.left_2.value(0)
        Motor.right_1.value(0)
        Motor.right_2.value(1)

tmp = Motor()
tmp.start()
tmp.next()
time.sleep(2)
tmp.left()
time.sleep(2)
tmp.right()
time.sleep(2)
tmp.back()
