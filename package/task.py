import _thread

from utime import sleep_ms

class Task(object):
    lock = _thread.allocate_lock()

    def __init__(self, event=(lambda args: print('task running')), args=None):
        self.alive = False
        self.set_cb(event, args)

    def set_cb(self, event, args):
        self.event = event
        self.args = args

    def run(self):
        if Task.lock.acquire():
            while self.alive:
                self.event(self.args)
            Task.lock.release()
        _thread.exit()

    def stop(self):
        if self.alive is True:
            self.alive = False
            if Task.lock.acquire():
                # print("stop")
                Task.lock.release()

    def start(self, size=2048):
        self.stop()
        self.alive = True
        if Task.lock.acquire():
            # print("start")
            import gc
            gc.collect()
            _thread.stack_size(size)
            _thread.start_new_thread(self.run, ())
            _thread.stack_size()
            Task.lock.release()

if __name__ == "__main__":
    import time
    def unit_test(args):
        print('unit_test', args)
        sleep_ms(500)
    tmp = Task(unit_test, {'name': 'unit_test_0'})
    tmp.start()
    time.sleep(1)
    tmp.set_cb(unit_test, {'name': 'unit_test_1'})
    tmp.start()
    time.sleep(2)
    tmp.set_cb(unit_test, {'name': 'unit_test_2'})
    tmp.start()
    # time.sleep(3)
    tmp.stop()

