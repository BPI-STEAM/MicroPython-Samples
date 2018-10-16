
class Accelerometer:

    def __init__(self, sensor):
        self.sensor = sensor

    def get_x(self):
        return self.sensor.acceleration[0] * 5

    def get_y(self):
        return self.sensor.acceleration[1] * 5

    def get_z(self):
        return self.sensor.acceleration[2] * 5

    def get_values(self):
        return self.sensor.acceleration


def unit_test():
    print("\n\
    ")
    from display import Display
    display = Display()
    from machine import Pin, I2C
    from mpu9250 import MPU9250
    from time import sleep
    i2c = I2C(scl=Pin(22), sda=Pin(21), freq=200000)
    sensor = MPU9250(i2c)
    print('MPU9250 whoami: ' + hex(sensor.whoami))
    accelerometer = Accelerometer(sensor)
    while True:
        sleep(0.1)
        reading = accelerometer.get_x()
        print(reading)
        print(accelerometer.get_values())
        if reading > 20:
            display.show("R")
        elif reading < -20:
            display.show("L")
        else:
            display.show("-")

if __name__ == '__main__':
    unit_test()