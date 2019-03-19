from window_def import Window
from widget_manager import WidgetManager
from queue import Queue
from network_prediction import PredictionThread


class ThreadedClient:
    def __init__(self, master):
        # root tkinter UI
        self.master = master
        # queue used to manage threading messages
        self.input_queue = Queue()
        self.output_queue = Queue()
        # setup widget manager
        self.window = Window(master)
        self.widgets = WidgetManager(master,
                                     self.input_queue)
        # create threads setup
        self.pred_thread = PredictionThread(self.input_queue,
                                            self.output_queue)
        self.pred_thread.start()
        # create periodic call that checks for predictions
        self.periodic_call()

    def periodic_call(self):
        if self.output_queue.empty() is False:
            prediction = self.output_queue.get()
            self.widgets.output_img.update_img(prediction)
        if not self.pred_thread.running:
            import sys
            sys.exit(1)
        self.master.after(200, self.periodic_call)

    def end_application(self):
        self.pred_thread.running = False


