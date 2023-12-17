import tkinter
from tkinter import ttk
from tkinter.simpledialog import Dialog


class ObjDialog(Dialog):

    def __init__(self, parent, title=None):
        sc_height = parent.winfo_screenheight()
        sc_width = parent.winfo_screenwidth()
        self.properties = {"Window": {"type": "tkinter.Tk", "width": sc_width * 0.65, "height": sc_height * 0.884,
                                      "x": sc_width * 0.15, "y": sc_height * 0.022},
                           "Dialog (simple)": {"type": "simpledialog.Dialog", "width": sc_width * 0.15625,
                                               "height": sc_height * 0.222,
                                               "x": (sc_width - sc_width * 0.15625) / 2,
                                               "y": (sc_height - sc_height * 0.222) / 2},
                           "Dialog (common)": {"type": "commondialog.Dialog",
                                               "width": sc_width * 0.15625, "height": sc_height * 0.222,
                                               "x": (sc_width - sc_width * 0.15625) / 2,
                                               "y": (sc_height - sc_height * 0.222) / 2},
                           "Widget": {"type": "Widget",
                                      "width": sc_width * 0.09375, "height": sc_height * 0.111,
                                      "x": (sc_width - sc_width * 0.09375) / 2,
                                      "y": (sc_height - sc_height * 0.111) / 2}}
        super().__init__(parent, title)

    def body(self, master):
        self.geometry(f"200x200+675+350")
        self.resizable(False, False)
        self.listbox = tkinter.Listbox(master=self, background='SystemWindow',
                                       foreground='SystemButtonText', font='TkDefaultFont')
        self.listbox.insert("end", *["Window", "Dialog (simple)", "Dialog (common)", "Widget"])
        self.listbox.bind("<Double-1>", self.ok)
        self.listbox.place(x=2, y=0, width=156, height=164)
        self.ttk_button = ttk.Button(master=self, text='Create', underline=-1, command=self.ok)
        self.ttk_button.place(x=2, y=169, width=76, height=25)
        self.ttk_button_2 = ttk.Button(master=self, text='Cancel', underline=-1,
                                       command=self.destroy)
        self.ttk_button_2.place(x=83, y=169, width=76, height=25)
        return self.listbox

    def apply(self):
        self.result = self.getresult()

    def getresult(self):
        return (self.listbox.get(self.listbox.curselection()),
                self.properties[self.listbox.get(self.listbox.curselection())])

    def validate(self):
        try:
            self.result = self.getresult()
            return 1
        except tkinter.TclError:
            return 0

    def buttonbox(self):
        pass
