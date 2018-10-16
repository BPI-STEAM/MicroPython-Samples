from machine import Pin
sw = Pin(35, Pin.IN)
# there is an red LED on the board
LED = Pin(18, Pin.OUT)# configuring 18 to Push/Pull output

# LED is on only when the  button is pressed down
while True:
	if sw.value() == True:
		LED.value(0)
	else:
		LED.value(1)