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
        self.page = ImageUploadPageManager(self.master,
                                           self.input_queue,
                                           self)
        self.page.place(relx=0.5,
                        rely=0.1,
                        anchor=N)
        self.cur_page = 0
        # create threads setup
        self.pred_thread = PredictionThread(self.input_queue,
                                            self.output_queue)
        self.pred_thread.daemon = True
        self.pred_thread.start()
        # create periodic call that checks for predictions
        self.periodic_call()

    def periodic_call(self):
        if self.output_queue.empty() is False:
            prediction, chrom = self.output_queue.get()
            self.page.output_img.on_output_generated(prediction, chrom)
        self.master.after(200, self.periodic_call)

    def end_application(self):
        self.pred_thread.running = False

    def switch_page(self):
        self.page.destroy()
        new_frame = None
        if self.cur_page is 1:
            new_frame = ImageUploadPageManager(self.master,
                                               self.input_queue,
                                               self)
            self.cur_page = 0
        else:
            new_frame = ImageUploadPageManager(self.master,
                                               self.input_queue,
                                               self)
            self.cur_page = 1
        self.page = new_frame
        self.page.place(relx=0.5,
                        rely=0.1,
                        anchor=N)


