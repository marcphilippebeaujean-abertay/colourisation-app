from tkinter import *


class MiniPredDisplay(Frame):
    def __init__(self, master, position=(0.5, 0.5), frame_dim=100):
        Frame.__init__(self, master, width=600, height=300)
        self.image = None
        self.canvas = Canvas(self.master,
                             relief='solid',
                             bd=2,
                             width=frame_dim,
                             height=frame_dim)
        self.canvas.place(anchor=N,
                          relx=position[0],
                          rely=position[1])
        self.img_label = Label(master=self.canvas)
        self.img_label.place(relx=0.5, rely=0.25, anchor=N)
        self.img_label.configure(image=self.image)
        self.reveal_text = Label(self.master, text='Testing')
        self.reveal_text.place(anchor=N,
                               relx=position[0],
                               rely=position[1]-0.08)

    def update_from_pred(self, pred):
        img, _ = pred.generate_output((50, 50))
        self.image = img
        self.reveal_text.configure(text=pred.model_name)
        self.img_label.configure(image=self.image)

    def reset_display(self):
        self.image = None
        self.reveal_text.configure(text='')
