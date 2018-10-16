import machine
import time , os
#p16 = machine.Pin(16)
#pwm16 = machine.PWM(p16)
a = 25
servo = machine.PWM(machine.Pin(16), freq=50)
while True:
	for i in range(25,125):
		servo.duty(i)
		time.sleep(0.02)
		print(i)