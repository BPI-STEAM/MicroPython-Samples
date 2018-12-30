
import XAsyncSockets

import zhiwu

A = zhiwu.encode(43)
B = zhiwu.decode(55)

# ServerIP = '192.168.123.97'
ServerIP = '10.10.10.215'

xAsyncSocketsPool = XAsyncSockets.XAsyncSocketsPool()
xAsyncUDPDatagram = XAsyncSockets.XAsyncUDPDatagram.Create(xAsyncSocketsPool, ('0.0.0.0', 32))

def _onUDPDatagramDataRecv(xAsyncUDPDatagram, remoteAddr, datagram) :
    # print('On UDP Datagram Data Recv (%s:%s) :' % remoteAddr, bytes(datagram))
    # print(str(B.core(bytes(datagram))))
    print(B.parse(bytes(datagram)))
    print(B)


def _onUDPDatagramFailsToSend(xAsyncUDPDatagram, datagram, remoteAddr) :
    print('On UDP Datagram Fails To Send', bytes(datagram), remoteAddr)

if xAsyncUDPDatagram:
    xAsyncUDPDatagram.OnFailsToSend = _onUDPDatagramFailsToSend
    xAsyncUDPDatagram.OnDataRecv = _onUDPDatagramDataRecv
    print("LocalAddr : %s:%s" % xAsyncUDPDatagram.LocalAddr)

    Pack = A.collect()
    xAsyncUDPDatagram.AsyncSendDatagram(datagram=bytearray(Pack), remoteAddr=(ServerIP, 9954))


from   _thread  import start_new_thread

def tran_server():
    global xAsyncSocketsPool
    xAsyncSocketsPool.AsyncWaitEvents()

try:
    start_new_thread(tran_server, ())
    import time
    while True:
        time.sleep(1)
        Pack = A.collect("sync", str(time.time()))
        xAsyncUDPDatagram.AsyncSendDatagram(datagram=bytearray(Pack), remoteAddr=(ServerIP, 9954))
        print(A)

finally:
    xAsyncSocketsPool.StopWaitEvents()
    del(A)
    del(B)
