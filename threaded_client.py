from first_page import ImageUploadPageManager
from second_page import SecondPageWidgetManager
from queue import Queue
from network_prediction import PredictionThread
from tkinter import *


class ThreadedClient:
    def __init__(self, master):
        # root tkinter UI
        self.master = master
        # queue used to manage threading messages
        self.input_queue = Queue()
        self.output_queue = Queue()
        # setup widget manager
        self.page_1 = ImageUploadPageManager(self.master,
                                             self.input_queue)
        self.page_1.pack()
        self.page_2 = SecondPageWidgetManager(master)
        # create threads setup
        self.pred_thread = PredictionThread(self.input_queue,
                                            self.output_queue)
        self.pred_thread.daemon = True
        self.pred_thread.start()
        # create periodic call that checks for predictions
        self.periodic_call()
        b = Button(master, text="Toggle Page", command=self.switch_page)
        b.pack()

    def periodic_call(self):
        if self.output_queue.empty() is False:
            prediction, chrom = self.output_queue.get()
            self.page_1.output_img.on_output_generated(prediction, chrom)
        self.master.after(200, self.periodic_call)

    def end_application(self):
        self.pred_thread.running = False

    def switch_page(self):
        self.page_1.on_page_switch()
        self.page_2.on_page_switch()


