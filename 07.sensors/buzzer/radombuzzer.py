import machine
import time , os
from random import *
#p16 = machine.Pin(16)
#pwm16 = machine.PWM(p16)
a = 25
buzzer = machine.PWM(machine.Pin(25), duty=512)
while True:
	i = randint(25, 7812)         #generates a random number form 25 to 7812
            #set buzzer's tone immediately to random_tone
	buzzer.freq(i)
	time.sleep(0.1)              # wait half a second
	print(buzzer.freq() )         #prints the buzzer's current tone