from pg_one_mgr import ImageUploadPageManager
from pg_two_mgr import SecondPageWidgetManager
from pg_three_mgr import SetPredictionManager
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
        self.toggle_btns = []
        # toggle button used to switch between pages
        for i in range(3):
            active = True if i is 0 else False
            toggle_btn = ToggleButton(i, master, client=self, active=active)
            toggle_btn.place(relx=0.4+i*0.1, rely=0.02, anchor=N)
            self.toggle_btns.append(toggle_btn)
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

    def switch_page(self, target_page):
        if self.page.is_pred_pending:
            self.notification_update('Please wait for process to finish!', True)
            return
        for btn in self.toggle_btns:
            btn.active = not btn.active
            btn.update_icon()
        self.notification_label.configure(text='')
        self.page.destroy()
        new_frame = None
        self.cur_page_id = target_page
        if self.cur_page_id is 0:
            new_frame = ImageUploadPageManager(self.master,
                                               self.input_queue,
                                               self)
        elif self.cur_page_id is 1:
            new_frame = SecondPageWidgetManager(self.master,
                                                self,
                                                self.input_queue,
                                                self.output_queue)
        else:
            new_frame = SetPredictionManager(self.master,
                                             self,
                                             self.input_queue)
        for btn in self.toggle_btns:
            btn.active = (self.cur_page_id == btn.target_page)
            btn.update_icon()
        if self.cur_page_id != 0:
            self.intensity_toggle.hide_buttons()
        self.page = new_frame
        self.pred_thread.pred_mode = self.page.pred_mode
        self.page.place(relx=0.5, rely=0.1, anchor=N)

    def notification_update(self, text, is_error=False):
        color = 'red' if is_error else 'green'
        self.notification_label.configure(fg=color, text=text)
