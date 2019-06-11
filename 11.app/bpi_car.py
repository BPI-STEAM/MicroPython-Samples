import wifi
wifi.try_connect()

# 返回数据response header
headers = {'Access-Control-Allow-Origin': '*'}

from microbit import *
from microWebSrv import MicroWebSrv

@MicroWebSrv.route('/get_temp')
def _httpHandlerTestGet(httpClient, httpResponse):
    params = httpClient.GetRequestQueryParams()
    tmp = temperature()  # get temperature ℃
    obj = {
        'temperature': str(tmp),
    }
    httpResponse.WriteResponseJSONOk(obj=obj, headers=headers)

@MicroWebSrv.route('/N')
def _httpHandlerTestGet(httpClient, httpResponse):
    display.show(Image.ARROW_N)
    httpResponse.WriteResponseJSONOk(obj={
        'move': 'N',
    }, headers=headers)

@MicroWebSrv.route('/S')
def _httpHandlerTestGet(httpClient, httpResponse):
    display.show(Image.ARROW_S)
    httpResponse.WriteResponseJSONOk(obj={
        'move': 'S',
    }, headers=headers)

@MicroWebSrv.route('/W')
def _httpHandlerTestGet(httpClient, httpResponse):
    display.show(Image.ARROW_W)
    httpResponse.WriteResponseJSONOk(obj={
        'move': 'W',
    }, headers=headers)

@MicroWebSrv.route('/E')
def _httpHandlerTestGet(httpClient, httpResponse):
    display.show(Image.ARROW_E)
    httpResponse.WriteResponseJSONOk(obj={
        'move': 'E',
    }, headers=headers)

if __name__ == '__main__':
    if 'srv' in locals():
        reset()
    pin13.write_digital(1)
    import time
    while True:
        print(time.time())
        time.sleep(2)
        if wifi.isconnected():
            print(wifi.wlan.ifconfig())
            display.scroll(wifi.wlan.ifconfig()[0])
            srv = MicroWebSrv(webPath='www/')
            pin13.write_digital(0)
            srv.Start(False)
        else:
            pin13.write_digital(1)