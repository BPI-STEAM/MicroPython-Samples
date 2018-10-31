
class LightIntensity():
    def __init__(self, pin):
        from machine import ADC, Pin
        self.adc = ADC(Pin(pin, Pin.IN))
        self.adc.atten(ADC.ATTN_11DB) # 0-3.9V
    def read(self):
        self.last_val=self.new_val
        self.new_val = self.adc.read()/5
        return int(self.new_val*5/40.95)

def unit_test():
    print('\n\
        from time import sleep\n\
        LightL = LightIntensity(36)\n\
        LightR = LightIntensity(39)\n\
        while True:\n\
            print("LightL", LightL.read())\n\
            print("LightR", LightR.read())\n\
            sleep(0.5)\n\
    ')
    from time import sleep
    LightL = LightIntensity(36)
    LightR = LightIntensity(39)
    while True:
        print('LightL', LightL.read())
        print('LightR', LightR.read())
        sleep(0.5)

if __name__ == '__main__':
    unit_test()
