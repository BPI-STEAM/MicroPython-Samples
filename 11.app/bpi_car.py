

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
    if arrow is 'S':
        display.show(Image.ARROW_S)
    if arrow is 'W':
        display.show(Image.ARROW_W)
    if arrow is 'E':
        display.show(Image.ARROW_E)
    httpResponse.WriteResponseJSONOk(obj={
        'arrow': arrow,
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