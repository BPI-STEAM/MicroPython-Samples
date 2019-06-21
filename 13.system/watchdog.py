
import machine

t = machine.WDT(0, 5000) # init wdt 0, timeout 5s

t.feed() # feed it

t.delete() # close it

# t.feed() # feed it
import time
while True:
    print("watchdog...")
    # t.feed() # feed it
    time.sleep(1)
