import machine,time
from random import *
a = 25
#p16 = machine.Pin(16)
#pwm16 = machine.PWM(p16)
servo = machine.PWM(machine.Pin(16), freq=50)
while True:
	i = randint(25, 125)         #generates a random number form 25 to 125
	servo.duty(i)                #set servo's position immediately to random_angle
	time.sleep(0.5)              # wait half a second
	print(servo.duty() )         #prints the servo's current position