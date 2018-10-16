import machine,time
LED = machine.PWM(machine.Pin(18), freq=1000)
brightness = 0
fade_amount = 5
while True:
	LED.duty(brightness)
	brightness += fade_amount
	time.sleep(0.01) 
	if brightness >  255 or brightness < 0:
		fade_amount *= -1