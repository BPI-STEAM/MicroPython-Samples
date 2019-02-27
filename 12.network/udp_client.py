import wifi
wifi.try_connect()

from XAsyncSockets import XAsyncSocketsPool, XAsyncUDPDatagram
from   _thread  import start_new_thread

class NetServer:
    Pool = None

    def __init__(self, Server = ('0.0.0.0', 32)):
        if NetServer.Pool is None:
            NetServer.Pool = XAsyncSocketsPool()
            start_new_thread(NetServer.run_forever, ())

        self.UDPDatagram = XAsyncUDPDatagram.Create(NetServer.Pool, Server, 256)
        self.UDPDatagram.OnDataRecv = NetServer._onUDPDatagramDataRecv
        self.UDPDatagram.OnFailsToSend = NetServer._onUDPDatagramFailsToSend
        print("LocalAddr : %s:%s" % self.UDPDatagram.LocalAddr)

    def exit(self):
        self.UDPDatagram.Close()

    def unit_test(self):
        import time
        Remote = ('10.10.10.237', 9954)
        data = bytearray(u"1231")
        while True:
            self.UDPDatagram.AsyncSendDatagram(datagram=data, remoteAddr=Remote)
            print(data)
            time.sleep(2)

    def run_forever():
        try:
            NetServer.Pool.AsyncWaitEvents()
        finally:
            NetServer.Pool.StopWaitEvents()

    def _onUDPDatagramDataRecv(xAsyncUDPDatagram, remoteAddr, datagram):
        print('On UDP Datagram Data Recv (%s:%s) :' % remoteAddr, bytes(datagram), xAsyncUDPDatagram)

    def _onUDPDatagramFailsToSend(xAsyncUDPDatagram, datagram, remoteAddr):
        print('On UDP Datagram Fails To Send', bytes(datagram), remoteAddr, xAsyncUDPDatagram)

if __name__ == '__main__':
    client = NetServer()
    client.unit_test()
    client.exit()
