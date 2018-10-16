import neopixel 
from machine import Pin, PWM
from random import randint 
import time
	
array = [262, 286, 311, 349, 392, 440, 494, 523, 587, 659, 698, 784, 880, 987, 1046, 1174, 1318, 1396, 1567, 1760, 1975]
	
while True:

	Pwm = PWM(Pin(25)) # create PWM object from a pin
	
	for value in array:

		Pwm.freq(value) # set frequency
		print('Pwm.freq ' + str(Pwm.freq())) # get current frequency

		Pwm.duty(randint(100, 200)) # set duty cycle
		print('Pwm.duty ' + str(Pwm.duty())) # get current duty cycle

	array.reverse()

	for value in array:

		Pwm.freq(value) # set frequency
		print('Pwm.freq ' + str(Pwm.freq())) # get current frequency
		
		Pwm.duty(randint(100, 200)) # set duty cycle
		print('Pwm.duty ' + str(Pwm.duty())) # get current duty cycle

	array.reverse()

	for value in array:

		Pwm.freq(value) # set frequency
		print('Pwm.freq ' + str(Pwm.freq())) # get current frequency

		Pwm.duty(randint(100, 200)) # set duty cycle
		print('Pwm.duty ' + str(Pwm.duty())) # get current duty cycle

		array.reverse()

	for value in array:
	
		Pwm.freq(value) # set frequency
		print('Pwm.freq ' + str(Pwm.freq())) # get current frequency

		Pwm.duty(randint(100, 200)) # set duty cycle
		print('Pwm.duty ' + str(Pwm.duty())) # get current duty cycle

		array.reverse()

	Pwm.deinit() # turn off PWM on the pin

	NeoPixelPower = Pin(2, Pin.OUT)
	NeoPixelPower.value(1)

	# Setup the Neopixel strip on pin0 with a length of 8 pixels
	np = neopixel.NeoPixel(Pin(4), 25)

	while True:

		value = 0
		for b in range(0, 51):
			np.fill((0, 0, value))
			np.write()
			time.sleep(0.005)
			value = value + 5
		value = 255
		for b in range(0, 51):
			np.fill((0, 0, value))
			np.write()
			time.sleep(0.005)
			value = value - 5

		value = 0
		for b in range(0, 51):
			np.fill((0, value, 0))
			np.write()
			time.sleep(0.005)
			value = value + 5
		value = 255
		for b in range(0, 51):
			np.fill((0, value, 0))
			np.write()
			time.sleep(0.005)
			value = value - 5

		value = 0
		for b in range(0, 51):
			np.fill((value, 0, 0))
			np.write()
			time.sleep(0.005)
			value = value + 5
		value = 255
		for b in range(0, 51):
			np.fill((value, 0, 0))
			np.write()
			time.sleep(0.005)
			value = value - 5

		value = 0
		for b in range(0, 51):
			np.fill((value, value, value))
			np.write()
			time.sleep(0.005)
			value = value + 5
		value = 255
		for b in range(0, 51):
			np.fill((value, value, value))
			np.write()
			time.sleep(0.005)
			value = value - 5