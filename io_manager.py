from pg_one_mgr import ImageUploadPageManager
from pg_two_mgr import SecondPageWidgetManager
from queue import Queue
from prediction_thread import PredictionThread
from tkinter import *


class IOManager:
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
            prediction = self.output_queue.get()
            self.page.on_prediction_received(prediction)
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
            new_frame = SecondPageWidgetManager(self.master,
                                                self,
                                                self.input_queue,
                                                self.output_queue)
            self.cur_page = 1
        self.pred_thread.multi_pred = (self.cur_page == 1)
        self.page = new_frame
        self.page.place(relx=0.5,
                        rely=0.1,
                        anchor=N)


