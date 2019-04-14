from tkinter import *
import os


class ToggleButton(Label):
    def __init__(self, target_page, master=None, client=None, active=False, **kwargs):
        Label.__init__(self, master, **kwargs)
        self.active = active
        self.client = client
        self.images = [PhotoImage(file=os.path.join(os.getcwd(),
                                                    'images',
                                                    'icons',
                                                    'page_select.png')),
                       PhotoImage(file=os.path.join(os.getcwd(),
                                                    'images',
                                                    'icons',
                                                    'page_not_selected.png'))]
        self.update_icon()
        self.configure(borderwidth=0,
                       highlightbackground='white',
                       highlightthickness=0,
                       padx=0, pady=0)
        self.bind("<Button-1>", self.on_clicked)
        self.target_page = target_page

    def on_clicked(self, e):
        if self.active:
            return
        else:
            self.client.switch_page(self.target_page)

    def update_icon(self):
        if self.active:
            self.configure(image=self.images[0])
        else:
            self.configure(image=self.images[1])

