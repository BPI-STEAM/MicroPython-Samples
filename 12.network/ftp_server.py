import wifi
wifi.try_connect()

try:
    import ftptiny
    ftp = ftptiny.FtpTiny() # create one
    ftp.start() # start an ftp thread
    while True:
        pass # your working
finally:
    ftp.stop()
