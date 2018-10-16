from display import Pixel, PixelPower
PixelPower(True)
View = Pixel()

RGB = (10, 10, 10)
View.LoadXY(1, 1, RGB)
View.LoadPos(24, RGB)
View.Show()
