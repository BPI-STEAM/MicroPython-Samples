import machine,time
LED = machine.PWM(machine.Pin(18), freq=1000)
tick = 0 # counter variable
while True:
	if tick < 40:
		# self.tick % 20 gives a number 0 to 19
        # subtracting 9 makes it -9 to 10
        # abs maps it 9 to 0 to 10
        # subtracting from 10 maps it 1 to 10 to 0
        # multiplying by 25 scales it 25 to 250 to 0
		LED.duty((10 - (abs((tick % 20) - 9))) * 25)
	tick = (tick + 1) % 100
	time.sleep(0.1) 