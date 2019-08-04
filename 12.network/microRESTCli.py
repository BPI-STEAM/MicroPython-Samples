"""
The MIT License (MIT)
Copyright © 2018 Jean-Christophe Bos & HC² (www.hc2.fr)
"""

from microWebCli import MicroWebCli
from time        import gmtime, mktime

class MicroRESTCli :

    # ============================================================================
    # ===( Utils  )===============================================================
    # ============================================================================

    def Timestamp2JsonDT(timestamp=None) :
        t = gmtime(timestamp)
        return "%4d-%02d-%02dT%02d:%02d:%02dZ" % (t[0], t[1], t[2], t[3], t[4], t[5])

    # ----------------------------------------------------------------------------

    def JsonDT2Timestamp(jsonDT) :
        if jsonDT is None :
            return None
        try :
            return mktime( ( int(jsonDT[ 0: 4]),
                             int(jsonDT[ 5: 7]),
                             int(jsonDT[ 8:10]),
                             int(jsonDT[11:13]),
                             int(jsonDT[14:16]),
                             int(jsonDT[17:19]),
                             None,
                             None ) )
        except :
            raise Exception('Error to convert JSON datetime (%s)' % jsonDT)

    # ============================================================================
    # ===( Constructor )==========================================================
    # ============================================================================

    def __init__(self, baseUrl, user=None, password=None, token=None) :
        if not baseUrl.endswith('/') :
            baseUrl += '/'
        if user :
            auth = MicroWebCli.AuthBasic(user, password)
        elif token :
            auth = MicroWebCli.AuthToken(token)
        else :
            auth = None
        self._baseUrl  = baseUrl
        self._cli      = MicroWebCli(baseUrl, auth=auth)
        self._lastCode = None
        self._lastMsg  = None
        self._lastJson = None
        if not self._cli.URL :
            raise Exception('Base URL is not correct (%s)' % baseUrl)

    # ============================================================================
    # ===( Functions )============================================================
    # ============================================================================

    def _req( self,
              method, resUrl, o=None,
              fileToSave=None, progressCallback=None, _bouncedURL=None ) :
        if not self._cli.IsClosed() :
            raise Exception('MicroRESTCli is already in processing')
        self._lastCode   = None
        self._lastMsg    = None
        self._lastJson   = None
        self._cli.Method = method
        url = self._baseUrl
        if resUrl :
            url += resUrl[1:] if resUrl.startswith('/') else resUrl
        self._cli.URL = url if not _bouncedURL else _bouncedURL
        if o :
            self._cli.OpenRequestJSONData(o)
        else :
            self._cli.OpenRequest()
        r = self._cli.GetResponse()
        if r.IsLocationMoved() :
            r.Close()
            return self._req(method, None, o, fileToSave, progressCallback, r.LocationMovedURL())
        self._lastCode = r.GetStatusCode()
        self._lastMsg  = r.GetStatusMessage()
        if not fileToSave or not r.IsSuccess() :
            if 'application/json' in r.GetContentType().lower() :
                try :
                    self._lastJson = r.ReadContentAsJSON()
                except Exception as ex :
                    if r.IsSuccess() :
                        raise ex
            else :
                r.Close()
                if r.IsSuccess() :
                    raise Exception('REST call did not return a json content type')
        if r.IsSuccess() :
            if fileToSave :
                r.WriteContentToFile(fileToSave, progressCallback)
                return r.GetContentType()
            else :
                return self._lastJson
        raise Exception( 'REST call failed with %d response code (%s)'
                         % (self._lastCode, self._lastMsg) )

    # ----------------------------------------------------------------------------

    def GET(self, resUrl, fileToSave=None, progressCallback=None) :
        return self._req( 'GET', resUrl,
                          fileToSave=fileToSave, progressCallback=progressCallback )

    # ----------------------------------------------------------------------------

    def POST(self, resUrl, o, fileToSave=None, progressCallback=None) :
        return self._req( 'POST', resUrl, o,
                          fileToSave=fileToSave, progressCallback=progressCallback )

    # ----------------------------------------------------------------------------

    def PUT(self, resUrl, o, fileToSave=None, progressCallback=None) :
        return self._req( 'PUT', resUrl, o,
                          fileToSave=fileToSave, progressCallback=progressCallback )

    # ----------------------------------------------------------------------------

    def PATCH(self, resUrl, o, fileToSave=None, progressCallback=None) :
        return self._req( 'PATCH', resUrl, o,
                          fileToSave=fileToSave, progressCallback=progressCallback )

    # ----------------------------------------------------------------------------

    def DELETE(self, resUrl, fileToSave=None, progressCallback=None) :
        return self._req( 'DELETE', resUrl,
                          fileToSave=fileToSave, progressCallback=progressCallback )

    # ----------------------------------------------------------------------------

    def GetLastStatusCode(self) :
        return self._lastCode

    # ----------------------------------------------------------------------------

    def GetLastStatusMessage(self) :
        return self._lastMsg

    # ----------------------------------------------------------------------------

    def GetLastJSONResponse(self) :
        return self._lastJson

    # ============================================================================
    # ===( Properties )===========================================================
    # ============================================================================

    @property
    def ConnTimeoutSec(self) :
        return self._cli.ConnTimeoutSec

    @ConnTimeoutSec.setter
    def ConnTimeoutSec(self, value) :
        self._cli.ConnTimeoutSec = value

    # ------------------------------------------------------------------------

    @property
    def Headers(self) :
        return self._cli.Headers

    @Headers.setter
    def Headers(self, value) :
        self._cli.Headers = value

    # ============================================================================
    # ============================================================================
    # ============================================================================

