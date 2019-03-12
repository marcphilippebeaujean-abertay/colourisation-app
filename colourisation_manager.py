from tkinter import *
from PIL import Image, ImageDraw, ImageTk


class ColourisationManager:
    def __init__(self, master=None):
        self.master = master
        self.create_widget_layout()
        self.source_img = None
        self.output_img = None

    def create_widget_layout(self):
        # generate canvas to hold images
        upload_canvas, self.source_img = self.create_placeholder_canvas(E)
        _, self.output_img = self.create_placeholder_canvas(W)
        # add button for configuring images
        choose_file = Button(upload_canvas, text='Choose File')
        choose_file.pack()
        choose_file.place(relx=0.5, rely=0.9, anchor=N)

    def create_placeholder_canvas(self, anchor):
        # generate canvas to hold images
        canvas = Canvas(self.master, bg='#eaeaea')
        # create vanilla background image
        blank_source = Image.new('RGBA', (200, 200), "#ffffff")
        blank = ImageTk.PhotoImage(blank_source)
        # configure image and assign it to canvas
        source_img = Label(canvas, image=blank)
        source_img.configure(image=blank)
        # expand and center canvas
        canvas.pack(expand=0)
        canvas.place(relx=0.5, rely=0.5, anchor=anchor)
        return canvas, source_img
