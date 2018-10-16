from machine import Pin
import machine
adc = machine.ADC(Pin(36)) #there are two sensors on the board:pin36 and pin39
LED = machine.PWM(machine.Pin(18), freq=50)
# using ADC (analog digital converter)

# led's intensity is controlled by the potentiometer's value

while True:
	# dividing by 16 since .read() gives a 12bit value
	# but .intensity() needs a 8bit value 
	# ensuring pot_value is an integer
	pot_value = int(adc.read()/4)
	pot_value=1024-pot_value
	LED.duty(pot_value)