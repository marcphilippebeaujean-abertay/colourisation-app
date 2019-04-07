from tkinter import *
from first_page import PageManager


class SecondPageWidgetManager(PageManager):
    def __init__(self, master):
        super().__init__(master, False)
        self.master = master

