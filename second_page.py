from tkinter import *
from first_page import PageManager


class SecondPageWidgetManager(PageManager):
    def __init__(self, master, client):
        super().__init__(master, False, client)
        self.master = master

