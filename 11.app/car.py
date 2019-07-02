"""
The MIT License (MIT)
Copyright © 2019    @Lyubiao
"""

"""
bpi-car
position                               |\\\\\\| in_a | in_b |
          -+-----------------+-        +--------------------+
         | + |     前      | + |       | 左前 |  12  |  13  |
         | + |             | + |       +--------------------+
           |                 |         | 右前 |  15  |  14  |
           +-----------------+         +--------------------+
           |                 |         | 左后 |   8  |   9  |
         | + |     后      | + |       +--------------------+
         | + |             | + |       | 右后 |  10  |  11  |
           +-----------------+         +--------------------+
"""




import pca9685
from ucollections import deque
class bpicar(pca9685.PCA9685):
    def __init__(self, i2c, address=0x40):
        pca9685.PCA9685.__init__(self, i2c, address)
        self.freq(1000)
        self.data_cache = ()
        self.DataCache = deque(self.data_cache, 10)
        self.left_value = 0
        self.right_value = 0
        self.front_after = 0
        self.left_right = 0

    def _run(self, in_a, in_b, speed, invert=False):
        if invert == False:
            self.duty(in_a, speed)
            self.duty(in_b, 0)

        if invert == True:
            self.duty(in_b, speed)
            self.duty(in_a, 0)

    def forward(self, speed):

        self._run(15, 14, speed)
        self._run(12, 13, speed, True)
        self._run(10, 11, speed)
        self._run(8, 9, speed, True)

    def backward(self, speed):
        self._run(15, 14, speed, True)
        self._run(12, 13, speed)
        self._run(10, 11, speed, True)
        self._run(8, 9, speed)

    def turn_left(self, speed):

        self._run(15, 14, speed)
        self._run(12, 13, speed)
        self._run(10, 11, speed)
        self._run(8, 9, speed)

    def turn_right(self, speed):
        self._run(15, 14, speed, True)
        self._run(12, 13, speed, True)
        self._run(10, 11, speed, True)
        self._run(8, 9, speed, True)

    def stop(self):
        self._run(14, 15, 0)
        self._run(12, 13, 0)
        self._run(10, 11, 0)
        self._run(8, 9, 0)

    def car_test(self):
        import utime
        while True:
            if len(self.DataCache):
                print('f', len(self.DataCache))
                temp = self.DataCache.popleft()
                print('a', len(self.DataCache))
                if temp == 'N':
                    self.front_after += 1
                    if self.front_after > 4:
                        self.front_after = 4
                    if self.front_after == 0:
                        self.left_right = 0
                    print('self.front_after=', self.front_after)
                    print('self.left_right=', self.left_right)

                if temp == 'S':
                    self.front_after -= 1
                    if self.front_after < -4:
                        self.front_after = -4
                    if self.front_after == 0:
                        self.left_right = 0
                    print('self.front_after=', self.front_after)
                    print('self.left_right=', self.left_right)

                if temp == 'E':
                    self.left_right += 1
                    if self.left_right > 4:
                        self.left_right = 4
                    print('self.front_after=', self.front_after)
                    print('self.left_right=', self.left_right)

                if temp == 'W':
                    self.left_right -= 1
                    if self.left_right < -4:
                        self.left_right = -4
                    if self.front_after == 0:
                        self.left_right = 0
                    print('self.front_after=', self.front_after)
                    print('self.left_right=', self.left_right)

                speed = 1000 * abs(self.front_after)
                if self.front_after >= 0:
                    if self.left_right <= 0:
                        self._run(15, 14, speed)
                        self._run(10, 11, speed)
                        self._run(12, 13, int(
                            speed*(8-abs(self.left_right))/8), True)
                        self._run(
                            8, 9, int(speed*(8-abs(self.left_right))/8), True)
                    if self.left_right > 0:
                        self._run(15, 14, int(
                            speed*(8-abs(self.left_right))/8))
                        self._run(10, 11, int(
                            speed*(8-abs(self.left_right))/8))
                        self._run(12, 13, speed, True)
                        self._run(8, 9, speed, True)
                if self.front_after < 0:
                    if self.left_right <= 0:
                        self._run(15, 14, speed, True)
                        self._run(10, 11, speed, True)
                        self._run(12, 13, int(
                            speed*(8-abs(self.left_right))/8))
                        self._run(8, 9,   int(
                            speed*(8-abs(self.left_right))/8))
                    if self.left_right > 0:
                        self._run(15, 14, int(
                            speed*(8-abs(self.left_right))/8), True)
                        self._run(10, 11, int(
                            speed*(8-abs(self.left_right))/8), True)
                        self._run(12, 13, speed)
                        self._run(8, 9, speed)
                print(speed)
                print(int(speed*(8-abs(self.left_right))/8))
            utime.sleep_ms(20)


def unit_test():
    from machine import Pin, I2C
    i2c = I2C(scl=Pin(22), sda=Pin(21), freq=10000)
    car = bpicar(i2c)
    import utime
    import _thread
    _thread.start_new_thread(car.car_test, ())

    car.forward(4095)
    utime.sleep(5)
    car.backward(4095)
    utime.sleep(5)
    car.turn_left(4095)
    utime.sleep(5)
    car.turn_right(4095)
    utime.sleep(5)
    car.stop()
    utime.sleep(5)
    car.DataCache.append('N')
    car.DataCache.append('N')
    car.DataCache.append('N')
    car.DataCache.append('N')
    utime.sleep(10)
    car.DataCache.append('E')
    car.DataCache.append('E')
    utime.sleep(10)
    car.DataCache.append('S')
    car.DataCache.append('S')
    car.DataCache.append('S')
    car.DataCache.append('S')
    car.DataCache.append('S')
    car.DataCache.append('S')
    car.DataCache.append('S')
    car.DataCache.append('S')

    utime.sleep(10)
    car.stop()


if __name__ == '__main__':
    unit_test()
