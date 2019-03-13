from tkinter import *
from tkinter.filedialog import askopenfilename
import os


class WidgetManager(Frame):
    def __init__(self, master=None, upload_logo='upload_logo.png'):
        Frame.__init__(self, master)
        self.master = master
        self.upload_logo = PhotoImage(file=os.path.join(os.getcwd(), upload_logo))
        self.upload_logo = self.upload_logo.subsample(3, 3)
        self.error_msg = Label(self.master, text="", fg="red")
        self.error_msg.pack(side=BOTTOM)
        self.output_img = None
        self.source_img = None
        self.create_widget_layout()

    def create_widget_layout(self):
        # generate canvas to hold images
        upload_canvas = self.create_placeholder_canvas(E)
        #output_canvas = self.create_placeholder_canvas(W)
        # create upload image stock
        self.source_img = Label(upload_canvas, image=self.upload_logo)
        self.source_img.configure(image=self.upload_logo)
        self.source_img.place(relx=0.5, rely=0.5, anchor=CENTER)
        # add button for configuring images
        choose_file = Button(upload_canvas,
                             text='Choose File',
                             command=lambda: self.load_img())
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
                                              ("All Files", "*.*")),
                                   title='Choose an Image')
        if len(img_path) is 0:
            return
        if os.path.isfile(img_path):
            try:
                self.upload_logo = PhotoImage(file=img_path)
                self.source_img.configure(image=self.upload_logo)
            except:
                self.error_msg.configure(text="Failed to load File!")


