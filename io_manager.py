from pg_one_mgr import ImageUploadPageManager
from pg_two_mgr import SecondPageWidgetManager
from queue import Queue
from prediction_thread import PredictionThread
from tkinter import *
from toggle_btn import ToggleButton
from brightness_clr_toggle import ClrIntensityToggle


class IOManager:
    def __init__(self, master):
        # root tkinter UI
        self.master = master
        # queue used to manage threading messages
        self.input_queue = Queue()
        self.output_queue = Queue()
        # initialise label members
        self.notification_label = Label(master,
                                        text='',
                                        fg='green',
                                        font=('Helvetica', 20))
        self.notification_label.place(anchor=N, relx=0.5, rely=0.9)
        # setup widget manager
        self.page = ImageUploadPageManager(self.master,
                                           self.input_queue,
                                           self)
        self.page.place(relx=0.5,
                        rely=0.1,
                        anchor=N)
        self.cur_page_id = 0
        # create threads setup
        self.pred_thread = PredictionThread(self.input_queue,
                                            self.output_queue)
        self.pred_thread.daemon = True
        self.pred_thread.start()
        # create periodic call that checks for predictions
        self.periodic_call()
        # toggle button used to switch between pages
        toggle_a = ToggleButton(master, client=self, active=True)
        toggle_a.place(relx=0.45, rely=0.02, anchor=N)
        toggle_b = ToggleButton(master, client=self, active=False)
        toggle_b.place(relx=0.55, rely=0.02, anchor=N)
        self.toggle_btns = [toggle_a, toggle_b]
        self.intensity_toggle = ClrIntensityToggle(master, self)

    def periodic_call(self):
        if self.output_queue.empty() is False:
            prediction = self.output_queue.get()
            self.page.on_prediction_received(prediction)
            if self.cur_page_id is 0:
                self.intensity_toggle.show_btns()
        self.master.after(200, self.periodic_call)

    def end_application(self):
        self.pred_thread.running = False

    def switch_page(self):
        if self.page.is_pred_pending:
            self.notification_update('Please wait for process to finish!', True)
            return
        for btn in self.toggle_btns:
            btn.active = not btn.active
            btn.update_icon()
        self.notification_label.configure(text='')
        self.page.destroy()
        new_frame = None
        if self.cur_page_id is 1:
            new_frame = ImageUploadPageManager(self.master,
                                               self.input_queue,
                                               self)
            self.cur_page_id = 0
        else:
            new_frame = SecondPageWidgetManager(self.master,
                                                self,
                                                self.input_queue,
                                                self.output_queue)
            self.cur_page_id = 1
            self.intensity_toggle.hide_buttons()
        self.pred_thread.multi_pred = (self.cur_page_id == 1)
        self.page = new_frame
        self.page.place(relx=0.5, rely=0.1, anchor=N)

    def notification_update(self, text, is_error=False):
        color = 'red' if is_error else 'green'
        self.notification_label.configure(fg=color, text=text)
