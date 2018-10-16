import dht,time,machine
dht = dht.DHT11(machine.Pin(13))
while True:
	dht.measure()
	print("temperature:",dht.temperature())
	print("humidity:",dht.humidity())				#DHT22 can be read twice every second
	time.sleep(1)									#DHT11 can only be read once every second