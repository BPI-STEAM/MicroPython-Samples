try:
    import network
    mdns = network.mDNS()
    mdns.start("bpibit", "MicroPython with mDNS")
    _ = mdns.addService('_ftp', '_tcp', 21, "MicroPython",
                        {"board": "ESP32", "service": "bpibit FTP File transfer", "passive": "True"})
    _ = mdns.addService('_telnet', '_tcp', 23, "MicroPython", {"board": "ESP32", "service": "bpibit Telnet REPL"})
    _ = mdns.addService('_http', '_tcp', 80, "MicroPython", {"board": "ESP32", "service": "bpibit Web server"})
    print("mDNS started")
except Exception as e:
    print("mDNS not started")