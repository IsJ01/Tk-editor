from tkinter.ttk import Treeview, Style
from tkinter import NW, END, Tk
from images import ImageDict


class WidgetsPanel(Tk):
    tk_el = {"Text": ["Label", "Entry", "Text", "Message"],
             "Buttons": ["Button", "Radiobutton", "Checkbutton", "Menubutton"],
             "Boxes": ["Listbox", "Spinbox"],
             "Containers": ["Canvas", "Frame", "LabelFrame"],
             "Other": ["Scale", "Scrollbar"]}

    ttk_el = {"Text": ["Label", "Entry"],
              "Buttons": ["Button", "Radiobutton", "Checkbutton", "Menubutton"],
              "Boxes": ["Spinbox", "Combobox"],
              "Containers": ["Frame", "LabelFrame", "Notebook"],
              "Other": ["Scale", "Scrollbar", "Treeview", "Separator", "Progressbar"]}

    def __init__(self, window):
        super().__init__()
        self.master_ = window
        style = Style(self)
        style.theme_use("default")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.sc_height = self.winfo_screenheight()
        self.sc_width = self.winfo_screenwidth()
        self.geometry(f"{int(self.sc_width / 100 * 15)}x{int(self.sc_height * 0.97)}+0+{int(self.sc_height * 0.022)}")
        self.treeView = Treeview(self)
        self.images = ImageDict(self)
        self.render(self.master_.menu.var.get())
        self.attributes('-toolwindow', True)
        self.resizable(width=False, height=False)
        self.title("Widgets panel")

    def on_closing(self):
        self.master_.menu.wid_var.set(False)
        self.destroy()

    def createTableMenu(self, args):
        self.master_.menu.createTableMenu(args)

    def render(self, mode: bool):
        if self.treeView:
            self.treeView.destroy()
        self.treeView = Treeview(master=self, show='tree headings')
        self.treeView.heading("#0", text=f'Widgets ({["Tk", "Ttk"][mode]})', anchor=NW)
        elements = self.tk_el if not mode else self.ttk_el
        num = 1
        tag = "ttk" if mode else ""
        for k, v in elements.items():
            parent = list(elements).index(k) + 100
            self.treeView.insert("", iid=parent, index=END, text=k, open=True, tags="tree")
            for wid in v:
                self.treeView.insert(parent, iid=num, index=END, text=f"   {wid}", tags=tag, image=self.images[wid])
                num += 1
        self.treeView.place(y=0, height=self.sc_height, width=self.sc_width / 100 * 15)
        self.treeView.bind('<Button-3>', self.createTableMenu)
        self.treeView.bind('<<TreeviewSelect>>', self.master_.getWidget)
