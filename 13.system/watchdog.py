
import machine

t = machine.WDT(0, 5) # init wdt 0, timeout 5s

t.feed() # feed it

t.delete() # close it