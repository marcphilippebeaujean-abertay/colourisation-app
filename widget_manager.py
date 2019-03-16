from tkinter import *
from tkinter.filedialog import askopenfilename
from img_processing import get_pre_processed_img
from image_frame import ImageFrame
from PIL import ImageTk, Image
import os


class WidgetManager(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        # define default widget images
        self.source_img = ImageFrame(self.master,
                                     E,
                                     os.path.join(os.getcwd(), 'upload_logo.png'))
        self.output_img = ImageFrame(self.master,
                                     W,
                                     os.path.join(os.getcwd(), 'eye_logo.png'))
        # initialise label members
        self.error_msg = Label(self.master,
                               text='',
                               fg='red',
                               font=('Helvetica', 20))
        self.error_msg.pack(side=BOTTOM)
        # generate initial widget layout
        self.create_widget_layout()

    def create_widget_layout(self):
        # add button for configuring images
        choose_file = Button(self.source_img.canvas,
                             text='Choose File',
                             command=lambda: self.load_img())
        choose_file.place(relx=0.5,
                          rely=0.9,
                          anchor=N)

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
                                            (self.source_img.frame_dim-5))
                img = Image.fromarray(img)
                # apply widget updates
                self.source_img.update_img(ImageTk.PhotoImage(img))
                self.error_msg.configure(text='')
                # start loading animation
                self.output_img.init_animation(self.output_img.loading_anim().__next__)
            except:
                self.error_msg.configure(text='Failed to load Image!')

