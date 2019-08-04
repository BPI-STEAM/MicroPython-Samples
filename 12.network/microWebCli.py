"""
The MIT License (MIT)
Copyright © 2018 Jean-Christophe Bos & HC² (www.hc2.fr)
"""

from   struct import pack
import socket
import gc

class MicroWebCli :

    # ============================================================================
    # ===( Class AuthBasic  )=====================================================
    # ============================================================================

    class AuthBasic :

        # ------------------------------------------------------------------------

        def __init__(self, user, password) :
            if password is None :
                password = ''
            if not 'b2a_base64' in globals() :
                from binascii import b2a_base64
            cred = '%s:%s' % (user, password)
            self._auth = 'Basic %s' % b2a_base64(cred).decode().strip()

        # ------------------------------------------------------------------------

        def Apply(self, microWebCli) :
            microWebCli.Headers['Authorization'] = self._auth

    # ============================================================================
    # ===( Class AuthToken  )=====================================================
    # ============================================================================

    class AuthToken :

        # ------------------------------------------------------------------------

        def __init__(self, token) :
            self._auth = 'Bearer %s' % token

        # ------------------------------------------------------------------------

        def Apply(self, microWebCli) :
            microWebCli.Headers['Authorization'] = self._auth

    # ============================================================================
    # ===( Utils  )===============================================================
    # ============================================================================

    def _tryAllocByteArray(size) :
        for x in range(10) :
            try :
                gc.collect()
                return bytearray(size)
            except :
                pass
        return None

    # ----------------------------------------------------------------------------

    def _quote(s, safe='/') :
        r = ''
        for c in str(s) :
            if (c >= 'a' and c <= 'z') or \
               (c >= '0' and c <= '9') or \
               (c >= 'A' and c <= 'Z') or \
               (c in '.-_') or (c in safe) :
                r += c
            else :
                r += '%%%02X' % ord(c)
        return r

    # ----------------------------------------------------------------------------

    def _urlEncode(s) :
        return MicroWebCli._quote(s, ';/?:@&=+$,')

    # ----------------------------------------------------------------------------

    def _unquote(s) :
        r = str(s).split('%')
        for i in range(1, len(r)) :
            s = r[i]
            try :
                r[i] = chr(int(s[:2], 16)) + s[2:]
            except :
                r[i] = '%' + s
        return ''.join(r)

    # ----------------------------------------------------------------------------

    def _unquote_plus(s) :
        return MicroWebCli._unquote(str(s).replace('+', ' '))

    # ----------------------------------------------------------------------------

    def GETRequest(url, queryParams=None, auth=None, connTimeoutSec=10, socks5Addr=None) :
        c = MicroWebCli(url, auth=auth, connTimeoutSec=connTimeoutSec, socks5Addr=socks5Addr)
        if queryParams :
            c.QueryParams = queryParams
        c.OpenRequest()
        r = c.GetResponse()
        if r.IsSuccess() :
            return r.ReadContent()
        r.Close()
        if r.IsLocationMoved() :
            return MicroWebCli.GETRequest(r.LocationMovedURL(), queryParams, auth, connTimeoutSec, socks5Addr)
        return None

    # ----------------------------------------------------------------------------

    def POSTRequest(url, formData={}, auth=None, connTimeoutSec=10, socks5Addr=None) :
        c = MicroWebCli(url, method='POST', auth=auth, connTimeoutSec=connTimeoutSec, socks5Addr=socks5Addr)
        c.OpenRequestFormData(formData)
        r = c.GetResponse()
        if r.IsSuccess() :
            return r.ReadContent()
        r.Close()
        if r.IsLocationMoved() :
            return MicroWebCli.POSTRequest(r.LocationMovedURL(), formData, auth, connTimeoutSec, socks5Addr)
        return None

    # ----------------------------------------------------------------------------

    def JSONRequest(url, o=None, auth=None, connTimeoutSec=10, socks5Addr=None) :
        c = MicroWebCli( url,
                         method         = ('POST' if o else 'GET'),
                         auth           = auth,
                         connTimeoutSec = connTimeoutSec,
                         socks5Addr     = socks5Addr )
        if o :
            c.OpenRequestJSONData(o)
        else :
            c.OpenRequest()
        r = c.GetResponse()
        if r.IsSuccess() :
            return r.ReadContentAsJSON()
        r.Close()
        if r.IsLocationMoved() :
            return MicroWebCli.JSONRequest(r.LocationMovedURL(), o, auth, connTimeoutSec, socks5Addr)
        return None

    # ----------------------------------------------------------------------------

    def FileRequest(url, filepath, progressCallback=None, auth=None, connTimeoutSec=10, socks5Addr=None) :
        c = MicroWebCli(url, auth=auth, connTimeoutSec=connTimeoutSec, socks5Addr=socks5Addr)
        c.OpenRequest()
        r = c.GetResponse()
        if r.IsSuccess() :
            r.WriteContentToFile(filepath, progressCallback)
            return r.GetContentType()
        r.Close()
        if r.IsLocationMoved() :
            return MicroWebCli.FileRequest( r.LocationMovedURL(),
                                            filepath,
                                            progressCallback,
                                            auth,
                                            connTimeoutSec,
                                            socks5Addr )
        return None

    # ============================================================================
    # ===( Constructor )==========================================================
    # ============================================================================

    def __init__( self, url='', method='GET', auth=None, connTimeoutSec=10, socks5Addr=None) :
        self.URL            = url
        self.Method         = method
        self.Auth           = auth
        self.ConnTimeoutSec = connTimeoutSec
        self._socks5Addr    = socks5Addr
        self._headers       = { }
        self._socket        = None
        self._socketAddr    = None
        self._response      = None

    # ============================================================================
    # ===( Functions )============================================================
    # ============================================================================

    def _write(self, data) :
        try :
            data = memoryview(data)
            while data :
                n    = self._socket.write(data)
                data = data[n:]
            return True
        except :
            pass
        self.Close()
        raise Exception('Error to send data on connection')

    # ------------------------------------------------------------------------

    def _writeFirstLine(self) :
        path = MicroWebCli._quote(self.Path)
        qs   = self.QueryString
        if qs != '' :
            path = path + '?' + qs
        self._write('%s %s HTTP/1.0\r\n' % (self.Method, path))

    # ------------------------------------------------------------------------

    def _writeHeader(self, name, value) :
        self._write("%s: %s\r\n" % (name, value))

    # ------------------------------------------------------------------------

    def _writeEndHeader(self) :
        self._write("\r\n")

    # ------------------------------------------------------------------------

    def OpenRequest( self,
                     data           = None,
                     contentType    = None,
                     contentLength  = None ) :
        if self._socket :
            raise Exception('Request is already opened')
        if not self.URL :
            raise Exception('No URL defined')
        if self.Socks5Addr :
            if not isinstance(self.Socks5Addr, tuple) or len(self.Socks5Addr) != 2 :
                raise Exception('"Socks5Addr" must be a tuple of (host, port)')
            host, port = self.Socks5Addr
            if not isinstance(host, str) or not isinstance(port, int) :
                raise Exception('"Socks5Addr" is incorrect ("%s", %s)' % self.Socks5Addr)
        else :
            host = self.Host
            port = self.Port
        self._response = None
        try :
            self._socketAddr = socket.getaddrinfo(host, port)[0][-1]
            cli              = socket.socket( socket.AF_INET,
                                              socket.SOCK_STREAM,
                                              socket.IPPROTO_TCP )
            cli.settimeout(self.ConnTimeoutSec)
            cli.connect(self._socketAddr)
        except :
            raise Exception('Error to connect to %s:%s' % (host, port))
        if self.Socks5Addr :
            err = None
            try :
                cli.send(b'\x05\x01\x00')
                b = cli.read(2)
                if b is None or len(b) < 2 or b[0] != 0x05 or b[1] != 0x00 :
                    err = "%s:%s doesn't supports MicroWebCli SOCKS5 client protocol" % self.Socks5Addr
                else :
                    h = self.Host.encode()
                    p = pack('>H', self.Port)
                    cli.send(b'\x05\x01\x00\x03' + bytes([len(h)]) + h + p)
                    b = cli.read(4)
                    if b is None or len(b) < 4 or b[1] != 0x00 :
                        err = "Error to connect to %s:%s through SOCKS5 server" % (self.Host, self.Port)
                    else :
                        if b[3] == 0x01 :
                            l = 4
                        elif b[3] == 0x03 :
                            l = cli.read(1)[0]
                        elif b[3] == 0x04 :
                            l = 16
                        cli.read(l + 2)
            except Exception as ex :
                err = 'Error during negotiation with SOCKS5 server (%s)' % ex
            if err :
                cli.close()
                raise Exception(err)
        if self.Proto == 'https' :
            if not 'ssl' in globals() :
                import ssl
            try :
                try :
                    cli = ssl.wrap_socket(cli, timeout=self.ConnTimeoutSec)
                except TypeError :
                    cli = ssl.wrap_socket(cli)
            except Exception as ex :
                cli.close()
                raise Exception('Error to open a secure SSL/TLS connection (%s)' % ex)
        self._socket = cli
        self._writeFirstLine()
        if data :
            contentLength = len(data)
        self._headers['Host'] = self.Host
        if self._auth :
            try :
                self._auth.Apply(self)
            except :
                raise Exception('Error to apply authentication using %s' % type(self._auth))
        else :
            self._headers.pop('Authorization', None)
        if contentType :
            self._headers['Content-Type'] = contentType
        else :
            self._headers.pop('Content-Type', None)
        if contentLength :
            self._headers['Content-Length'] = contentLength
        else :
            self._headers.pop('Content-Length', None)
        self._headers['User-Agent'] = 'MicroWebCli by JC`zic'
        for h in self._headers :
            self._writeHeader(h, self._headers[h])
        self._writeEndHeader()
        if data :
            self._write(data)

    # ------------------------------------------------------------------------

    def OpenRequestFormData(self, formData={}) :
        data = ''
        if len(formData) > 0 :
            for param in formData :
                if param != '' :
                    if data != '' :
                        data += '&'
                    data += MicroWebCli._quote(param) + '=' + MicroWebCli._quote(formData[param])
        self.OpenRequest( data          = data,
                          contentType   = 'application/x-www-form-urlencoded' )

    # ------------------------------------------------------------------------   

    def OpenRequestJSONData(self, o=None) :
        if not 'json' in globals() :
            import json
        try :
            data = json.dumps(o)
        except :
            raise Exception('Error to convert object to JSON format')
        self.OpenRequest( data          = data,
                          contentType   = 'application/json' )

    # ------------------------------------------------------------------------   

    def RequestWriteData(self, data) :
        self._write(data)

    # ------------------------------------------------------------------------

    def GetResponse(self) :
        if not self._response :
            self._response = MicroWebCli._response(self, self._socket, self._socketAddr)
        return self._response

    # ------------------------------------------------------------------------

    def IsClosed(self) :
        return self._socket is None

    # ------------------------------------------------------------------------

    def Close(self) :
        if self._socket :
            try :
                self._socket.close()
            except :
                pass
            self._socket = None

    # ============================================================================
    # ===( Properties )===========================================================
    # ============================================================================

    @property
    def ConnTimeoutSec(self) :
        return self._connTimeoutSec

    @ConnTimeoutSec.setter
    def ConnTimeoutSec(self, value) :
        self._connTimeoutSec = int(value) if value and int(value) > 0 else None

    # ------------------------------------------------------------------------

    @property
    def Method(self) :
        return self._method

    @Method.setter
    def Method(self, value) :
        self._method = str(value).upper()

    # ------------------------------------------------------------------------

    @property
    def URL(self) :
        host = self.Host
        if host != '' :
            proto = self.Proto
            port  = self.Port
            if ( proto == 'http'  and port == 80  ) or \
               ( proto == 'https' and port == 443 ) :
                port = ''
            else :
                port = ':' + str(port)
            url = proto + '://' + host + port + self.Path
            url = MicroWebCli._urlEncode(url)
            qs  = self.QueryString
            if qs != '' :
                return url + '?' + qs
            return url
        return None

    @URL.setter
    def URL(self, value) :
        try :
            s = str(value)
            if '://' in s :
                proto, s = s.split('://', 1)
            else :
                proto = 'http'
        except :
            raise ValueError('URL error (%s)' % value)
        self.Proto = proto
        if '/' in s :
            host, path = s.split('/', 1)
        elif '?' in s :
            host, path = s.split('?', 1)
            path       = '?' + path
        else :
            host = s
            path = ''
        if ':' in host :
            try :
                host, port = host.split(':')
                self.Port  = port
            except :
                raise ValueError('URL host:port error (%s)' % host)
        self.Host         = host
        self._queryParams = { }
        self.Path         = path

    # ------------------------------------------------------------------------

    @property
    def Proto(self) :
        return self._proto

    @Proto.setter
    def Proto(self, value) :
        value = str(value).lower()
        if value == 'http' :
            self._port = 80
        elif value == 'https' :
            self._port = 443
        else :
            raise ValueError('Unsupported URL protocol (%s)' % value)
        self._proto = value

    # ------------------------------------------------------------------------

    @property
    def Host(self) :
        return self._host
    
    @Host.setter
    def Host(self, value) :
        self._host = MicroWebCli._unquote_plus(str(value))

    # ------------------------------------------------------------------------

    @property
    def Port(self) :
        return self._port

    @Port.setter
    def Port(self, value) :
        self._port = int(value)

    # ------------------------------------------------------------------------

    @property
    def Path(self) :
        return self._path

    @Path.setter
    def Path(self, value) :
        x = value.split('?', 1)
        if len(x[0]) > 0 :
            if x[0][0] != '/' :
                x[0] = '/' + x[0]
            self._path = MicroWebCli._unquote_plus(x[0])
        else :
            self._path = '/'
        if len(x) == 2 :
            self.QueryString = x[1]

    # ------------------------------------------------------------------------

    @property
    def QueryString(self) :
        r = ''
        for param in self._queryParams :
            if param != '' :
                if r != '' :
                    r += '&'
                r += MicroWebCli._quote(param) + '=' + MicroWebCli._quote(self._queryParams[param])
        return r

    @QueryString.setter
    def QueryString(self, value) :
        self._queryParams = { }
        for x in value.split('&') :
            param = x.split('=', 1)
            if param[0] != '' :
                value = MicroWebCli._unquote(param[1]) if len(param) > 1 else ''
                self._queryParams[MicroWebCli._unquote(param[0])] = value

    # ------------------------------------------------------------------------

    @property
    def QueryParams(self) :
        return self._queryParams

    @QueryParams.setter
    def QueryParams(self, value) :
        if not isinstance(value, dict) :
            raise ValueError('QueryParams must be a dict')
        self._queryParams = value

    # ------------------------------------------------------------------------

    @property
    def Headers(self) :
        return self._headers

    @Headers.setter
    def Headers(self, value) :
        if not isinstance(value, dict) :
            raise ValueError('Headers must be a dict')
        self._headers = value

    # ------------------------------------------------------------------------

    @property
    def Auth(self) :
        return self._auth

    @Auth.setter
    def Auth(self, value) :
        self._auth = value

    # ------------------------------------------------------------------------

    @property
    def Socks5Addr(self) :
        return self._socks5Addr

    @Socks5Addr.setter
    def Socks5Addr(self, value) :
        self._socks5Addr = value

    # ============================================================================
    # ===( Class Response  )======================================================
    # ============================================================================

    class _response :

        # ------------------------------------------------------------------------

        def __init__(self, microWebCli, socket, addr) :
            self._microWebCli   = microWebCli
            self._socket        = socket
            self._addr          = addr
            self._httpVer       = None
            self._code          = None
            self._msg           = None
            self._headers       = { }
            self._contentType   = None
            self._contentLength = None
            self._processResponse()

        # ------------------------------------------------------------------------

        def _processResponse(self) :
            try :
                self._parseFirstLine()
                self._parseHeader()
                if self._contentLength == 0 :
                    self.Close()
            except :
                self._microWebCli.Close()
                raise Exception('Error to get response')

        # ------------------------------------------------------------------------

        def _parseFirstLine(self) :
            self._httpVer, code, self._msg = self._socket.readline() \
                                                         .decode()   \
                                                         .strip()    \
                                                         .split(' ', 2)
            self._code = int(code)

        # ------------------------------------------------------------------------

        def _parseHeader(self) :
            while True :
                elements = self._socket.readline() \
                                       .decode()   \
                                       .strip()    \
                                       .split(':', 1)
                if len(elements) == 2 :
                    self._headers[elements[0].strip()] = elements[1].strip()
                elif len(elements) == 1 and len(elements[0]) == 0 :
                    self._contentType   = self._headers.get("Content-Type", None)
                    ctLen               = self._headers.get("Content-Length", None)
                    self._contentLength = int(ctLen) if ctLen is not None else None
                    break

        # ------------------------------------------------------------------------

        def GetClient(self) :
            return self._microWebCli

        # ------------------------------------------------------------------------

        def GetAddr(self) :
            return self._addr

        # ------------------------------------------------------------------------

        def GetIPAddr(self) :
            return self._addr[0]

        # ------------------------------------------------------------------------

        def GetPort(self) :
            return self._addr[1]

        # ------------------------------------------------------------------------

        def GetHTTPVersion(self) :
            return self._httpVer

        # ------------------------------------------------------------------------

        def GetStatusCode(self) :
            return self._code

        # ------------------------------------------------------------------------

        def GetStatusMessage(self) :
            return self._msg

        # ------------------------------------------------------------------------

        def IsSuccess(self) :
            return (self._code >= 200 and self._code < 300)

        # ------------------------------------------------------------------------

        def IsLocationMoved(self) :
            return self.LocationMovedURL() is not None

        # ------------------------------------------------------------------------

        def LocationMovedURL(self) :
            if self._code >= 300 and self._code < 400 :
                return self._headers.get('Location', None)
            return None

        # ------------------------------------------------------------------------

        def GetHeaders(self) :
            return self._headers

        # ------------------------------------------------------------------------

        def GetContentType(self) :
            return self._contentType

        # ------------------------------------------------------------------------

        def GetContentLength(self) :
            return self._contentLength

        # ------------------------------------------------------------------------

        def ReadContent(self, size=None) :
            try :
                if size is None :
                    b = self._socket.read()
                    self.Close()
                    return b
                elif size > 0 :
                    b = self._socket.read(size)
                    if len(b) < size :
                        self.Close()
                    return b
            except MemoryError as memEx :
                self.Close()
                raise MemoryError('Error to read response content (%s)' % memEx)
            except :
                self.Close()
            return None

        # ------------------------------------------------------------------------

        def ReadContentInto(self, buf, nbytes=None) :
            if nbytes is None :
                nbytes = len(buf)
            if nbytes > 0 :
                try :
                    x = self._socket.readinto(buf, nbytes)
                    if x < nbytes :
                        self.Close()
                    return x
                except :
                    self.Close()
            return 0

        # ------------------------------------------------------------------------

        def ReadContentAsJSON(self) :
            cnt = self.ReadContent()
            if cnt :
                if not 'json' in globals() :
                    import json
                try :
                    return json.loads(cnt)
                except :
                    raise Exception('Error to parse JSON response : %s' % cnt)
            return None

        # ------------------------------------------------------------------------

        def WriteContentToFile(self, filepath, progressCallback=None) :
            fSize = self._contentLength
            buf   = MicroWebCli._tryAllocByteArray(fSize if fSize and fSize < 1024 else 1024)
            if not buf :
                raise MemoryError('Not enough memory to allocate buffer')
            buf = memoryview(buf)
            try :
                file = open(filepath, 'wb')
            except :
                raise Exception('Error to create file (%s)' % filepath)
            sizeRem = fSize
            pgrSize = 0
            while sizeRem is None or sizeRem > 0 :
                if sizeRem and sizeRem < len(buf) :
                    buf = buf[:sizeRem]
                x = self.ReadContentInto(buf)
                if x == 0 :
                    break
                if x < len(buf) :
                    buf = buf[:x]
                if sizeRem :
                    sizeRem -= x
                try :
                    file.write(buf)
                except :
                    break
                pgrSize += x
                if progressCallback :
                    try :
                        progressCallback(self, pgrSize, fSize)
                    except Exception as ex :
                        print('Error in progressCallback : %s' % ex)
            file.close()
            self.Close()
            if sizeRem and sizeRem > 0 :
                if not 'remove' in globals() :
                    from os import remove
                remove(filepath)
                raise Exception('Error to receive and save file (%s)' % filepath)

        # ------------------------------------------------------------------------

        def IsClosed(self) :
            return self._microWebCli.IsClosed()

        # ------------------------------------------------------------------------

        def Close(self) :
            self._microWebCli.Close()

    # ============================================================================
    # ============================================================================
    # ============================================================================

