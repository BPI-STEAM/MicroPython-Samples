import wifi
wifi.start()

server_ip = "192.168.123.97"
client_id = "umqtt_client"

import time

from umqtt.robust import MQTTClient

try:

    c = MQTTClient(client_id, server_ip)
    c.DEBUG = True

    def sub_cb(topic, msg):
        print((topic, msg))
        c.publish(topic, msg)

    c.set_callback(sub_cb)

    if not c.connect(clean_session = False):
            c.subscribe(b"foo_topic")
        
    c.publish(b"foo_topic", b"hello")

    while 1:
        time.sleep(1)
        if c.check_msg() is not None:
            c.wait_msg()
        else:
            print('other operator')

finally:
    c.disconnect()