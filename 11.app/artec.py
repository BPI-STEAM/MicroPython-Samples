import machine
import time

import button

button_a = button.Button(15)
button_b = button.Button(27)

import music

music.play(music.POWER_UP)

import pins

led1 = pins.Pins(12)
led2 = pins.Pins(14)

led1.write_digital(1)
led2.write_digital(1)

import display

Image = display.Image
display = display.Display()

display.clear()

all_boats = [
    Image("00000:" "00000:" "00000:" "00000:" "00000"),
    Image("11111:" "00000:" "00000:" "00000:" "00000"),
    Image("11111:" "11111:" "00000:" "00000:" "00000"),
    Image("11111:" "11111:" "11111:" "00000:" "00000"),
    Image("11111:" "11111:" "11111:" "11111:" "00000"),
    Image("11111:" "11111:" "11111:" "11111:" "11111"),
    Image("00000:" "11111:" "11111:" "11111:" "11111"),
    Image("00000:" "00000:" "11111:" "11111:" "11111"),
    Image("00000:" "00000:" "00000:" "11111:" "11111"),
    Image("00000:" "00000:" "00000:" "00000:" "11111"),
    Image("00000:" "00000:" "00000:" "00000:" "00000"),
]

display.show(all_boats, color=(10, 10, 10), delay=150)

led1.write_digital(0)
led2.write_digital(0)

music.play(music.JUMP_UP)
display.show('A', color=(20, 0, 0))
while 0 == button_a.was_pressed():
    time.sleep(0.1)
time.sleep(0.5)
display.show('O', color=(0, 20, 0))

music.play(music.JUMP_UP)
display.show('B', color=(20, 0, 0))
while 0 == button_b.was_pressed():
    time.sleep(0.1)
time.sleep(0.5)
display.show('O', color=(0, 20, 0))

music.play(music.JUMP_UP)
display.show('T', color=(20, 0, 0))
import temperature
__adc = machine.ADC(machine.Pin(35, machine.Pin.IN))
__adc.atten(machine.ADC.ATTN_11DB)
temperature = temperature.Temperature(__adc).temperature

time.sleep(1)
while temperature() < 10:
    time.sleep(1)
display.show('O', color=(0, 20, 0))

music.play(music.JUMP_UP)
display.show('9', color=(20, 0, 0))
__i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=200000)
while True:
    __dev = __i2c.scan()
    if len(__dev) > 0:
        buf = bytearray(1)
        while buf[0] != 234:
            __i2c.readfrom_mem_into(__dev[0], 0, buf)
            time.sleep(1)
            # print(buf[0])
        break
display.show('O', color=(0, 20, 0))

music.play(music.JUMP_UP)
display.show('L', color=(20, 0, 0))
time.sleep(0.5)
import light
lt = light.Intensity(34)
while True:
    last = lt.read()
    time.sleep(1)
    now = lt.read()
    if abs(now - last) > 100:
        break
display.show('O', color=(0, 20, 0))

music.play(music.POWER_DOWN)
time.sleep(0.5)
display.clear()