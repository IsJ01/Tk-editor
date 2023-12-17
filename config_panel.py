from tkinter import (ttk, Tk, TclError, Label, Entry, Text, Message,
                     Canvas, Button, Radiobutton, Checkbutton, Menubutton, Scale,
                     Listbox, Spinbox, Scrollbar, Frame, LabelFrame)
from tkinter.colorchooser import askcolor


class ConfigPanel(Tk):
    widgets = []

    def __init__(self, master):
        super().__init__()
        self.master_ = master
        self.current_object = None
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.create_widgets_fields()
        self.sc_height = self.winfo_screenheight()
        self.sc_width = self.winfo_screenwidth()
        self.geometry(f"{int(self.sc_width / 100 * 17.4) + 22}x{int(self.sc_height * 0.97)}"
                      f"+{int(self.sc_width / 100 * 80 + 2)}+{int(self.sc_height * 0.022)}")
        self.panel_wigets = []
        self.createPanel()
        self.attributes('-toolwindow', True)
        self.resizable(width=False, height=False)
        self.bind('<Control-z>', self.master_.undo)
        self.bind('<Control-Shift-Z>', self.master_.redo)
        self.bind('<Delete>', self.master_.delete)
        self.bind("<Return>", self.focus_out)
        self.title("Configurate panel")
        self.bind("<Button-1>", self.click)

    def createPanel(self):
        self.panel = Canvas(master=self, relief="ridge", width=self.sc_width / 100 * 17.2, height=self.sc_height * 0.97,
                            borderwidth=2, scrollregion=(0, 0, 340, 900))
        self.scroll_c2 = Scrollbar(master=self, orient='vertical', command=self.panel.yview)
        self.scroll_c2.place(x=self.sc_width / 100 * 17.4 + 4, y=2, height=self.sc_height * 0.97)
        self.panel['yscrollcommand'] = self.scroll_c2.set
        self.panel.place(x=0, y=0)

    def click(self, event):
        if event.widget in [self.panel, self]:
            self.focus_set()

    def focus_out(self, *args):
        self.master_.apply()

    def on_closing(self):
        self.master_.menu.conf_var.set(False)
        self.destroy()

    def create_widgets_fields(self):
        widgets = [Label, Entry, Text, Message,
                   Button, Radiobutton, Checkbutton, Menubutton,
                   Listbox, Spinbox,
                   Canvas, Frame, LabelFrame,
                   Scrollbar, Scale,
                   ttk.Label, ttk.Entry,
                   ttk.Button, ttk.Radiobutton, ttk.Checkbutton, ttk.Menubutton,
                   ttk.Spinbox, ttk.Combobox,
                   ttk.Frame, ttk.Labelframe, ttk.Notebook,
                   ttk.Scale, ttk.Scrollbar, ttk.Treeview, ttk.Separator, ttk.Sizegrip, ttk.Progressbar]
        fields = ["widgetName", 'width', 'height', 'x', 'y', 'background', "activebackground",
                  'foreground', "activeforeground", 'cursor', 'border', 'relief', 'text', 'font', 'underline',
                  "orient"]
        self.values = {"cursor": ['arrow', 'circle', 'clock', 'cross', 'dotbox', 'exchange', 'fleur',
                                  'heart', 'man', 'mouse', 'pirate', 'plus', 'shuttle', 'sizing',
                                  'spider', 'spraycan', 'star', 'target', 'tcross', 'trek', 'watch'],
                       "relief": ["raised", "sunken", "flat", "ridge", "solid", "groove"],
                       "theme": ttk.Style().theme_names(),
                       "orient": ["vertical", "horizontal"]
                       }

        table_fields = {}
        for wid in widgets:
            end_fields = [fields[0]]
            for field in fields[1:]:
                self.wid = wid()
                try:
                    if ((wid in [Entry, ttk.Entry] and field == "text")
                            or (wid in [ttk.Combobox, ttk.Entry] and field == "background")):
                        raise TclError
                    self.wid[field]
                    end_fields.append(field)
                except TclError:
                    if field in ["x", "y", 'width', "height"]:
                        end_fields.append(field)
            table_fields[wid] = end_fields
        self.widgets = table_fields

    def get_property(self, property, widget):
        if property == "widgetName":
            return self.master_.get_normal_name(widget.widgetName)
        if property == "theme":
            return widget.style.theme_use()
        if property == "title":
            return widget.title()
        if property in ["x", "y", "width", "height"]:
            return eval(f"widget.winfo_{property}()")
        if property == "relief":
            return widget["relief"]
        else:
            return widget[property]

    @staticmethod
    def button_clicked(event):
        widget = list(event.widget.master.children.values())[1]
        text = askcolor(parent=widget)
        if not text[-1]:
            return
        widget.delete(0, "end")
        widget.insert(0, text[-1])

    def get_field(self, fields, master):
        if fields in ['cursor', 'relief', "theme", "orient"]:
            return [ttk.Combobox(master, values=self.values[fields])]
        if fields in ['width', 'height', 'x', 'y', 'border', "underline"]:
            return [ttk.Spinbox(master, from_=-10000, to=10000)]
        if fields in ['background', "activebackground", 'foreground', "activeforeground"]:
            entry = ttk.Entry(master)
            button = ttk.Button(master, text="...")
            button.bind("<Button-1>", self.button_clicked)
            button.bind("<FocusOut>", self.focus_out)
            return [entry, button]
        else:
            return [ttk.Entry(master)]

    def addPropertyFields(self, widget):
        # если объект выбран
        if not self.master_.window.new_obj:
            for fr in self.panel.winfo_children():
                for ch in fr.winfo_children():
                    ch.destroy()
                fr.destroy()
            self.master_.fields.clear()
            self.current_object = widget
            # в этом цикле панель очищается от старых виджетов
            # в данном словаре хранятся виджеты и свойства к ним
            # w - переменная в которой хранится название класса выбранного виджета
            w = widget.__class__
            # теперь в переменной properties хранятся все свойства
            if widget == self.master_.window:
                properties = ['width', 'height', 'x', 'y', 'title', "theme"]
            else:
                properties = self.widgets[w]
            # теперь в цикле перебираются свойства
            for property_ in properties:
                # для каждого свойства создается текст для
                # обозначения поля и само поле в котором пользователь записывает свойство
                frame = ttk.Frame(self.panel, relief="ridge", border=2)
                label = ttk.Label(frame, text=property_, relief="groove", borderwidth=2)
                res = self.get_field(property_, frame)
                entry = res[0]
                if len(res) > 1:
                    btn = res[1]
                    entry.place(width=self.sc_width / 100 * 6.5, y=3,
                                x=self.sc_width / 100 * 9)
                    btn.place(width=self.sc_width / 100 * 1.2, height=23, y=2,
                              x=self.sc_width / 100 * 9 + self.sc_width / 100 * 6.5)
                else:
                    entry.place(width=self.sc_width / 100 * 7.6, y=3,
                                x=self.sc_width / 100 * 9)
                entry.insert(0, self.get_property(property_, widget))
                label.place(width=self.sc_width / 100 * 6.5, y=4,
                            x=self.sc_width / 100 * 1)
                entry.bind("<FocusOut>", self.focus_out)
                # в переменной a и b хранится результат добавления виджета в панель (для последующего удаления)
                c = self.panel.create_window(0, properties.index(property_) * 30 + 13, window=frame, anchor="nw")
                self.panel.itemconfigure(c, width=self.panel.winfo_width() - 8, height=30)
                self.panel.coords(c, 4, properties.index(property_) * 30)
                self.panel_wigets.append(c)
                # в словарь fields добавляется свойство и его поле ввода
                self.master_.fields[property_] = entry
            # в переменной event_obj хранится выбранный виджет
            self.master_.window.current_obj = widget
