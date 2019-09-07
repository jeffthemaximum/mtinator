import threading
import time

from application import app


class ServiceThread:
    def __init__(self, func, interval=5):
        self.func = func
        self.interval = interval
        self.kill = threading.Event()

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        with app.app_context():
            while not self.kill.is_set():
                self.func()
                time.sleep(self.interval)
