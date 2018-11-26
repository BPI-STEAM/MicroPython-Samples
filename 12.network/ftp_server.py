
def ftp_server(other):
    try:
        import wifi
        wifi.try_connect()
        import time
        while wifi.isconnected() is False:
            time.sleep(1)
        import ftptiny
        ftp = ftptiny.FtpTiny()
        ftp.start()

        other()
        
    finally:
        print('ftp.stop()')
        ftp.stop()

# This is a recommended usage

@ftp_server
def main():
    while True:
        pass

