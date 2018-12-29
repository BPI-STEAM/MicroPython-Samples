"""
The MIT License (MIT)
Copyright © 2018 Jean-Christophe Bos & HC² (www.hc2.fr)
"""


from   _thread  import allocate_lock, start_new_thread
from   time     import sleep
from   select   import select
import socket
import ssl

try :
    from time import perf_counter
except :
    from time import ticks_ms
    def perf_counter() :
        return ticks_ms() / 1000

# ============================================================================
# ===( XAsyncSocketsPool )====================================================
# ============================================================================

class XAsyncSocketsPoolException(Exception) :
    pass

class XAsyncSocketsPool :

    def __init__(self) :
        self._processing   = False
        self._threadsCount = 0
        self._opLock       = allocate_lock()
        self._asyncSockets = { }
        self._readList     = [ ]
        self._writeList    = [ ]
        self._handlingList = [ ]

    # ------------------------------------------------------------------------

    def _incThreadsCount(self) :
        self._opLock.acquire()
        self._threadsCount += 1
        self._opLock.release()

    # ------------------------------------------------------------------------

    def _decThreadsCount(self) :
        self._opLock.acquire()
        self._threadsCount -= 1
        self._opLock.release()

    # ------------------------------------------------------------------------

    def _addSocket(self, socket, asyncSocket) :
        if socket :
            socketno = socket.fileno()
            self._opLock.acquire()
            ok = (socketno not in self._asyncSockets)
            if ok :
                self._asyncSockets[socketno] = asyncSocket
            self._opLock.release()
            return ok
        return False

    # ------------------------------------------------------------------------

    def _removeSocket(self, socket) :
        if socket :
            socketno = socket.fileno()
            self._opLock.acquire()
            ok = (socketno in self._asyncSockets)
            if ok :
                del self._asyncSockets[socketno]
                if socket in self._readList :
                    self._readList.remove(socket)
                if socket in self._writeList :
                    self._writeList.remove(socket)
            self._opLock.release()
            return ok
        return False

    # ------------------------------------------------------------------------

    def _socketListAdd(self, socket, socketsList) :
        self._opLock.acquire()
        ok = (socket.fileno() in self._asyncSockets and socket not in socketsList)
        if ok :
            socketsList.append(socket)
        self._opLock.release()
        return ok

    # ------------------------------------------------------------------------

    def _socketListRemove(self, socket, socketsList) :
        self._opLock.acquire()
        ok = (socket.fileno() in self._asyncSockets and socket in socketsList)
        if ok :
            socketsList.remove(socket)
        self._opLock.release()
        return ok

    # ------------------------------------------------------------------------

    _CHECK_SEC_INTERVAL = 1.0

    def _processWaitEvents(self) :
        self._incThreadsCount()
        timeSec = perf_counter()
        while self._processing :
            try :
                rd, wr, ex = select( self._readList,
                                     self._writeList,
                                     self._readList,
                                     self._CHECK_SEC_INTERVAL )
            except :
                continue
            if not self._processing :
                break
            for socketsList in ex, wr, rd :
                for socket in socketsList :
                    asyncSocket = self._asyncSockets.get(socket.fileno(), None)
                    if asyncSocket and self._socketListAdd(socket, self._handlingList) :
                        if socketsList is ex :
                            asyncSocket.OnExceptionalCondition()
                        elif socketsList is wr :
                            asyncSocket.OnReadyForWriting()
                        else :
                            asyncSocket.OnReadyForReading()
                        self._socketListRemove(socket, self._handlingList)
            sec = perf_counter()
            if sec > timeSec + self._CHECK_SEC_INTERVAL :
                timeSec = sec
                for asyncSocket in list(self._asyncSockets.values()) :
                    if asyncSocket.ExpireTimeSec and \
                       timeSec > asyncSocket.ExpireTimeSec :
                        asyncSocket._close(XClosedReason.Timeout)
        self._decThreadsCount()

    # ------------------------------------------------------------------------

    def AddAsyncSocket(self, asyncSocket) :
        try :
            socket = asyncSocket.GetSocketObj()
        except :
            raise XAsyncSocketsPoolException('AddAsyncSocket : "asyncSocket" is incorrect.')
        return self._addSocket(socket, asyncSocket)

    # ------------------------------------------------------------------------

    def RemoveAsyncSocket(self, asyncSocket) :
        try :
            socket = asyncSocket.GetSocketObj()
        except :
            raise XAsyncSocketsPoolException('RemoveAsyncSocket : "asyncSocket" is incorrect.')
        return self._removeSocket(socket)

    # ------------------------------------------------------------------------

    def GetAllAsyncSockets(self) :
        return list(self._asyncSockets.values())

    # ------------------------------------------------------------------------

    def GetAsyncSocketByID(self, id) :
        return self._asyncSockets.get(id, None)

    # ------------------------------------------------------------------------

    def NotifyNextReadyForReading(self, asyncSocket, notify) :
        try :
            socket = asyncSocket.GetSocketObj()
        except :
            raise XAsyncSocketsPoolException('NotifyNextReadyForReading : "asyncSocket" is incorrect.')
        if notify :
            self._socketListAdd(socket, self._readList)
        else :
            self._socketListRemove(socket, self._readList)

    # ------------------------------------------------------------------------

    def NotifyNextReadyForWriting(self, asyncSocket, notify) :
        try :
            socket = asyncSocket.GetSocketObj()
        except :
            raise XAsyncSocketsPoolException('NotifyNextReadyForWriting : "asyncSocket" is incorrect.')
        if notify :
            self._socketListAdd(socket, self._writeList)
        else :
            self._socketListRemove(socket, self._writeList)

    # ------------------------------------------------------------------------

    def AsyncWaitEvents(self, threadsCount=0) :
        if self._processing or self._threadsCount :
            return
        self._processing = True
        if threadsCount > 0 :
            try :
                for i in range(threadsCount) :
                    start_new_thread(self._processWaitEvents, ())
            except :
                raise XAsyncSocketsPoolException('AsyncWaitEvents : Fatal error to create new threads...')
        else :
            self._processWaitEvents()

    # ------------------------------------------------------------------------

    def StopWaitEvents(self) :
        self._processing = False
        while self._threadsCount :
            sleep(0.001)

# ============================================================================
# ===( XClosedReason )========================================================
# ============================================================================

class XClosedReason() :

    Error        = 0x00
    ClosedByHost = 0x01
    ClosedByPeer = 0x02
    Timeout      = 0x03

# ============================================================================
# ===( XAsyncSocket )=========================================================
# ============================================================================

class XAsyncSocketException(Exception) :
    pass

class XAsyncSocket :

    def __init__(self, asyncSocketsPool, socket, bufSlot=None) :
        if type(self) is XAsyncSocket :
            raise XAsyncSocketException('XAsyncSocket is an abstract class and must be implemented.')
        self._asyncSocketsPool = asyncSocketsPool
        self._socket           = socket
        self._bufSlot          = bufSlot
        self._expireTimeSec    = None
        self._state            = None
        self._onClosed         = None
        try :
            socket.settimeout(0)
            socket.setblocking(0)
            if bufSlot is not None and type(bufSlot) is not XBufferSlot :
                raise Exception()
            asyncSocketsPool.AddAsyncSocket(self)
        except :
            raise XAsyncSocketException('XAsyncSocket : Arguments are incorrects.')

    # ------------------------------------------------------------------------

    def _setExpireTimeout(self, timeoutSec) :
        try :
            if timeoutSec and timeoutSec > 0 :
                self._expireTimeSec = perf_counter() + timeoutSec
        except :
            raise XAsyncSocketException('"timeoutSec" is incorrect to set expire timeout.')

    # ------------------------------------------------------------------------

    def _removeExpireTimeout(self) :
        self._expireTimeSec = None

    # ------------------------------------------------------------------------

    def _close(self, closedReason=XClosedReason.Error, triggerOnClosed=True) :
        if self._asyncSocketsPool.RemoveAsyncSocket(self) :
            try :
                self._socket.close()
            except :
                pass
            self._socket = None
            if self._bufSlot is not None :
                self._bufSlot.Available = True
                self._bufSlot = None
            if triggerOnClosed and self._onClosed :
                try :
                    self._onClosed(self, closedReason)
                except Exception as ex :
                    raise XAsyncSocketException('Error when handling the "OnClose" event : %s' % ex)
            return True
        return False

    # ------------------------------------------------------------------------

    def GetAsyncSocketsPool(self) :
        return self._asyncSocketsPool

    # ------------------------------------------------------------------------

    def GetSocketObj(self) :
        return self._socket

    # ------------------------------------------------------------------------

    def Close(self) :
        return self._close(XClosedReason.ClosedByHost)

    # ------------------------------------------------------------------------

    def OnReadyForReading(self) :
        pass

    # ------------------------------------------------------------------------

    def OnReadyForWriting(self) :
        pass

    # ------------------------------------------------------------------------

    def OnExceptionalCondition(self) :
        self._close()

    # ------------------------------------------------------------------------

    @property
    def SocketID(self) :
        return self._socket.fileno() if self._socket else None

    @property
    def ExpireTimeSec(self) :
        return self._expireTimeSec

    @property
    def OnClosed(self) :
        return self._onClosed
    @OnClosed.setter
    def OnClosed(self, value) :
        self._onClosed = value

    @property
    def State(self) :
        return self._state
    @State.setter
    def State(self, value) :
        self._state = value

# ============================================================================
# ===( XAsyncTCPServer )======================================================
# ============================================================================

class XAsyncTCPServerException(Exception) :
    pass

class XAsyncTCPServer(XAsyncSocket) :

    @staticmethod
    def Create(asyncSocketsPool, srvAddr, srvBacklog=256, recvBufSlots=None) :
        try :
            srvSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except :
            raise XAsyncTCPServerException('Create : Cannot open socket (no enought memory).')
        try :
            srvSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            srvSocket.bind(srvAddr)
            srvSocket.listen(srvBacklog)
        except :
            raise XAsyncTCPServerException('Create : Error to binding the TCP server on this address.')
        if not recvBufSlots :
            recvBufSlots = XBufferSlots(256, 4096, keepAlloc=True)
        xAsyncTCPServer = XAsyncTCPServer( asyncSocketsPool,
                                           srvSocket,
                                           srvAddr,
                                           recvBufSlots )
        asyncSocketsPool.NotifyNextReadyForReading(xAsyncTCPServer, True)
        return xAsyncTCPServer

    # ------------------------------------------------------------------------

    def __init__(self, asyncSocketsPool, srvSocket, srvAddr, recvBufSlots) :
        try :
            super().__init__(asyncSocketsPool, srvSocket)
            self._srvAddr          = srvAddr
            self._recvBufSlots     = recvBufSlots
            self._onClientAccepted = None
        except :
            raise XAsyncTCPServerException('Error to creating XAsyncTCPServer, arguments are incorrects.')

    # ------------------------------------------------------------------------

    def OnReadyForReading(self) :
        try :
            cliSocket, cliAddr = self._socket.accept()
        except :
            return
        bufSlot = self._recvBufSlots.GetAvailableSlot()
        if not bufSlot or not self._onClientAccepted :
            cliSocket.close()
            return
        asyncTCPCli = XAsyncTCPClient( self._asyncSocketsPool,
                                       cliSocket,
                                       self._srvAddr,
                                       cliAddr,
                                       bufSlot )
        try :
            self._onClientAccepted(self, asyncTCPCli)
        except Exception as ex :
            asyncTCPCli._close()
            raise XAsyncTCPServerException('Error when handling the "OnClientAccepted" event : %s' % ex)

    # ------------------------------------------------------------------------

    @property
    def SrvAddr(self) :
        return self._srvAddr

    @property
    def OnClientAccepted(self) :
        return self._onClientAccepted
    @OnClientAccepted.setter
    def OnClientAccepted(self, value) :
        self._onClientAccepted = value

# ============================================================================
# ===( XAsyncTCPClient )======================================================
# ============================================================================

class XAsyncTCPClientException(Exception) :
    pass

class XAsyncTCPClient(XAsyncSocket) :

    @staticmethod
    def Create(asyncSocketsPool, srvAddr, connectTimeout=5, recvbufLen=4096) :
        try :
            size    = max(256, int(recvbufLen))
            bufSlot = XBufferSlot(size=size, keepAlloc=False)
        except :
            raise XAsyncTCPClientException('Create : "recvbufLen" is incorrect.')
        try :
            cliSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except :
            raise XAsyncTCPClientException('Create : Cannot open socket (no enought memory).')
        asyncTCPCli = XAsyncTCPClient( asyncSocketsPool,
                                       cliSocket,
                                       srvAddr,
                                       None,
                                       bufSlot )
        ok = False
        try :
            if hasattr(cliSocket, "connect_ex") :
                errno = cliSocket.connect_ex(srvAddr)
                if errno == 0 or errno == 36 :
                    asyncTCPCli._setExpireTimeout(connectTimeout)
                    ok = True
            else :
                cliSocket.settimeout(connectTimeout)
                cliSocket.setblocking(1)
                cliSocket.connect(srvAddr)
                cliSocket.settimeout(0)
                cliSocket.setblocking(0)
                ok = True
        except :
            pass
        if ok :
            asyncSocketsPool.NotifyNextReadyForWriting(asyncTCPCli, True)
            return asyncTCPCli
        asyncTCPCli._close()
        return None

    # ------------------------------------------------------------------------

    def __init__(self, asyncSocketsPool, cliSocket, srvAddr, cliAddr, bufSlot) :
        try :
            super().__init__(asyncSocketsPool, cliSocket, bufSlot)
            self._srvAddr          = srvAddr
            self._cliAddr          = cliAddr if cliAddr else ('0.0.0.0', 0)
            self._onFailsToConnect = None
            self._onConnected      = None
            self._onDataRecv       = None
            self._onDataRecvArg    = None
            self._onDataSent       = None
            self._onDataSentArg    = None
            self._sizeToRead       = None
            self._rdLinePos        = None
            self._rdBufView        = None
            self._wrBufView        = memoryview(b'')
            self._socketOpened     = (cliAddr is not None)
        except :
            raise XAsyncTCPClientException('Error to creating XAsyncTCPClient, arguments are incorrects.')

    # ------------------------------------------------------------------------

    def Close(self) :
        if self._wrBufView :
            try :
                self._socket.send(self._wrBufView)
            except :
                pass
        try :
            self._socket.shutdown(socket.SHUT_RDWR)
        except :
            pass
        return self._close(XClosedReason.ClosedByHost)

    # ------------------------------------------------------------------------

    def OnReadyForReading(self) :
        while True :
            if self._rdLinePos is not None :
                # In the context of reading a line,
                while True :
                    try :
                        b = self._socket.recv(1)
                    except ssl.SSLError as sslErr :
                        if sslErr.args[0] != ssl.SSL_ERROR_WANT_READ :
                            self._close()
                        return
                    except BlockingIOError as bioErr :
                        if bioErr.errno != 35 :
                            self._close()
                        return
                    except :
                        self._close()
                        return
                    if b :
                        if b == b'\n' :
                            lineLen = self._rdLinePos 
                            self._rdLinePos = None
                            self._asyncSocketsPool.NotifyNextReadyForReading(self, False)
                            self._removeExpireTimeout()
                            if self._onDataRecv :
                                line = self._bufSlot.Buffer[:lineLen]
                                try :
                                    line = line.decode()
                                except :
                                    pass
                                try :
                                    self._onDataRecv(self, line, self._onDataRecvArg)
                                except Exception as ex :
                                    raise XAsyncTCPClientException('Error when handling the "OnDataRecv" event : %s' % ex)
                            break
                        elif b != b'\r' :
                            if self._rdLinePos < self._bufSlot.Size :
                                self._bufSlot.Buffer[self._rdLinePos] = ord(b)
                                self._rdLinePos += 1
                            else :
                                self._close()
                                return
                    else :
                        self._close(XClosedReason.ClosedByPeer)
                        return
            elif self._rdBufView :
                # In the context of reading data,
                try :
                    n = self._socket.recv_into(self._rdBufView)
                except ssl.SSLError as sslErr :
                    if sslErr.args[0] != ssl.SSL_ERROR_WANT_READ :
                        self._close()
                    return
                except BlockingIOError as bioErr :
                    if bioErr.errno != 35 :
                        self._close()
                    return
                except :
                    self._close()
                    return
                self._rdBufView = self._rdBufView[n:]
                if n > 0 :
                    if not self._sizeToRead or not self._rdBufView :
                        self._rdBufView = None
                        self._asyncSocketsPool.NotifyNextReadyForReading(self, False)
                        self._removeExpireTimeout()
                        if self._onDataRecv :
                            size = self._sizeToRead if self._sizeToRead else n
                            data = memoryview(self._bufSlot.Buffer)[:size]
                            try :
                                self._onDataRecv(self, data, self._onDataRecvArg)
                            except Exception as ex :
                                raise XAsyncTCPClientException('Error when handling the "OnDataRecv" event : %s' % ex)
                else :
                    self._close(XClosedReason.ClosedByPeer)
                    return
            else :
                return

    # ------------------------------------------------------------------------

    def OnReadyForWriting(self) :
        if not self._socketOpened :
            if hasattr(self._socket, "getsockopt") :
                if self._socket.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR) :
                    self._close(XClosedReason.Error, triggerOnClosed=False)
                    if self._onFailsToConnect :
                        try :
                            self._onFailsToConnect(self)
                        except Exception as ex :
                            raise XAsyncTCPClientException('Error when handling the "OnFailsToConnect" event : %s' % ex)
                    return
                self._cliAddr = self._socket.getsockname()
                self._removeExpireTimeout()
            self._socketOpened = True
            if self._onConnected :
                try :
                    self._onConnected(self)
                except Exception as ex :
                    raise XAsyncTCPClientException('Error when handling the "OnConnected" event : %s' % ex)
        if self._wrBufView :
            try :
                n = self._socket.send(self._wrBufView)
            except :
                self._close()
                return
            self._wrBufView = self._wrBufView[n:]
            if self._wrBufView :
                return
            self._asyncSocketsPool.NotifyNextReadyForWriting(self, False)
            if self._onDataSent :
                try :
                    self._onDataSent(self, self._onDataSentArg)
                except Exception as ex :
                    raise XAsyncTCPClientException('Error when handling the "OnDataSent" event : %s' % ex)

    # ------------------------------------------------------------------------

    def AsyncRecvLine(self, onDataRecv=None, onDataRecvArg=None, timeoutSec=None) :
        if self._rdLinePos is not None or self._rdBufView :
            raise XAsyncTCPClientException('AsyncRecvLine : Already waiting asynchronous receive.')
        if self._socket :
            self._setExpireTimeout(timeoutSec)
            self._rdLinePos     = 0
            self._onDataRecv    = onDataRecv
            self._onDataRecvArg = onDataRecvArg
            self._asyncSocketsPool.NotifyNextReadyForReading(self, True)
            return True
        return False

    # ------------------------------------------------------------------------

    def AsyncRecvData(self, size=None, onDataRecv=None, onDataRecvArg=None, timeoutSec=None) :
        if self._rdLinePos is not None or self._rdBufView :
            raise XAsyncTCPClientException('AsyncRecvData : Already waiting asynchronous receive.')
        if self._socket :
            if size :
                try :
                    size = int(size)
                except :
                    raise XAsyncTCPClientException('AsyncRecvData : "size" is incorrect.')
            if not size or size < 0 :
                self._sizeToRead = None
                size             = self._bufSlot.Size
            elif size > self._bufSlot.Size :
                raise XAsyncTCPClientException('AsyncRecvData : "size" must be less or equal to buffer size.')
            else :
                self._sizeToRead = size
            self._setExpireTimeout(timeoutSec)
            self._rdBufView     = memoryview(self._bufSlot.Buffer)[:size]
            self._onDataRecv    = onDataRecv
            self._onDataRecvArg = onDataRecvArg
            self._asyncSocketsPool.NotifyNextReadyForReading(self, True)
            return True
        return False

    # ------------------------------------------------------------------------

    def AsyncSendData(self, data, onDataSent=None, onDataSentArg=None) :
        if self._socket :
            try :
                if bytes([data[0]]) :
                    if self._wrBufView :
                        self._wrBufView = memoryview(self._wrBufView.tobytes() + data)
                    else :
                        self._wrBufView = memoryview(data)
                    self._onDataSent    = onDataSent
                    self._onDataSentArg = onDataSentArg
                    self._asyncSocketsPool.NotifyNextReadyForWriting(self, True)
                    return True
            except :
                pass
            raise XAsyncTCPClientException('AsyncSendData : "data" is incorrect.')
        return False

    # ------------------------------------------------------------------------

    @property
    def SrvAddr(self) :
        return self._srvAddr

    @property
    def CliAddr(self) :
        return self._cliAddr

    @property
    def OnFailsToConnect(self) :
        return self._onFailsToConnect
    @OnFailsToConnect.setter
    def OnFailsToConnect(self, value) :
        self._onFailsToConnect = value

    @property
    def OnConnected(self) :
        return self._onConnected
    @OnConnected.setter
    def OnConnected(self, value) :
        self._onConnected = value

# ============================================================================
# ===( XAsyncUDPDatagram )====================================================
# ============================================================================

class XAsyncUDPDatagramException(Exception) :
    pass

class XAsyncUDPDatagram(XAsyncSocket) :

    @staticmethod
    def Create(asyncSocketsPool, localAddr=None, recvbufLen=4096, broadcast=False) :
        try :
            udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except :
            raise XAsyncUDPDatagramException('Create : Cannot open socket (no enought memory).')
        if broadcast :
            udpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        openRecv = (localAddr is not None)
        if openRecv :
            try :
                udpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                udpSocket.bind(localAddr)
            except :
                raise XAsyncUDPDatagramException('Create : Error to binding the UDP Datagram local address.')
            try :
                size    = max(256, int(recvbufLen))
                bufSlot = XBufferSlot(size=size, keepAlloc=False)
            except :
                raise XAsyncUDPDatagramException('Create : "recvbufLen" is incorrect.')
        else :
            bufSlot = None
        xAsyncUDPDatagram = XAsyncUDPDatagram(asyncSocketsPool, udpSocket, bufSlot)
        if openRecv :
            asyncSocketsPool.NotifyNextReadyForReading(xAsyncUDPDatagram, True)
        return xAsyncUDPDatagram

    # ------------------------------------------------------------------------

    def __init__(self, asyncSocketsPool, udpSocket, bufSlot) :
        try :
            super().__init__(asyncSocketsPool, udpSocket, bufSlot)
            self._wrDgramFiFo   = XFiFo()
            self._onFailsToSend = None
            self._onDataSent    = None
            self._onDataSentArg = None
            self._onDataRecv    = None
        except :
            raise XAsyncUDPDatagramException('Error to creating XAsyncUDPDatagram, arguments are incorrects.')

    # ------------------------------------------------------------------------

    def OnReadyForReading(self) :
        try :
            n, remoteAddr = self._socket.recvfrom_into(self._bufSlot.Buffer)
            datagram      = memoryview(self._bufSlot.Buffer)[:n]
        except :
            if hasattr(self._socket, "recvfrom_into") :
                return
            else :
                try :
                    buf, remoteAddr = self._socket.recvfrom(self._bufSlot.Size)
                    datagram        = memoryview(buf)
                except :
                    return
        if self._onDataRecv :
            try :
                self._onDataRecv(self, remoteAddr, datagram)
            except Exception as ex :
                raise XAsyncUDPDatagramException('Error when handling the "OnDataRecv" event : %s' % ex)


    # ------------------------------------------------------------------------

    def OnReadyForWriting(self) :
        if not self._wrDgramFiFo.Empty :
            datagram   = None
            remoteAddr = ('0.0.0.0', 0)
            try :
                datagram, remoteAddr = self._wrDgramFiFo.Get()
                self._socket.sendto(datagram, remoteAddr)
            except :
                if self._onFailsToSend :
                    try :
                        self._onFailsToSend(self, datagram, remoteAddr)
                    except Exception as ex :
                        raise XAsyncUDPDatagramException('Error when handling the "OnFailsToSend" event : %s' % ex)
            if not self._wrDgramFiFo.Empty :
                return
        self._asyncSocketsPool.NotifyNextReadyForWriting(self, False)
        if self._onDataSent :
            try :
                self._onDataSent(self, self._onDataSentArg)
            except Exception as ex :
                raise XAsyncUDPDatagramException('Error when handling the "OnDataSent" event : %s' % ex)

    # ------------------------------------------------------------------------

    def AsyncSendDatagram(self, datagram, remoteAddr, onDataSent=None, onDataSentArg=None) :
        if self._socket :
            try :
                if bytes([datagram[0]]) and len(remoteAddr) == 2 :
                    self._wrDgramFiFo.Put( (datagram, remoteAddr) )
                    self._onDataSent    = onDataSent
                    self._onDataSentArg = onDataSentArg
                    self._asyncSocketsPool.NotifyNextReadyForWriting(self, True)
                    return True
            except :
                pass
            raise XAsyncUDPDatagramException('AsyncSendDatagram : Arguments are incorrects.')
        return False

    # ------------------------------------------------------------------------

    @property
    def LocalAddr(self) :
        try :
            return self._socket.getsockname()
        except :
            return ('0.0.0.0', 0)

    @property
    def OnDataRecv(self) :
        return self._onDataRecv
    @OnDataRecv.setter
    def OnDataRecv(self, value) :
        self._onDataRecv = value

    @property
    def OnFailsToSend(self) :
        return self._onFailsToSend
    @OnFailsToSend.setter
    def OnFailsToSend(self, value) :
        self._onFailsToSend = value

# ============================================================================
# ===( XBufferSlot )==========================================================
# ============================================================================

class XBufferSlot :

    def __init__(self, size, keepAlloc=True) :
        self._available = True
        self._size      = size
        self._keepAlloc = keepAlloc
        self._buffer    = bytearray(size) if keepAlloc else None

    @property
    def Available(self) :
        return self._available
    @Available.setter
    def Available(self, value) :
        if value and not self._keepAlloc :
            self._buffer = None
        self._available = value

    @property
    def Size(self) :
        return self._size

    @property
    def Buffer(self) :
        self._available = False
        if self._buffer is None :
            self._buffer = bytearray(self._size)
        return self._buffer

# ============================================================================
# ===( XBufferSlots )=========================================================
# ============================================================================

class XBufferSlots :

    def __init__(self, slotsCount, slotsSize, keepAlloc=True) :
        self._slotsCount = slotsCount
        self._slotsSize  = slotsSize
        self._slots      = [ ]
        self._lock       = allocate_lock()
        for i in range(slotsCount) :
            self._slots.append(XBufferSlot(slotsSize, keepAlloc))

    def GetAvailableSlot(self) :
        ret = None
        self._lock.acquire()
        for slot in self._slots :
            if slot.Available :
                slot.Available = False
                ret = slot
                break
        self._lock.release()
        return ret

    @property
    def SlotsCount(self) :
        return self.slotsCount

    @property
    def SlotsSize(self) :
        return self.slotsSize

    @property
    def Slots(self) :
        return self._slots

# ============================================================================
# ===( XFiFo )================================================================
# ============================================================================

class XFiFoException(Exception) :
    pass

class XFiFo :

    def __init__(self) :
        self._lock  = allocate_lock()
        self._first = None
        self._last  = None

    def Put(self, obj) :
        self._lock.acquire()
        if self._first :
            self._last[1] = [obj, None]
            self._last    = self._last[1]
        else :
            self._last  = [obj, None]
            self._first = self._last
        self._lock.release()

    def Get(self) :
        self._lock.acquire()
        if self._first :
            obj         = self._first[0]
            self._first = self._first[1]
            self._lock.release()
            return obj
        else :
            self._lock.release()
            raise XFiFoException('Get : XFiFo is empty.')

    def Clear(self) :
        self._first = None
        self._last  = None

    @property
    def Empty(self) :
        return (self._first is None)

# ============================================================================
# ============================================================================
# ============================================================================
