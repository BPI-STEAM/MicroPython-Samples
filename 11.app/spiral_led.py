import utime
from random import randint
from display import Pixel, PixelPower
PixelPower(True)
View = Pixel()

RGB = (0, 0, 0)

def Draw(x, y):
	View.LoadXY(x, y, RGB)
	View.Show()
	utime.sleep_ms(1)




r, g, b, br = 1, 1, 1, 1

while True:
	RGB = (r * br, g * br, b * br)
	print('RGB:' + str(RGB))
	
	br = br + 5
	
	if br > 20:
		br = 1
		r, g, b = randint(0, 2), randint(0, 2), randint(0, 2)
		
	x, y = 2, 2
	
	r, u, l, d = 1, 1, 2, 2

	while r < 6:
	
		Draw(x, y)
		
		end = x + r
		while x < end:
			x = x + 1
			Draw(x, y)
		r = r + 2
		
		end = y + u
		while y < end:
			y = y + 1
			Draw(x, y)
		u = u + 2
			
		end = x - l
		while x > end:
			x = x - 1
			Draw(x, y)
		l = l + 2
		
		end = y - d
		while y > end:
			y = y - 1
			Draw(x, y)
		d = d + 2

