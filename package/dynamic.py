
from webdav import lock

import _thread

_file, _state, _time = '', False, 0

def _file_time(file_name):
	from uos import stat
	return stat(file_name)[8] # Get File Time

def _check_file():
	import utime
	from uio import StringIO
	from uos import dupterm, dupterm_notify
	global _file, _state, _time
	run_cmd = "execfile('%s')\r\n" % (_file)
	dupterm(StringIO(run_cmd))
	dupterm_notify(None)
	bak, last_time = _file_time(_file), utime.time()
	while(_state):
		if (utime.time() > last_time + _time):
			tmp, last_time = _file_time(_file), utime.time()
			if(bak != tmp and lock.acquire()):
				bak = tmp
				dupterm(StringIO("\x03\x43"))
				dupterm_notify(None)
				dupterm(StringIO(run_cmd))
				dupterm_notify(None)
				lock.release()
	_thread.exit()
	
def start(file_name = 'index.py', check_time = 2):
	import os
	os.stat(file_name)
	global _file, _state, _time 
	_file, _state, _time = file_name, True, check_time
	_thread.start_new_thread(_check_file, ())

def close():
	global _state
	_state = False
	utime.sleep(1)
	
