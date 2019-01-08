import time
import machine

t = list(time.localtime(94534523))
t.insert(3, 0)
t.pop()
print(t)

rtc = machine.RTC()

print(rtc.datetime(t))
print(rtc.datetime())


print(time.time())


#
# # print(time.time())
# t1 = time.localtime(546450051)
# print(t1)
# tm.datetime(t1)
# print(tm.datetime())
# t2 = time.maketime(time.localtime(546450052))
# print(t2)
# tm.datetime(t2)
# print(tm.datetime())

# print(time.time())
