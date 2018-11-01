import utime
from machine import I2C, Pin
from mpu9250 import MPU9250
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=200000)
sensor = MPU9250(i2c)
print("MPU9250 id: " + hex(sensor.whoami))
while True:
	print('acceleration:', str(sensor.acceleration))
	print('gyro:', str(sensor.gyro))
	print('magnetic:', str(sensor.magnetic))
	