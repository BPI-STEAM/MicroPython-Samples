from machine import Pin, I2C

# construct an I2C bus
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=100000)
while True:
	print(i2c.scan())