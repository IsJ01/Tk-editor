import tkinter
from tkinter.ttk import Treeview, Style
from tkinter import NW, END, Tk, Menu


class WindowPanel(Tk):

    def __init__(self, window):
        super().__init__()
        self.master_ = window
        self.contextMenu = None
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.sc_height = self.winfo_screenheight()
        self.sc_width = self.winfo_screenwidth()
        self.geometry(f"{int(self.sc_width / 100 * 15)}x{int(self.sc_height * 0.2)}+0+{int(self.sc_height * 0.722)}")
        self.treeView = Treeview(self)
        self.render()
        self.resizable(True, False)
        self.attributes('-toolwindow', True)
        self.title("Window panel")
        self.bind('<Control-z>', self.master_.undo)
        self.bind('<Control-Shift-Z>', self.master_.redo)
        self.bind('<Control-x>', self.master_.cut)
        self.bind('<Control-c>', self.master_.copy)
        self.bind('<Control-v>', self.master_.paste)
        self.bind('<Delete>', self.master_.delete)

    def on_closing(self):
        self.master_.menu.win_panel_var.set(False)
        self.destroy()

    def createWidgetMenu(self, args):
        if self.contextMenu:
            self.clear()
        if self.master_.window.current_obj:
            self.master_.addPropertyFields(self.master_.window.current_obj)
        else:
            return
        self.contextMenu = Menu(master=self, tearoff=0)
        commands = [("Cut", self.master_.cut), ("Copy", self.master_.copy),
                    ("Paste", self.master_.paste),
                    ("Delete", self.master_.delete)]

        for t, c in commands:
            self.contextMenu.add_command(label=t, command=c)
        x, y = args.x_root, args.y_root
        self.contextMenu.post(x, y)
        self.master_.win_panel.render() if self.master_.menu.win_panel_var.get() else ...

    def clear(self, *args):
        for w in self.winfo_children():
            if w.__class__ == Menu:
                w.destroy()

    def tree_select(self, args):
        self.clear()
        item = self.treeView.item(self.treeView.selection())
        self.master_.window.current_obj = self.master_.window.children[item["text"]]\
            if "." not in item["text"] and "Widget" not in item["text"] else self.master_.window
        self.master_.addPropertyFields(self.master_.window.current_obj)

    def addItems(self, item: tkinter.Widget, name, parent):
        if item == self.master_.window:
            parent = 1
            self.treeView.insert("", iid=parent, index=END, text=self.master_.type,
                                 values=(self.master_.window.title()), open=True)
        else:
            iid = int(str(parent) + str(item.master.winfo_children().index(item)))
            self.treeView.insert(parent, iid=iid, index=END, text=name,
                                 values=(item.widgetName), open=True)
            parent = iid
        if not item.winfo_children():
            return
        for child in item.children:
            self.addItems(item.children[child], child, parent) if item.children[child].place_info() else ...

    def render(self):
        if self.treeView:
            self.treeView.destroy()
        self.treeView = Treeview(master=self, show='tree headings', columns=("name"))
        self.treeView.column("#0", width=15, anchor="c")
        self.treeView.column("name", width=15, anchor="c")
        self.treeView.heading("#0", text='object')
        self.treeView.heading("name", text='name')
        self.addItems(self.master_.window, "", "")
        self.treeView.pack(fill="both")
        self.treeView.bind('<<TreeviewSelect>>', self.tree_select)
        self.treeView.bind('<Button-3>', self.createWidgetMenu)
        self.treeView.bind("<FocusOut>", self.clear)
