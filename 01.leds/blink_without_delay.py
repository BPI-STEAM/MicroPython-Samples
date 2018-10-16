from machine import Pin
import time
LED = Pin(18, Pin.OUT)

prev_millis = 0
interval = 1000

def toggle(LED):
	LED.value(not LED.value())

while True:
	curr_millis = time.ticks_ms()
	if curr_millis - prev_millis > interval:
		prev_millis = curr_millis
		toggle(LED)
