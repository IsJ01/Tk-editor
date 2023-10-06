import tkinter
from tkinter import ttk


class Window(tkinter.Tk):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.title('tk')
        self.style = ttk.Style(self)
        self.style.theme_use('vista')
        self.geometry('300x200+379+51')
        self.ttk_label = ttk.Label(border='1', relief='flat', text='Логин', underline='-1')
        self.ttk_label.place(x=26, y=10, width=40, height=19)
        self.ttk_label_2 = ttk.Label(border='1', relief='flat', text='Пароль', underline='-1')
        self.ttk_label_2.place(x=31, y=59, width=50, height=19)
        self.ttk_entry = ttk.Entry(font='TkTextFont')
        self.ttk_entry.place(x=114, y=13, width=126, height=21)
        self.ttk_entry_2 = ttk.Entry(font='TkTextFont')
        self.ttk_entry_2.place(x=115, y=63, width=126, height=21)
        self.ttk_button = ttk.Button(text='Войти', underline='-1')
        self.ttk_button.place(x=39, y=104, width=76, height=25)