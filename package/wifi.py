
import network

wlan = network.WLAN(network.STA_IF)

ifconfig = wlan.ifconfig

if wlan.active() is False:
    wlan.active(True)

def disconnect():
    global wlan
    wlan.disconnect()

def close():
    disconnect()
    global wlan
    wlan.active(False)

def isconnected():
    global wlan
    return wlan.isconnected()

def smartconfig():
    close()
    print(network.smartconfig())

def try_connect():
    import wifi_cfg
    wlan.disconnect()
    wlan.connect(wifi_cfg.WIFI_SSID, wifi_cfg.WIFI_PSWD)

is_smartconfig = False

def __irq_sc(p):
    p.irq().trigger(0)
    global is_smartconfig
    if is_smartconfig is False:
        is_smartconfig = True
        print("Started wifi in smartconfig mode")


def ready(led_delay=175, pin_id=35):
    if isconnected():
        print('Wifi connected.')
        return

    from machine import Pin
    pin = Pin(pin_id, Pin.IN).irq(trigger=Pin.IRQ_RISING, handler=__irq_sc)

    try:

        from display import Display, Purple, Yellow, Green, Blue
        print('Press "A" to enter the smartconfig mode while the led is rolling')
        mac = wlan.config('mac')
        view = ('%X%X' % (mac[4], mac[5]))
        try:
            import wifi_cfg
        except:
            default = "WIFI_SSID = 'webduino.io'\nWIFI_PSWD = 'webduino'\nHOST_NAME='bit%s'\n" % view
            print("create default wifi_cg.py : \n" + default + "or run smartconfig restart config ")
            with open("wifi_cfg.py", "w") as f:
                f.write(default)
            import wifi_cfg
        if hasattr(wifi_cfg, 'HOST_NAME'):
            wlan.config(dhcp_hostname=wifi_cfg.HOST_NAME)
        
        display = Display()
        
        display.scroll(view, [Purple, Yellow, Green, Blue], led_delay)
        
        from time import sleep
        sleep(3)
        
        if is_smartconfig:
            smartconfig()
        else:
            print("Started wifi in normal mode")
            try_connect()

    except Exception as e:
        print(e)
    finally:
        # display.clear()
        pin.trigger(0)

if __name__ == '__main__':
    ready()
    
