from tkinter import PhotoImage


class ImageDict(dict):
    def __init__(self, win):
        super().__init__()
        self.images = {"Label": PhotoImage(master=win.treeView, file="data/Label.png"),
                       "Radiobutton": PhotoImage(master=win.treeView, file="data/Radiobutton.png"),
                       "Entry": PhotoImage(master=win.treeView, file="data/Entry.png"),
                       "Text": PhotoImage(master=win.treeView, file="data/Text.png"),
                       "Message": PhotoImage(master=win.treeView, file="data/Message.png"),
                       "Button": PhotoImage(master=win.treeView, file="data/Button.png"),
                       "Checkbutton": PhotoImage(master=win.treeView, file="data/Checkbutton.png"),
                       "Menubutton": PhotoImage(master=win.treeView, file="data/Menubutton.png"),
                       "Listbox": PhotoImage(master=win.treeView, file="data/Listbox.png"),
                       "Spinbox": PhotoImage(master=win.treeView, file="data/Spinbox.png"),
                       "Combobox": PhotoImage(master=win.treeView, file="data/Combobox.png"),
                       "Canvas": PhotoImage(master=win.treeView, file="data/Canvas.png"),
                       "Frame": PhotoImage(master=win.treeView, file="data/Frame.png"),
                       "LabelFrame": PhotoImage(master=win.treeView, file="data/LabelFrame.png"),
                       "Notebook": PhotoImage(master=win.treeView, file="data/Notebook.png"),
                       "Scale": PhotoImage(master=win.treeView, file="data/Scale.png"),
                       "Scrollbar": PhotoImage(master=win.treeView, file="data/Scrollbar.png"),
                       "Treeview": PhotoImage(master=win.treeView, file="data/Treeview.png"),
                       "Separator": PhotoImage(master=win.treeView, file="data/Separator.png"),
                       "Progressbar": PhotoImage(master=win.treeView, file="data/Progressbar.png")
                       }

    def __getitem__(self, item):
        if item in self.images:
            return self.images[item]
        else:
            return ''
