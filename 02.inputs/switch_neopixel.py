import machine
from neopixel import NeoPixel
from machine import Pin
#This configures a NeoPixel strip on GPIO4 with 25 pixels.
# You can adjust the “4” (pin number) and the “25” (number of pixel) to suit your set up.
sw = Pin(35, Pin.IN)
np = NeoPixel(machine.Pin(4), 25)
while True:
	while 0 == sw.value():
		np[0] = (255, 0, 0)               #set the colour of the first pixels
		np[1] = (255, 255, 255)             #set the colour of the second pixels
		np.write()                        # use the write() method to output the colours to the LEDs
	else:
		np[0] = (0, 0, 0)               #set the colour of the first pixels
		np[1] = (0, 0, 0)             #set the colour of the second pixels
		np.write()                        # use the write() method to output the colours to the LEDsS