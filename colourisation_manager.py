from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import os


class ColourisationManager(Frame):
    def __init__(self, master=None):
        self.master = master
        self.create_widget_layout()
        self.source_img = Label(self.master)
        self.source_img.pack(side=LEFT)
        self.output_img = Label(self.master)

    def create_widget_layout(self):
        # generate canvas to hold images
        upload_canvas = self.create_placeholder_canvas(E)
        output_canvas = self.create_placeholder_canvas(W)
        # add button for configuring images
        choose_file = Button(upload_canvas,
                             text='Choose File',
                             command=lambda: self.load_img())
        choose_file.pack()
        choose_file.place(relx=0.5, rely=0.9, anchor=N)

    def create_placeholder_canvas(self, anchor):
        # generate canvas to hold images
        canvas = Canvas(self.master, bg='#eaeaea')
        # expand and center canvas
        canvas.pack(expand=0)
        canvas.place(relx=0.5, rely=0.5, anchor=anchor)
        return canvas

    def load_img(self):
        img_path = askopenfilename(initialdir=os.getcwd(),
                                   filetypes=(("PNG File", "*.png"),
                                              ("JPEG File", "*.jpeg")),
                                   title="Choose an Image")
        if len(img_path) is 0:
            return
        if os.path.isfile(img_path):
            with open(img_path, 'rb') as f:
                tk_img = ImageTk.PhotoImage(Image.open(f))
                self.source_img.configure(image=tk_img)
                self.source_img.configure.pack(side=LEFT, fill="both", expand="yes")

