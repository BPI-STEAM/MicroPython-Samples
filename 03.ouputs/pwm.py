from machine import PWM, Pin

LED = PWM(Pin(18), freq=1000)

LED.duty(100)
