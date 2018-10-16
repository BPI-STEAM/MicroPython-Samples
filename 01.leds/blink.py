from machine import Pin
import time
LED = Pin(18, Pin.OUT)
while True:
	time.sleep(0.2) # Set 0.2s Python execute time.
	LED.value(1)
	time.sleep(0.2) # Set 0.2s Python execute time.
	LED.value(0)