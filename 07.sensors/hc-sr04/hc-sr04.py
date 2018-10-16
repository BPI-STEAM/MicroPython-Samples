from machine import Pin
import time
trigPin = Pin(15, Pin.OUT)
echoPin = Pin(16, Pin.IN)
trigPin.value(0)
echoPin.value(0)
def checkdist():
	trigPin.value(0)
	time.sleep(0.002)
	trigPin.value(1)
	time.sleep(0.01)
	trigPin.value(0)
	while(echoPin.value()==0):
		pass
	t1=time.ticks_us()
	while(echoPin.value()==1):
		pass
	t2=time.ticks_us()
	t3=time.ticks_diff(t2,t1)/10000
	return t3*340/2
while True:
		print("Distance:%0.2f cm" %checkdist())
		time.sleep(0.5)