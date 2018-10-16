from utime import time, sleep_ms as sleep

class Button:

    def __init__(self, pin):
        from machine import Pin
        self.pin = Pin(pin, Pin.IN)

    def get_presses(self, delay = 1):
        last_time, last_state, presses = time(), 0, 0
        while time() < last_time + delay:
            sleep(50)
            if last_state == 0 and self.pin.value() == 1:
                last_state= 1
            if last_state == 1 and self.pin.value() == 0:
                last_state, presses = 0, presses + 1
        return presses

    def is_pressed(self):
        return self.pin.value() == 0

    def was_pressed(self, delay = 1):
        last_time, last_state = time(), self.pin.value()
        while time() < last_time + delay:
            sleep(50)
            if last_state != self.pin.value():
                return True
        return False

def unit_test():
    print('The unit test code is as follows')
    print('\n\
        button_a = Button(35)\n\
        while True:\n\
            print(\'button_a was_pressed \', button_a.was_pressed())\n\
            print(\'button_a is_pressed \', button_a.is_pressed())\n\
            print(\'button_a get_presses \', button_a.get_presses())\n\
        ')
    button_a = Button(35)
    while True:
        print('button_a was_pressed ', button_a.was_pressed())
        print('button_a is_pressed ', button_a.is_pressed())
        print('button_a get_presses ', button_a.get_presses())

if __name__ == '__main__':
    unit_test()
