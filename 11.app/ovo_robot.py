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

@MicroWebSrv.route('/SAD')
def _httpHandlerTestGet(httpClient, httpResponse):
    params = httpClient.GetRequestQueryParams()
    display.show(Image.SAD)

@MicroWebSrv.route('/scroll')
def _httpHandlerTestGet(httpClient, httpResponse):
    params = httpClient.GetRequestQueryParams()
    display.scroll(str(params['text']))

if __name__ == '__main__':
    if 'srv' in locals():
        reset()
    pin13.write_digital(0)
    import time
    while True:
        time.sleep(2)
        if wifi.isconnected():
            srv = MicroWebSrv(webPath='www/')
            srv.Start(True)
            pin13.write_digital(1)
        else:
            pin13.write_digital(0)