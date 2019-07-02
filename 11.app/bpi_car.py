

import wifi
wifi.try_connect()

from machine import Pin, I2C
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=10000)
import car
car = car.bpicar(i2c)
import utime
import _thread
_thread.start_new_thread(car.car_test,())

from microWebSrv import MicroWebSrv
from microbit import *

# 返回数据response header
headers = {'Access-Control-Allow-Origin': '*'}

@MicroWebSrv.route('/get_temp')
def _httpHandlerTestGet(httpClient, httpResponse):
    params = httpClient.GetRequestQueryParams()
    tmp = temperature()  # get temperature ℃
    obj = {
        'temperature': str(tmp),
    }
    httpResponse.WriteResponseJSONOk(obj=obj, headers=headers)

# such as http://192.168.30.139/move?arrow=N
# such as http://192.168.30.139/move?arrow=W
# such as http://192.168.30.139/move?arrow=S
# such as http://192.168.30.139/move?arrow=E
@MicroWebSrv.route('/move')
def _httpHandlerTestGet(httpClient, httpResponse):
    params = httpClient.GetRequestQueryParams()
    arrow = params['arrow']
    if arrow is 'N':
        display.show(Image.ARROW_N)
        car.DataCache.append('N')
    if arrow is 'S':
        display.show(Image.ARROW_S)
        car.DataCache.append('S')
    if arrow is 'W':
        display.show(Image.ARROW_W)
        car.DataCache.append('W')
    if arrow is 'E':
        display.show(Image.ARROW_E)
        car.DataCache.append('E')
    httpResponse.WriteResponseJSONOk(obj={
        'arrow': arrow,
    }, headers=headers)

def _recvTextCallback(webSocket, msg):
    print("WS RECV TEXT : %s" % msg)

    arrow = msg

    if arrow is 'N':
        display.show(Image.ARROW_N)
        car.DataCache.append('N')
    if arrow is 'S':
        display.show(Image.ARROW_S)
        car.DataCache.append('S')
    if arrow is 'W':
        display.show(Image.ARROW_E)
        car.DataCache.append('W')
    if arrow is 'E':
        display.show(Image.ARROW_W)
        car.DataCache.append('E')

    webSocket.SendText("%s" % msg)

def _recvBinaryCallback(webSocket, data):
    print("WS RECV DATA : %s" % data)


def _closedCallback(webSocket):
    print("WS CLOSED")

def _acceptWebSocketCallback(webSocket, httpClient):
    print("WS ACCEPT")
    webSocket.RecvTextCallback = _recvTextCallback
    webSocket.RecvBinaryCallback = _recvBinaryCallback
    webSocket.ClosedCallback = _closedCallback

if __name__ == '__main__':
    if 'srv' in locals():
        reset()
    pin13.write_digital(1)
    import time
    is_alive = False
    mws = MicroWebSrv()
    while True:
        if is_alive is False:
            if wifi.isconnected():
                print(wifi.wlan.ifconfig())
                display.scroll(wifi.wlan.ifconfig()[0])
                mws.MaxWebSocketRecvLen = 32
                mws.WebSocketThreaded = False
                mws.AcceptWebSocketCallback = _acceptWebSocketCallback
                try:
                    is_alive = True
                    mws.Start(threaded=True)
                except Exception as e:
                    print(e)
            else:
                is_alive = False
                mws.Stop()

        pin13.write_digital(1)
        time.sleep(1)
        pin13.write_digital(0)
        time.sleep(1)

