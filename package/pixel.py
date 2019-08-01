from machine import Pin
from neopixel import NeoPixel

def PixelPower(bool):
    Pin(2, Pin.OUT).value(bool)

class Pixel(NeoPixel):

    def __init__(self):
        self.Min, self.Max, self.Sum = 0, 5, 25
        NeoPixel.__init__(self, Pin(4), self.Sum, 3, 1)

    def LoadXY(self, X, Y, RGB, isSoftWare = True):
        if self.Min <= X and X < self.Max and self.Min <= Y and Y < self.Max:
            if isSoftWare: # SoftWare coordinate system
                self[int(Y) + ((self.Max - 1) - int(X)) * self.Max] = RGB # left and top is (0, 0)
            else: # Hardware coordinate system
                self[(int(X)) + int(Y) * self.Max] = RGB # right and top is (0, 0)
        else:
            pass
        # print('Pixel Load Over Limit')

    def LoadPos(self, Pos, RGB):
        if self.Min <= Pos and Pos < self.Sum:
            self[Pos] = RGB
        else:
            pass
        # print('Pixel Load Over Limit')

    def Show(self):
        self.write()

def unit_test():
    PixelPower(True)
    View = Pixel()

    View.LoadXY(0, 0, (10, 0, 0))
    View.LoadXY(0, 4, (0, 10, 0))
    View.LoadXY(4, 0, (0, 0, 10))
    View.LoadXY(4, 4, (10, 10, 10))
    View.Show()

    # default SoftWare coordinate system

