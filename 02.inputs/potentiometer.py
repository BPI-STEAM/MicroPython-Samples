from machine import Pin
import machine
adc = machine.ADC(Pin(33))
# using ADC (analog digital converter)
LED = machine.PWM(machine.Pin(18), freq=1000)


# led's intensity is controlled by the Pin18's value

while True:
	# dividing by 4 since .read() is from 0 to 4095
	# but .intensity() is from 0 to 1024
	# ensuring pot_value is an integer
	pot_value = int(adc.read()/4)
	LED.duty(pot_value)
	print(adc.read())