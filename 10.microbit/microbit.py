import machine

from utime import ticks_ms as running_time, sleep_ms as sleep

from pins import Pins
pin0 = Pins(25)
pin1 = Pins(32)
pin2 = Pins(33)
pin3 = Pins(13)
pin4 = Pins(16)
pin5 = Pins(35)
pin6 = Pins(12)
pin7 = Pins(14)
pin8 = Pins(16)
pin9 = Pins(17)
pin10 = Pins(26)
pin11 = Pins(27)
pin12 = Pins(2)
pin13 = Pins(18)
pin14 = Pins(19)
pin15 = Pins(23)
pin16 = Pins(5)
pin19 = Pins(22)
pin20 = Pins(21)

from display import Display, Image
display = Display()

from button import Button
button_a = Button(35)
button_b = Button(27)

from temperature import Temperature
__adc = machine.ADC(machine.Pin(34, machine.Pin.IN))
__adc.atten(machine.ADC.ATTN_11DB)  # 0-3.9V
__temp = Temperature(__adc)
temperature = __temp.temperature

from mpu9250 import MPU9250
__sensor = MPU9250(machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=200000))
# print("MPU9250 Read whoami: " + hex(__sensor.whoami))

from compass import Compass
compass = Compass(__sensor)

from accelerometer import Accelerometer
accelerometer = Accelerometer(__sensor)
