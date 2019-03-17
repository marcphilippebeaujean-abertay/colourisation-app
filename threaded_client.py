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
        self.input_queue = Queue()
        self.output_queue = Queue()
        # setup widget manager
        self.window = Window(master)
        self.widgets = WidgetManager(master, self.input_queue)
        # create threads setup
        self.running = True
        self.thread1 = Thread(target=self.worker_thread1)
        self.thread1.start()
        # create periodic call that checks for predictions
        self.periodic_call()

    def worker_thread1(self):
        while self.running:
            # check if queue contains a new prediction to make
            if self.input_queue.empty() is False:
                img = self.input_queue.get()
                pred = generate_prediction(input_img=img)
                self.output_queue.put(pred)
            else:
                sleep(0.1)

    def periodic_call(self):
        if self.output_queue.empty() is False:
            prediction = self.output_queue.get()
            print('got a prediction from the output queue!')
            self.widgets.update_prediction_img()
        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            import sys
            sys.exit(1)
        self.master.after(200, self.periodic_call)

    def end_application(self):
        self.running = False


