import urequests
from microbit import *

def get_weather():
    # 各城市ID详见：http://mobile.weather.com.cn/js/citylist.xml
    url = "http://www.weather.com.cn/data/cityinfo/101200801.html"
    rsp = urequests.get(url)
    data = eval(rsp.text) # eval函数用于把字符串类型的json数据->转为python的字典类型
    weather = data["weatherinfo"]
    L = weather["temp1"] #最低温
    H = weather["temp2"] #最高温
    return "L:" + L[:-1] + " H:" + H[:-1] # 数据样例->  L:16 H:23

result = get_weather()
print(result)
display.scroll(result)

# L[:-1] H[:-1]去掉℃和℉两个特殊符号，否则会出现编码错误