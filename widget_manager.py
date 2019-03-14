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
        self.upload_logo = PhotoImage(file=os.path.join(os.getcwd(), 'upload_logo.png'))
        self.upload_logo = self.upload_logo.subsample(3, 3)
        self.output_logo = PhotoImage(file=os.path.join(os.getcwd(), 'eye_logo.png'))
        self.output_logo = self.output_logo.subsample(3, 3)
        # initialise label members
        self.error_msg = Label(self.master, text="", fg="red", font=("Helvetica", 20))
        self.error_msg.pack(side=BOTTOM)
        self.output_img = None
        self.input_img = None
        # generate initial widget layout
        self.frame_dim = frame_dimension
        self.create_widget_layout()

    def create_widget_layout(self):
        # generate canvas to hold images
        upload_canvas, self.input_img = self.create_placeholder_canvas(E, self.upload_logo)
        _, self.output_img = self.create_placeholder_canvas(W, self.output_logo)
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
        canvas.place(relx=0.5, rely=0.5, anchor=anchor)
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
            # TODO: Add for final app to prevent users from uploading invalid files
            #try:
            img, _ = get_pre_processed_img(img_path, (self.frame_dim-5))
            img = Image.fromarray(img)
            self.upload_logo = ImageTk.PhotoImage(img)
            self.input_img.configure(image=self.upload_logo)
            #except:
            #    self.error_msg.configure(text='Failed to load File!')


