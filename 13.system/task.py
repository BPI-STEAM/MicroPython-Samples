import _thread

class task(object):
    lock = _thread.allocate_lock()

    def __init__(self, event=(lambda args: print('task running')), args=None):
        self.alive = False
        self.set_cb(event, args)

    def set_cb(self, event, args):
        self.event = event
        self.args = args

    def run(self):
        if task.lock.acquire():
            while self.alive:
                self.event(self.args)
            task.lock.release()
        _thread.exit()

    def stop(self):
        self.alive = False
        if task.lock.acquire():
            # print("stop")
            task.lock.release()

    def start(self):
        self.stop()
        self.alive = True
        if task.lock.acquire():
            # print("start")
            _thread.start_new_thread(self.run, ())
            task.lock.release()


if __name__ == "__main__":
    import time
    def unit_test(args):
        time.sleep(0.25)
        print('unit_test', args)
    tmp = task(unit_test, {'name': 'unit_test_0'})
    tmp.start()
    time.sleep(1)
    tmp.set_cb(unit_test, {'name': 'unit_test_1'})
    tmp.start()
    time.sleep(2)
    tmp.set_cb(unit_test, {'name': 'unit_test_2'})
    tmp.start()
    # time.sleep(3)
    tmp.stop()

