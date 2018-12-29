
def pin_change(p):
    print('pin change', p)
    
from machine import Pin
Pin(34, Pin.IN).irq(trigger=Pin.IRQ_RISING, handler=pin_change)