
import XAsyncSockets

import zhiwu

A = zhiwu.encode(43)
B = zhiwu.decode(55)

ServerIP = '192.168.43.239'
# ServerIP = '10.10.10.215'
# ServerIP = '192.168.123.164'

xAsyncSocketsPool = XAsyncSockets.XAsyncSocketsPool()
xAsyncUDPDatagram = XAsyncSockets.XAsyncUDPDatagram.Create(xAsyncSocketsPool, ('0.0.0.0', 32))

def _onUDPDatagramDataRecv(xAsyncUDPDatagram, remoteAddr, datagram) :
    # print('On UDP Datagram Data Recv (%s:%s) :' % remoteAddr, bytes(datagram))
    # print(str(B.core(bytes(datagram))))
    result = B.parse(bytes(datagram))
    # print(result)
    (B.get())
    if ':' in result[1]:
        Pack = A.command(result[1])
        xAsyncUDPDatagram.AsyncSendDatagram(datagram=bytearray(Pack), remoteAddr=(ServerIP, 9954))

    pass

def _onUDPDatagramFailsToSend(xAsyncUDPDatagram, datagram, remoteAddr) :
    # print('On UDP Datagram Fails To Send', bytes(datagram), remoteAddr)
    pass

if xAsyncUDPDatagram:
    xAsyncUDPDatagram.OnFailsToSend = _onUDPDatagramFailsToSend
    xAsyncUDPDatagram.OnDataRecv = _onUDPDatagramDataRecv
    # print("LocalAddr : %s:%s" % xAsyncUDPDatagram.LocalAddr)

    Pack = A.collect()
    xAsyncUDPDatagram.AsyncSendDatagram(datagram=bytearray(Pack), remoteAddr=(ServerIP, 9954))


from _thread  import start_new_thread

def tran_server():
    global xAsyncSocketsPool
    xAsyncSocketsPool.AsyncWaitEvents()

try:

    import urequests


    def get_weather():
        url = "http://www.weather.com.cn/data/cityinfo/101200801.html"
        rsp = urequests.get(url)
        data = eval(rsp.text)  # eval函数用于把字符串类型的json数据->转为python的字典类型
        weather = data["weatherinfo"]
        L = weather["temp1"]  # 最低温
        H = weather["temp2"]  # 最高温
        return L[:-1] + "~" + H[:-1]  # 数据样例->  L:16 H:23


    today = get_weather()

    import time
    from esp import dht_readinto


    class DHTBase:
        def __init__(self, pin):
            self.pin = pin
            self.buf = bytearray(5)

        def measure(self):
            buf = self.buf
            dht_readinto(self.pin, buf)
            if (buf[0] + buf[1] + buf[2] + buf[3]) & 0xff != buf[4]:
                raise Exception("checksum error")


    class DHT11(DHTBase):
        def humidity(self):
            return self.buf[0]

        def temperature(self):
            return self.buf[2]


    from machine import Pin

    Pin(19, Pin.OUT).value(1)

    dht = DHT11(Pin(18))

    from machine import Pin, I2C
    import sh1106

    i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000)
    print(i2c.scan())
    display = sh1106.SH1106_I2C(128, 64, i2c, None, 0x3c)
    display.sleep(False)

    display.fill(0)
    display.show()

    start_new_thread(tran_server, ())

    cache = {}
    cache['humidity'], cache['temperat'] = 0, 0
    while True:
        time.sleep(0.8)

        dht.measure()

        if cache['humidity'] != dht.humidity():
            cache['humidity'] = dht.humidity()
            print("humidity:", dht.humidity())
            PackHumidity = A.collect("humidity", str(hex(dht.humidity())))
            xAsyncUDPDatagram.AsyncSendDatagram(datagram=bytearray(PackHumidity), remoteAddr=(ServerIP, 9954))

        if cache['temperat'] != dht.temperature():
            cache['temperat'] = dht.temperature()
            print("temperature:", dht.temperature())
            PackTemperat = A.collect("temperat", str(hex(dht.temperature())))
            xAsyncUDPDatagram.AsyncSendDatagram(datagram=bytearray(PackTemperat), remoteAddr=(ServerIP, 9954))

        display.text('   zhiwu idas   ', 0, 8, 1)
        display.text(str.format("humidity: {0}", dht.humidity()), 0, 20, 1)
        display.text(str.format("temperature: {0}", dht.temperature()), 0, 28, 1)
        display.text(str.format("dongguan: {0}", today), 0, 42, 1)
        display.text(str.format("time: {0}", time.time()), 0, 54, 1)

        display.show()
        display.fill(0)


finally:
    xAsyncSocketsPool.StopWaitEvents()
    del(A)
    del(B)

# ws:10.10.10.216,9954
