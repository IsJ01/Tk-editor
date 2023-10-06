from tkinter import Tk, Menu, BooleanVar, TclError, PhotoImage
import sys


class ToolBar(Tk):

    def __init__(self, master):
        super().__init__()
        self.menu = None
        self.win_var = BooleanVar(value=True)
        self.var = BooleanVar(value=False)
        self.conf_var = BooleanVar(value=True)
        self.wid_var = BooleanVar(value=True)
        self.master_ = master
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        width = self.winfo_screenwidth()
        self.geometry(f"{width}x{0}+0+0")
        self.attributes("-toolwindow", True)
        self.createMenu()
        self.resizable(width=False, height=False)
        self.title("Tkinter Editor")

    def on_closing(self):
        for win in [self.master_.window, self.master_.conf_panel, self.master_.wid_panel, self]:
            try:
                win.destroy()
            except TclError:
                pass

    def createMenu(self):
        # создание меню
        self.menu = Menu(master=self)
        self.config(menu=self.menu)
        # создание меню файлов
        self.createFileMenu()
        self.createEditMenu()
        self.createViewMenu()
        self.createHelpMenu()

    def createFileMenu(self):
        self.file_menu = Menu(master=self, tearoff=0)
        # добавление команд к элементам меню
        self.file_menu.add_command(label='Open', command=self.master_.open)
        self.file_menu.add_command(label='Save', command=self.master_.save)
        self.file_menu.add_command(label='Generate', command=self.master_.generate)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Exit', command=sys.exit)
        self.menu.add_cascade(label='File', menu=self.file_menu)

    def createEditMenu(self):
        self.edit_menu = Menu(master=self, tearoff=0)
        # добавление команд к элементам меню
        self.edit_menu.add_command(label="Undo", command=self.master_.undo)
        self.edit_menu.add_command(label="Redo", command=self.master_.redo)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=self.master_.cut)
        self.edit_menu.add_command(label="Copy", command=self.master_.copy)
        self.edit_menu.add_command(label="Paste", command=self.master_.paste)
        self.edit_menu.add_command(label="Delete", command=self.master_.delete)
        self.menu.add_cascade(label='Edit', menu=self.edit_menu)

    def createViewMenu(self):
        self.view_menu = Menu(master=self, tearoff=0)
        # добавление команд к элементам меню
        self.view_wid_menu = Menu(master=self, tearoff=0)
        self.view_wid_menu.add_radiobutton(label="Tk", variable=self.var, value=False,
                                           command=self.master_.setMode)
        self.view_wid_menu.add_radiobutton(label="Ttk", variable=self.var, value=True,
                                           command=self.master_.setMode)

        self.view_menu.add_checkbutton(label="Window", variable=self.win_var,
                                       command=self.master_.win_mode)
        self.view_menu.add_checkbutton(label="Configurate panel", variable=self.conf_var,
                                       command=self.master_.conf_mode)
        self.view_menu.add_checkbutton(label="Widgets panel", variable=self.wid_var,
                                       command=self.master_.wid_mode)
        self.view_menu.add_cascade(label="Widget panel", menu=self.view_wid_menu)
        self.menu.add_cascade(label='View', menu=self.view_menu)

    def createHelpMenu(self):
        self.help_menu = Menu(master=self, tearoff=0)
        # добавление команд к элементам меню
        self.help_menu.add_command(label='About program', command=self.master_.get_info)
        self.menu.add_cascade(label='Help', menu=self.help_menu)

    def createTableMenu(self, args):
        treeMenu = Menu(master=self, tearoff=0)
        treeMenu.add_radiobutton(label="Tk", variable=self.var,
                                 value=False, command=self.master_.setMode)
        treeMenu.add_radiobutton(label="Ttk", variable=self.var,
                                 value=True, command=self.master_.setMode)
        x, y = args.x_root, args.y_root
        treeMenu.post(x, y)
