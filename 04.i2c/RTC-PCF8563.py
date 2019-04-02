# https://github.com/gwvsol/ESP8266-RTC-PCF8563

from micropython import const
from time import localtime, mktime
from gc import collect

#Registers overview
_SECONDS = const(0x02)
_MINUTES = const(0x03)
_HOURS = const(0x04)
_DATE = const(0x05)
_WDAY = const(0x06)
_MONTH = const(0x07)
_YEAR = const(0x08)

class PCF8563(object):
    def __init__(self, i2c, i2c_addr, zone=0, dht=True):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        self.timebuf = None
        self.zone = zone
        self.block = False
        self.dht = dht
        if self.i2c_addr in self.i2c.scan():
            print('RTC: PCF8563 find at address: 0x%x ' %(self.i2c_addr))
        else:
            print('RTC: PCF8563 not found at address: 0x%x ' %(self.i2c_addr))
        collect() #Очищаем RAM
        
    #Преобразование двоично-десятичного формата
    def _bcd2dec(self, bcd):
        """Convert binary coded decimal (BCD) format to decimal"""
        return (((bcd & 0xf0) >> 4) * 10 + (bcd & 0x0f))

    #Преобразование в двоично-десятичный формат
    def _dec2bcd(self, dec):
        """Convert decimal to binary coded decimal (BCD) format"""
        tens, units = divmod(dec, 10)
        return (tens << 4) + units

    def _tobytes(self, num):
        return num.to_bytes(1, 'little')

    #Чтение времени или запись нового знвчения и преобразование в формат ESP8266
    #Возвращает кортеж в формате localtime() (в ESP8266 0 - понедельник, а 6 - воскресенье)
    def datetime(self, datetime=None):
        """Reading RTC time and convert to ESP8266 and Direct write un-none value.
        Range: seconds [0,59], minutes [0,59], hours [0,23],
        day [0,7], date [1-31], month [1-12], year [0-99]."""
        if datetime == None:
            """Reading RTC time and convert to ESP8266"""
            data = self.i2c.readfrom_mem(self.i2c_addr, _SECONDS, 7)
            ss = self._bcd2dec(data[0] & 0x7F)
            mm = self._bcd2dec(data[1] & 0x7F)
            hh = self._bcd2dec(data[2] & 0x3F)
            dd = self._bcd2dec(data[3] & 0x3F)
            wday = data[4] & 0x07
            MM = self._bcd2dec(data[5] & 0x1F)
            yy = self._bcd2dec(data[6]) + 2000
            return yy, MM, dd, hh, mm, ss, wday, 0 # wday in esp8266 0 == Monday, 6 == Sunday
        elif datetime != None:
            """Direct write un-none value"""
            if datetime == 'reset': #Если datetime = 'reset', сброс времени на 2000-01-01 00:00:00
                (yy, MM, mday, hh, mm, ss, wday, yday) = (0, 1, 1, 0, 0, 0, 0, 0)
            else:
                (yy, MM, mday, hh, mm, ss, wday, yday) = datetime
            if ss < 0 or ss > 59: #Записывем новое значение секунд
                raise ValueError('RTC: Seconds is out of range [0,59].')
            self.i2c.writeto_mem(self.i2c_addr, _SECONDS, self._tobytes(self._dec2bcd(ss)))
            if mm < 0 or mm > 59: #Записываем новое значение минут
                raise ValueError('RTC: Minutes is out of range [0,59].')
            self.i2c.writeto_mem(self.i2c_addr, _MINUTES, self._tobytes(self._dec2bcd(mm)))
            if hh < 0 or hh > 23: #Записываем новое значение часов
                raise ValueError('RTC: Hours is out of range [0,23].')
            self.i2c.writeto_mem(self.i2c_addr, _HOURS, self._tobytes(self._dec2bcd(hh)))  #Sets to 24hr mode
            if mday < 1 or mday > 31: #Записываем новое значение дней
                raise ValueError('RTC: Date is out of range [1,31].')
            self.i2c.writeto_mem(self.i2c_addr, _DATE, self._tobytes(self._dec2bcd(mday)))  #Day of month
            if wday < 0 or wday > 6: #Записываем новое значение дней недели
                raise ValueError('RTC: Day is out of range [0,6].')
            self.i2c.writeto_mem(self.i2c_addr, _WDAY, self._tobytes(self._dec2bcd(wday)))
            if MM < 1 or MM > 12: #Записываем новое значение месяцев
                raise ValueError('RTC: Month is out of range [1,12].')
            self.i2c.writeto_mem(self.i2c_addr, _MONTH, self._tobytes(self._dec2bcd(MM)))
            if yy < 0 or yy > 99: #Записываем новое значение лет
                raise ValueError('RTC: Years is out of range [0,99].')
            self.i2c.writeto_mem(self.i2c_addr, _YEAR, self._tobytes(self._dec2bcd(yy)))
            (yy, MM, mday, hh, mm, ss, wday, yday) = self.datetime() #Cчитываем записанное новое значение времени с PCF8563
            print('RTC: New Time: {:0>2d}-{:0>2d}-{:0>2d} {:0>2d}:{:0>2d}:{:0>2d}'.format(yy, MM, mday, hh, mm, ss)) #Выводим новое время PCF8563

    def settime(self, source='esp'):
        utc = self.datetime()
        if  source == 'esp': #Устанавливаем время с часов ESP8266
            utc = localtime()
        rtc = self.datetime() #Cчитываем значение времени с PCF8563
        #Блокировка перевода времени. Если октябрь, блокировка на 1час 3минуты
        if self.block and rtc[1] == 10:
            if rtc[3] == 2: #Если 2 часа, блокировка не снимается
                pass
            elif rtc[3] == 3 and rtc[4] <= 2: #Если 3 часа и меньше 2 минут, бликировка не снимается
                pass
            else: #Во всех остальных случаях блокировка снимается
                self.block = False
        #Если март, бликировка включена для следующего вызова метода
        elif self.block and rtc[1] == 3:
            if rtc[3] == 3: #Блокировка действует пока не измениться rtc[3] = 3
                pass
            else: #Во всех остальных случаях блокировка снимается
                self.block = False
        else: #Во всех остальных случаях блокировка снимается
            self.block = False
        (yy, MM, mday, hh, mm, ss, wday, yday) =  utc
        #Если существует разница во времени, применяем изменения
        if source == 'dht' and rtc[3] != hh:
            print('RTC: Old Time: {:0>2d}-{:0>2d}-{:0>2d} {:0>2d}:{:0>2d}:{:0>2d}'\
            .format(rtc[0], rtc[1], rtc[2], rtc[3], rtc[4], rtc[5]))
            self.datetime((yy - 2000, MM, mday, hh, mm, ss, wday, yday))
        elif source == 'esp' or source == 'ntp' or rtc[3] != hh or rtc[4] != mm or rtc[5] != ss:
            print('RTC: Old Time: {:0>2d}-{:0>2d}-{:0>2d} {:0>2d}:{:0>2d}:{:0>2d}'\
            .format(rtc[0], rtc[1], rtc[2], rtc[3], rtc[4], rtc[5]))
            self.datetime((yy - 2000, MM, mday, hh, mm, ss, wday, yday))
        #else: #Если разница во времени не обнаружена, выводим время с PCF8563
        #    print('RTC: No time change: {:0>2d}-{:0>2d}-{:0>2d} {:0>2d}:{:0>2d}:{:0>2d}'\
        #    .format(yy, MM, mday, hh, mm, ss))

if __name__ == "__main__":
		
	from machine import I2C, Pin
	i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000)
	rtc = PCF8563(i2c, 0x51, zone=3)
	print(rtc.datetime())
	