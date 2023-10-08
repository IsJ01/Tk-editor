from tkinter import (Tk, Widget, ttk, Label, Canvas, Menu, DISABLED, NORMAL,
                     TclError, Frame, LabelFrame, Message, Menubutton, Button, Text)


class Window(Tk):
    def __init__(self, master):
        super().__init__()
        self.master_ = master
        self.style = ttk.Style(self)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.moved = [None]
        self.new_obj = None
        self.current_obj = None
        self.contextMenu = None
        self.height = self.winfo_screenheight()
        self.width = self.winfo_screenwidth()
        self.geometry(f"{int(self.width / 100 * 65)}x"
                      f"{int(self.height * 0.884) + 20}+{int(self.width / 100 * 15)}+{20}")
        self.press = [[], False]
        self.dx, self.dy = 0, 0
        self.bind("<Button-1>", self.click)
        self.bind("<ButtonRelease>", self.up)
        self.bind("<Motion>", self.motion)
        self.bind("<Button-3>", self.createWidgetMenu)
        self.bind('<Control-z>', self.master_.undo)
        self.bind('<Control-Shift-Z>', self.master_.redo)
        self.bind('<Control-x>', self.master_.cut)
        self.bind('<Control-c>', self.master_.copy)
        self.bind('<Control-v>', self.master_.paste)
        self.bind('<Delete>', self.master_.delete)
        self.canvases = []

    def on_closing(self):
        self.master_.menu.win_var.set(False)
        self.destroy()

    def createWidgetMenu(self, args):
        self.current_obj = args.widget
        if self.current_obj != self.master_.conf_panel.current_object:
            self.master_.addPropertyFields(args.widget)
        self.contextMenu = Menu(master=self, tearoff=0)
        commands = [("Cut", self.master_.cut), ("Copy", self.master_.copy),
                    ("Paste", self.master_.paste),
                    ("Delete", self.master_.delete)]
        for t, c in commands:
            self.contextMenu.add_command(label=t, command=c)
        x, y = args.x_root, args.y_root
        self.contextMenu.post(x, y)

    def click(self, event):
        if self.contextMenu:
            self.contextMenu.destroy()
            self.contextMenu = None
        self.master_.addPropertyFields(event.widget)
        self.master_.selected_objects.clear()
        self.press = [[event.x, event.y], True]
        self.moved = [None, (self.current_obj.winfo_x(), self.current_obj.winfo_y(),
                             self.current_obj.winfo_width(), self.current_obj.winfo_height())]

    def up(self, event):
        if self.moved[0]:
            self.master_.event_keeper.addEvent("move", self.moved)
        if self.current_obj != self and self.current_obj and self.press[1]:
            self.master_.addPropertyFields(self.current_obj)
        self.press = [[], False]
        if self.new_obj:
            self.master_.event_keeper.addEvent("append", [self.current_obj])
        if self.current_obj != self and self.current_obj:
            try:
                self.current_obj.config(state=NORMAL)
            except TclError:
                pass
        if self.canvases:
            for canvas in self.canvases:
                canvas.destroy()
        self.new_obj = None

    def delete_object(self, widget: Widget, del_=True):
        if widget != self:
            if del_:
                widget.destroy()
            else:
                widget.place_forget()
            self.current_obj = None

    def copy_widget(self, widget):
        if widget != self:
            new_wid = widget.__class__(self)
            new_wid: Widget
            fields = self.master_.conf_panel.widgets[widget.__class__]
            for c in fields:
                try:
                    new_wid[c] = widget[c]
                except TclError:
                    pass
            return new_wid

    def select(self, x0, y0, x1, y1):
        if self.canvases:
            for canvas in self.canvases:
                canvas.destroy()
        canvas_1 = Label(self, bg="lightblue")
        canvas_1.place(x=x0, y=y0, width=abs(x0 - x1), height=1)

        canvas_2 = Label(self, bg="lightblue")
        canvas_2.place(x=x0 + abs(x0 - x1), y=y0, width=1, height=abs(y0 - y1))

        canvas_3 = Label(self, bg="lightblue")
        canvas_3.place(x=x0, y=y0, width=1, height=abs(y0 - y1))

        canvas_4 = Label(self, bg="lightblue")
        canvas_4.place(x=x0, y=y0 + abs(y0 - y1), width=abs(x0 - x1), height=1)
        self.canvases = [canvas_1, canvas_2, canvas_3, canvas_4]
        children = [wid for wid in self.children.values()]
        selected_objects = []
        for w in children:
            if w not in self.canvases:
                if w.winfo_x() in range(x0, x1 + 1) and w.winfo_y() in range(y0, y1 + 1):
                    selected_objects.append(w)
        return selected_objects

    def setDefaultState(self, obj):
        if obj.__class__ == ttk.Separator:
            obj.place(width=40, height=10)
        if obj.__class__ in [Button, ttk.Button]:
            obj.config(text="button")
            obj.place(width=76, height=25)
        if obj.__class__ in [ttk.Menubutton]:
            obj.configure(text=self.new_obj.__name__)
        if obj.__class__ in [Menubutton]:
            obj.configure(text=self.new_obj.__name__)
            obj.configure(border=2, relief="raised")
        if obj.__class__ in [ttk.Notebook, Message, ttk.Treeview]:
            if obj.__class__ == Message:
                obj.config(width=50)
            obj.place(width=70, height=40)
        if obj.__class__ in (Canvas, Frame, LabelFrame, ttk.Frame, ttk.LabelFrame, Text):
            obj.place(width=75, height=40)
            obj.configure(border=2, relief="ridge")
        if obj.__class__ in (Label, ttk.Label, ttk.LabelFrame, LabelFrame, Message):
            obj.configure(text=self.new_obj.__name__)
            obj.configure(border=2, relief="groove")

    def ver_name(self, widget: Widget, new=True):
        names = [wid.widgetName for wid in self.children.values() if wid != widget and wid.place_info()]
        if not new and widget.widgetName in names:
            if widget.widgetName in names:
                return True
            else:
                return False
        else:
            name = widget.widgetName
            if names.count(widget.widgetName) >= 1:
                name = f"{widget.widgetName}_{names.count(widget.widgetName) + 1}"
            widget.widgetName = name

    @staticmethod
    def move_obj(obj: Widget, pos):
        try:
            obj.configure(state=DISABLED)
        except TclError:
            pass
        obj.place(x=pos[0], y=pos[1])

    def add_object(self, obj, pos):
        obj.place(x=pos[0], y=pos[1])
        try:
            obj.configure(state=DISABLED)
        except TclError:
            pass
        self.setDefaultState(obj)
        self.current_obj = obj
        self.ver_name(self.current_obj)

    def motion(self, event):
        x, y = (event.x_root - self.winfo_rootx(),
                event.y_root - self.winfo_rooty())
        if self.new_obj:
            if self.current_obj:
                self.move_obj(self.current_obj, (x, y))
            else:
                obj = self.new_obj(self)
                self.add_object(obj, (x, y))
        if self.press[1] and event.widget != self:
            self.moved = [self.current_obj, self.moved[1], (x, y,
                                                            self.current_obj.winfo_width(),
                                                            self.current_obj.winfo_height())]
            self.move_obj(self.current_obj, (x, y))
        elif self.press[1] and self.current_obj in (self, *self.canvases):
            x0, y0 = self.press[0]
            x0, x1 = sorted([x0, x])
            y0, y1 = sorted([y0, y])
            selected_objects = self.select(x0, y0, x1, y1)
            self.master_.select_widgets(selected_objects)
