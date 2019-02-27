
import _thread

import time

class task(object):
    
    lock = _thread.allocate_lock()

    def __init__(self):
        self.alive = False

    def run(self):
        if task.lock.acquire():
            while self.alive:
                time.sleep(0.25)
                print("running")
            task.lock.release()
        _thread.exit()
        
    def stop(self):
        self.alive = False
        if task.lock.acquire():
            print("stop")
            task.lock.release()

    def start(self):
        self.stop()
        self.alive = True
        if task.lock.acquire():
            print("start")
            _thread.start_new_thread(self.run, ())
            task.lock.release()

if __name__ == "__main__":
    tmp = task()
    tmp.start()
    time.sleep(1)
    tmp.start()
    time.sleep(2)
    tmp.start()
    # time.sleep(3)
    tmp.stop()

