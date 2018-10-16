
import socket
import ure

def http_get(url):
    _, _, host, path = url.split('/', 3)
    print(path)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    while True:
        data = s.recv(100)
        if data:
            # print(str(data, 'utf8'), end='')
            result = str(data)
            print(result)
            result = ure.match('<em>(.*)</em>', result)
            if result != None:
                print(result.group())
        else:
            break
    s.close()

http_get('https://tianqi.moji.com/weather/china/shanghai/shanghai')

'''
result = ure.match('<em>(.*)</em>', r'<em>29\xc2\xb0</em>')
print(result.group(0))
'''