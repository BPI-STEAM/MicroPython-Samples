
def webdav_server(other):
    try:
        import wifi
        wifi.try_connect()
        import time
        while wifi.isconnected() is False:
            time.sleep(1)
        import webdav
        webdav.start()

        other()
        
    finally:
        print('webdav.close()')
        webdav.close()

# This is a recommended usage

@webdav_server
def main():
    while True:
        pass
