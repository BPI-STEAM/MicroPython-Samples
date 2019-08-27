
import os
import time

def set_firmware(com):
    try:
        from mp.mpfshell import MpFileShell
        shell = MpFileShell(help=True)
        shell.do_open(com)
        shell.do_put('microbit')
    except Exception as e:
        print(e)
        return str(e)

def get_firmware(com):
    try:
        import sys
        sys.argv = [
                'AutoFlash.py', '--chip', 'esp32', 
                '--port', com, 
                '--baud', '921600',
                'read_flash', '0x1000', '0x250000', 'firmware.bin'
        ]
        
        from esptool import main
        main()
        return None
    except Exception as e:
        print(e)
        return str(e)

if __name__ == "__main__":
    local_com = 'com5'
    set_firmware(local_com)
    # get_firmware(local_com)