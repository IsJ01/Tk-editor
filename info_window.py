from tkinter import *


class Info(Tk):
    def __init__(self):
        super().__init__()
        self.geometry('200x50')
        self.wm_title('About program')
        self.getInfo()

    def getInfo(self):
        self.label = Label(master=self, text='Tkinter forms editor v 2.0')
        self.label.place(x=(200 - self.label.winfo_reqwidth()) // 2, y=10)
        self.label_2 = Label(master=self)
