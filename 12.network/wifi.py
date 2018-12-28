import network

from button import Button

wlan = network.WLAN(network.STA_IF)

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

__button__, __last_button__ = False, False

def __check_button(button):
    global __button__, __last_button__
    if __last_button__ != button.is_pressed():
        __button__ = True

def start(led_delay=150, button=Button(35)):

    if isconnected():
        print('Wifi connected.')
        return

    global wlan, __button__, __last_button__
    __button__, __last_button__ = False, button.is_pressed()

    if wlan.active() is False:
        wlan.active(True)

    from machine import Timer
    from display import Display, Purple, Yellow, Green, Blue
    print('Press "A" to enter the smartconfig mode while the led is rolling')
    try:
        timer = Timer(-100)
        timer.init(period = 250, mode = Timer.PERIODIC, callback = lambda t : (__check_button(button)))
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
            
        Display().scroll(view, [Purple, Yellow, Green, Blue], led_delay)

        if __button__:
            print("Started wifi in smartconfig mode")
            smartconfig()
        else:
            print("Started wifi in normal mode")
            try_connect()

    except Exception as e:
        print(e)
    finally:
        Display().clear()
        timer.deinit()

