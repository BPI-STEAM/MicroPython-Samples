
from zwlib import *

def set_time(secs):
    import time
    import machine

    tmp = list(time.localtime(secs))
    tmp.insert(3, 0)
    tmp.pop()
    # print(tmp)

    # print(time.time())
    machine.RTC().datetime(tmp)
    # print(time.time())

    # import ntptime
    # time.settime()

class encode:

    def __init__(self, crypt = 43, entid = 1, devid = "0123456789ABC", devip = 1):
        self.en = encode_new(crypt, entid, bytearray(devid), devip)

    def __del__(self):
        encode_del(self.en)

    def get(self):
        return encode_parse(self.en)

    def __str__(self):
        return encode_parse(self.en)

    def command(self, cmd = "this is test"):
        return encode_command(self.en, cmd)

    def collect(self, source = "source", data = "data"):
        return encode_collect(self.en, source, data)

class decode:

    def __init__(self, crypt = 3):
        self.de = decode_new(crypt)

    def __del__(self):
        decode_del(self.de)

    def get(self):
        return decode_parse(self.de)

    def __str__(self):
        return decode_parse(self.de)

    def core(self, pack):
        return decode_core(self.de, pack)

    def parse(self, pack):
        res = self.core(pack)
        if (res != None):
            if (pack[0] == TYPE_COLLECT):
                # return [TYPE_COLLECT, res[1:ord(res[0]) + 1], res[ord(res[0]) + 2:]]
                src = 1+res[0]
                dt = 1 + src
                return [TYPE_COLLECT, res[1:src], res[dt:dt+res[src]]]
            elif (pack[0] == TYPE_COMMAND):
                result = [TYPE_COMMAND, res[1:res[0] + 1]]
                # print(result)
                if (result[1] == b'TimeSysn'):
                    # print(decode_parse(self.de))
                    set_time(decode_parse(self.de)[0])
                return result
        return None

if __name__ == '__main__':

    A = encode()
    print(A)
    B = decode()
    print(B)

    Pack = A.collect()
    print(B.parse(bytearray(Pack)))
    print(A)
    print(B)

    Pack = A.command()
    Data = B.parse(bytearray(Pack))
    print(B.parse(bytearray(Pack)))
    print(A)
    print(B)

    print(Data[1].decode('iso-8859-1'))
    print(Data[1].split(b' '))

    Pack = A.command('TimeSysn')
    print(B.parse(bytearray(Pack)))
    print(A)
    print(B)

    del(A)
    del(B)
    # A.__del__()
    # B.__del__()
