from machine import RTC
import time
start_year = 2018
start_month = 7
start_day = 20
start_weekday = 5 # Tuesday (1-7 is Monday to Sunday)
start_hours = 11
start_minutes = 11
start_seconds = 11
start_subseconds = 255 # this is a value that counts down from 255 to 0

rtc = RTC()

# datetime() takes one parameter (an 8-tuple) hence the double bracket (()) below
rtc.datetime((start_year, start_month, start_day, start_weekday, start_hours, start_minutes, start_seconds, start_subseconds))

# weekday in datetime() understands Monday as 1 and Sunday as 7
days_of_the_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday' ]

while True:
	# clock.datetime() returns an 8-tuple
	clock_t = rtc.datetime()
	'''
	year = clock_t[0]
	month = clock_t[1]
	day = clock_t[2]
	weekday = clock_t[3]
	hour = clock_t[4]
	min = clock_t[5]
	sec = clock_t[6]
	subsec = clock_t[7] # likely we wont be using this hence it's commented
	
	print('The time is', hour,':',min,':',sec)
	print('Today\'s date is', day,'.',month,'.',year)
	print('Today is a', days_of_the_week[weekday])
	'''
	time.sleep(0.1)
	