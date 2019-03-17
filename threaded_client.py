from network_prediction import generate_prediction
from window_def import Window
from widget_manager import WidgetManager
from queue import Queue
from threading import Thread
from time import sleep


class ThreadedClient:
    def __init__(self, master):
        # root tkinter UI
        self.master = master
        # queue used to manage theading messages
        self.queue = Queue()
        # setup widget manager
        self.window = Window(master)
        self.ui_mgr = WidgetManager(master, self.queue)
        # create threads setup
        self.running = True
        self.thread1 = Thread(target=self.worker_thread1)
        self.thread1.start()

    def worker_thread1(self):
        while self.running:
            # check if queue contains a new prediction to make
            try:
                img = self.queue.get()
                generate_prediction(input_img=img)
            except IndexError:
                sleep(0.1)

    def end_application(self):
        self.running = False


