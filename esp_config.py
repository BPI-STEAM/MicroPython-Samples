#!/usr/bin/env python
# coding: utf-8
'''
@File   :esp_config.py.py
@Author :youxinweizhi
@Date   :2019/3/29
@Github :https://github.com/youxinweizhi
'''
import os
import time

def erase(com):
    FLASH_START = "0x1000"
    FLASH_MODE = "dio"
    FLASH_FREQ = "40m"

    import sys
    sys.argv = [
            'AutoFlash.py', '--chip', 'esp32', 
            '--port', com, 
            '--baud', '921600', # 921600
            'erase_flash',
    ]
    
    try:
        from esptool import main
        main()
        return None
    except Exception as e:
        print(e)
        return str(e)


def flash(com):

    erase(com)

    FLASH_START = "0x1000"
    FLASH_MODE = "dio"
    FLASH_FREQ = "40m"

    import sys
    sys.argv = [
            'AutoFlash.py', '--chip', 'esp32', 
            '--port', com, 
            '--baud', '921600', # 921600
            'write_flash', '-z',
            '--flash_mode', FLASH_MODE, 
            '--flash_size', '4MB',
            '--flash_freq', FLASH_FREQ,
            '0x1000', os.getcwd() + '\\firmware.bin',
    ]
    
    try:
        from esptool import main
        main()
        return None
    except Exception as e:
        print(e)
        return str(e)

if __name__ == "__main__":
    flash('com3')