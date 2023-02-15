import threading

class ResettableTimer:
    def __init__(self, interval, callback):
        self.interval = interval
        self.callback = callback
        self.timer = None

    def start(self):
        if self.timer is None:
            self.timer = threading.Timer(self.interval, self.callback)
            self.timer.start()

    def restart(self):
        if self.timer is not None:
            self.timer.cancel()
        self.timer = threading.Timer(self.interval, self.callback)
        self.timer.start()  

    def cancel(self):
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None