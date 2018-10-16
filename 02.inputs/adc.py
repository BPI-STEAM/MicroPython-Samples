from machine import ADC, Pin
adc = ADC(Pin(34))
adc.atten(ADC.ATTN_6DB)
while True:
	print(str(adc.read()))

