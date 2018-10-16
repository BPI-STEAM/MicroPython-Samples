
from machine import Pin, SPI, reset
from tft import TFT_GREEN
# DC       - RS/DC data/command flag
# CS       - Chip Select, enable communication
# RST/RES  - Reset
dc  = Pin(5, Pin.OUT)
cs  = Pin(2, Pin.OUT)
rst = Pin(15, Pin.OUT)

# SPI Bus (CLK/MOSI/MISO)
# check your port docs to see which Pins you can use
spi = SPI(1, baudrate=60000000, polarity=1, phase=0, sck=Pin(14), mosi=Pin(13), miso=Pin(12))

# TFT object, this is ST7735R green tab version
tft = TFT_GREEN(128, 160, spi, dc, cs, rst)
tft.init()
while Thread[0]:
# start using the driver
	tft.clear(tft.rgbcolor(0, 0, 0))
	print(111)
	tft.pixel(0,0,tft.rgbcolor(0, 155, 255))
