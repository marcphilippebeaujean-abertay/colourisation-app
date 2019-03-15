from tkinter import *
from tkinter.filedialog import askopenfilename
from img_processing import get_pre_processed_img
from PIL import ImageTk, Image
import os


class WidgetManager(Frame):
    def __init__(self, master=None, frame_dimension=300):
        Frame.__init__(self, master)
        self.master = master
        # define default widget images
        self.source_img = PhotoImage(file=os.path.join(os.getcwd(), 'upload_logo.png'))
        self.output_img = PhotoImage(file=os.path.join(os.getcwd(), 'eye_logo.png'))
        # initialise label members
        self.error_msg = Label(self.master, text='', fg='red', font=('Helvetica', 20))
        self.error_msg.pack(side=BOTTOM)
        self.input_label = None
        self.output_label = None
        # generate initial widget layout
        self.frame_dim = frame_dimension
        self.create_widget_layout()
        # define state management variables
        self.update_loading_seq = None

    def create_widget_layout(self):
        # generate canvas to hold images
        upload_canvas, self.input_label = self.create_placeholder_canvas(E, self.source_img)
        _, self.output_label = self.create_placeholder_canvas(W, self.output_img)
        # add button for configuring images
        choose_file = Button(upload_canvas,
                             text='Choose File',
                             command=lambda: self.load_img())
        choose_file.place(relx=0.5, rely=0.9, anchor=N)

    def create_placeholder_canvas(self, anchor, default_image):
        # generate canvas to hold images
        canvas = Canvas(self.master,
                        relief='solid',
                        bd=2,
                        width=self.frame_dim,
                        height=self.frame_dim)
        canvas.place(relx=0.5, rely=0.47, anchor=anchor)
        # configure placeholder image
        label_placeholder = Label(canvas, image=default_image)
        label_placeholder.configure(image=default_image)
        label_placeholder.place(relx=0.5, rely=0.5, anchor=CENTER)
        return canvas, label_placeholder

    def load_img(self):
        img_path = askopenfilename(initialdir=os.getcwd(),
                                   filetypes=(("PNG File", "*.png"),
                                              ("All Files", "*.*")),
                                   title='Choose an Image')
        if len(img_path) is 0:
            return
        if os.path.isfile(img_path):
            try:
                # adjust image to fit to canvas
                img = get_pre_processed_img(img_path,
                                            (self.frame_dim-5))
                img = Image.fromarray(img)
                # apply widget updates
                self.source_img = ImageTk.PhotoImage(img)
                self.input_label.configure(image=self.source_img)
                self.error_msg.configure(text='')
                # start loading animation
                self.update_loading_seq = self.init_loading().__next__
                self.master.after(10, self.update_loading_seq)
            except:
                self.error_msg.configure(text='Failed to load Image!')

    def init_loading(self):
        angle = 359
        loading_img = Image.open(os.path.join(os.getcwd(), 'loading_img.png'))
        while True:
            self.output_img = ImageTk.PhotoImage(loading_img.rotate(angle))
            self.output_label.configure(image=self.output_img)
            if angle > 260:
                self.master.after_idle(self.update_loading_seq)
            yield
            angle -= 1
            angle %= 360

