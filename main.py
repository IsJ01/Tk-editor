import copy
import tkinter
from tkinter import filedialog, NORMAL, TclError, ttk, messagebox
from xml.dom import minidom
from xml.etree import ElementTree as et

from code_generator import CodeGenerator
from config_panel import ConfigPanel
from event_keeper import EventKeeper
from info_window import Info
from menu import ToolBar
from widgets_panel import WidgetsPanel
from window import Window


class Main:
    def __init__(self, **kw):

        self.copy_objects = []
        self.selected_objects = []

        # в этом словаре хранятся свойства и их поля
        self.fields = {}

        self.event_keeper = EventKeeper(self)
        self.menu = ToolBar(self)
        self.conf_panel = ConfigPanel(self)
        self.window = Window(self)
        self.wid_panel = WidgetsPanel(self)
        self.menu.mainloop()
        self.wid_panel.mainloop()
        self.conf_panel.mainloop()
        self.window.mainloop()

    def win_mode(self, *args):
        try:
            self.window.title()
            if self.menu.win_var.get():
                self.window.deiconify()
            else:
                self.window.withdraw()
        except TclError:
            self.window = Window(self)

    def conf_mode(self):
        try:
            self.conf_panel.title()
            if self.menu.conf_var.get():
                self.conf_panel.deiconify()
            else:
                self.conf_panel.withdraw()
        except TclError:
            self.conf_panel = ConfigPanel(self)

    def wid_mode(self):
        try:
            self.wid_panel.title()
            if self.menu.wid_var.get():
                self.wid_panel.deiconify()
            else:
                self.wid_panel.withdraw()
        except TclError:
            self.wid_panel = WidgetsPanel(self)

    # метод save сохраняет информацию о приложении в выбранном файле формата json
    def save(self):
        # в переменную file добавляется название файла, в который будет идти запись
        file = filedialog.asksaveasfilename(filetypes=({'Ui .ui': ".ui"}))

        if not file:
            return

        # функция для получения текста для его добавления в тег
        def getText(widget):
            if "text" in self.conf_panel.widgets[widget.__class__]:
                return widget["text"]
            return ""

        with open(file, 'w', encoding='utf8') as f:
            doc = minidom.Document()
            win = doc.createElement("Tk")
            for field in ["x", "y", "width", "height"]:
                eval(f"win.setAttribute(attname=field, value=self.window.winfo_{field}().__str__())")
            win.setAttribute(attname="title", value=self.window.title())
            win.setAttribute(attname="theme", value=self.window.style.theme_use())
            doc.appendChild(win)
            for widget in self.window.children.values():
                if not widget.place_info():
                    continue
                wid = doc.createElement(str(widget.__class__).split("'")[1])
                wid.setAttribute(attname="widgetName",
                                 value=self.get_normal_name(widget.widgetName))
                for field in self.conf_panel.widgets[widget.__class__][1:]:
                    if field not in ["x", "y", "width", "height"]:
                        if widget[field].__str__():
                            wid.setAttribute(attname=field, value=widget[field].__str__())
                    else:
                        eval(f"wid.setAttribute(attname=field, value=widget.winfo_{field}().__str__())")
                win.appendChild(wid)
            doc.writexml(f, "", "\t", "\n")

    # generate_place генерирует код с размещение виджетов методом place
    def generate(self):
        filename1 = filedialog.asksaveasfilename(filetypes=({'Python .py': ".py"}))
        if filename1:
            filename2 = filedialog.askopenfilename(filetypes=({'Ui .ui': ".ui"}))
            if filename2:
                with open(filename1, encoding="utf8", mode="w") as py_file:
                    with open(filename2, encoding='utf8') as ui_file:
                        CodeGenerator(py_file, ui_file)

    # метод open способен открыть файл с виджетами и разместить их в окно
    def open(self):
        file = filedialog.askopenfilename(filetypes=({'Ui .ui': ".ui"}))
        if not file:
            return
        self.window.destroy()
        self.window = Window(self)
        self.menu.destroy()
        self.menu = ToolBar(self)
        self.wid_panel.destroy()
        self.wid_panel = WidgetsPanel(self)
        self.conf_panel.destroy()
        self.conf_panel = ConfigPanel(self)
        self.event_keeper = EventKeeper(self)
        with open(file, encoding='utf8') as f:
            doc = et.parse(f)
            root = doc.getroot()
            self.window.geometry(f"{root.attrib['width']}x{root.attrib['height']}"
                                 f"+{root.attrib['x']}+{root.attrib['y']}")
            self.window.style.theme_use(root.attrib["theme"])
            for el in doc.getroot():
                new_wid = eval(el.tag)(self.window)
                new_wid.widgetName = el.attrib["widgetName"]
                new_wid.place(x=el.attrib["x"], y=el.attrib["y"],
                              width=el.attrib["width"], height=el.attrib["height"])
                for field in el.attrib.keys():
                    if field not in ["x", "y", "width", "height", "widgetName"]:
                        new_wid[field] = el.attrib[field]

    # addPropertyFields добавляет свойства для настройки виджетов
    def addPropertyFields(self, event):
        self.conf_panel.addPropertyFields(event)

    @staticmethod
    def is_normal_name(name: str):
        if name[0].isalpha() or name == "_":
            for w in name[1:]:
                if not (w.isalpha() or w.isdigit() or w == "_"):
                    return False
            return True
        return False

    @staticmethod
    def get_normal_name(name: str):
        try:
            eval(f"{copy.deepcopy(name)} = 4")
            return name
        except SyntaxError:
            return name.replace("::", "_")

    # метод apply сохраняет свойства виджета
    def apply(self, *args):
        if not self.window.current_obj:
            return
        old_fields = {}
        if self.window.current_obj == self.window:
            conf = {}
            for field in ['width', 'height', 'x', 'y']:
                old_fields[field] = str(eval(f'self.window.winfo_{field}()'))
                conf[field] = (eval(f"int(self.fields[field].get())"
                                    f" if self.fields[field].get() else self.window.winfo_{field}()"))
            self.window.geometry(f"{conf['width']}x{conf['height']}+{conf['x']}+{conf['y']}")
            old_fields['title'] = self.window.title()
            self.window.title(self.fields["title"].get())
            old_fields['theme'] = self.window.style.theme_use()
            self.window.style.theme_use(self.fields["theme"].get())
        else:
            conf = {}
            name = self.fields["widgetName"].get()
            if not self.fields["widgetName"].get():
                name = self.get_normal_name(self.window.current_obj.widgetName)
            if self.window.ver_name(self.window.current_obj, new=False):
                messagebox.showwarning("Warning", "This name has already been assigned to another widget")
                return
            if not self.is_normal_name(self.fields["widgetName"].get()) and self.fields["widgetName"].get():
                messagebox.showwarning("Warning", "This name cannot be given to the widget")
                return
            old_fields["widgetName"] = self.window.current_obj.widgetName
            self.window.current_obj.widgetName = name
            for field in ['width', 'height', 'x', 'y']:
                try:
                    old_fields[field] = str(eval(f'self.window.current_obj.winfo_{field}()'))
                    conf[field] = (eval(f"int(self.fields[field].get()) if self.fields[field].get()"
                                        f" else self.window.current_obj.winfo_{field}()"))
                except ValueError:
                    self.fields[field].delete(0, "end")
                    self.fields[field].insert(0, str(eval(f'self.window.current_obj.winfo_{field}()')))
                    conf[field] = (eval(f"int(self.fields[field].get()) if self.fields[field].get()"
                                        f" else self.window.current_obj.winfo_{field}()"))
            for field in self.fields:
                if self.fields[field].get() or field in ["cursor", "text"]:
                    if field not in ["widgetName", "x", "y", "width", "height"]:
                        try:
                            old_fields[field] = self.window.current_obj[field].__str__()
                            self.window.current_obj[field] = self.fields[field].get()
                        except TclError:
                            pass
                elif field in ['background', "activebackground"]:
                    old_fields[field] = self.window.current_obj[field]
                    self.window.current_obj[field] = "SystemButtonFace"
                elif field in ['foreground', "activeforeground"]:
                    old_fields[field] = self.window.current_obj[field]
                    self.window.current_obj[field] = "SystemButtonText"
            self.window.current_obj.place(x=conf['x'], y=conf['y'],
                                          width=conf['width'], height=conf['height'])
        new_f = {k: v.get() for k, v in self.fields.items()}
        if not (old_fields == new_f):
            self.event_keeper.addEvent("apply", [self.window.current_obj, old_fields, new_f])

    # метод delete удаляет виджет
    def delete(self, *args):
        if self.window.current_obj == self.window:
            return
        objects = [self.window.current_obj]
        if self.selected_objects:
            objects = self.selected_objects
        delete_objects = []
        for wid in objects:
            delete_objects.append((wid, wid.winfo_x(), wid.winfo_y(),
                                   wid.winfo_width(), wid.winfo_height()))
            self.window.delete_object(wid, del_=False)
        self.event_keeper.addEvent("delete", delete_objects)
        self.conf_panel.panel.delete("all")

    def undo(self, *args):
        self.event_keeper.removeEvent()

    def redo(self, *args):
        self.event_keeper.redoEvent()

    def copy(self, *args):
        if self.window.current_obj == self.window:
            return
        self.copy_objects.clear()
        objects = [self.window.current_obj]
        if self.selected_objects:
            objects = self.selected_objects[::]
        for wid in objects:
            self.copy_objects.append((self.window.copy_widget(wid),
                                      wid.winfo_x(), wid.winfo_y(),
                                      wid.winfo_width(), wid.winfo_height()))

    def cut(self, *args):
        if self.window.current_obj == self.window:
            return
        self.copy_objects.clear()
        objects = [self.window.current_obj]
        if self.selected_objects:
            objects = self.selected_objects
        delete_objects = []
        for wid in objects:
            delete_objects.append((wid, wid.winfo_x(), wid.winfo_y(),
                                   wid.winfo_width(), wid.winfo_height()))
            self.copy_objects.append((self.window.copy_widget(wid), wid.winfo_x(), wid.winfo_y(),
                                      wid.winfo_width(), wid.winfo_height()))
            self.window.delete_object(wid, del_=False)
        self.event_keeper.addEvent("delete", delete_objects)

    def paste(self, *args):
        if self.copy_objects:
            min_x, min_y = (min([w[1] for w in self.copy_objects]),
                            min([w[2] for w in self.copy_objects]))
            c_x, c_y = (self.window.winfo_pointerx() - self.window.winfo_rootx(),
                        self.window.winfo_pointery() - self.window.winfo_rooty())
            objects = []
            for wid, x, y, w, h in self.copy_objects:
                if not wid:
                    continue
                new_x = c_x + x - min_x
                new_y = c_y + y - min_y
                new_wid = self.window.copy_widget(wid)
                new_wid.place(x=new_x, y=new_y,
                              width=w, height=h)
                new_wid.widgetName = self.get_normal_name(new_wid.widgetName)
                self.window.ver_name(new_wid)
                objects.append(new_wid)
            self.event_keeper.addEvent("paste", objects)

    @staticmethod
    def get_info():
        info = Info()
        info.mainloop()

    def setMode(self, *args):
        self.wid_panel.render(mode=self.menu.var.get())

    def select_widgets(self, widgets):
        self.selected_objects.clear()
        self.selected_objects = widgets[::]

    # в данный метод сохраняет выбранный пользователем виджет
    def getWidget(self, event):
        if self.window.current_obj:
            try:
                self.window.current_obj.config(state=NORMAL)
            except TclError:
                pass
        self.window.current_obj = None
        self.window.new_obj = None
        item = self.wid_panel.treeView.item(self.wid_panel.treeView.selection())
        if item["tags"] == ["tree"]:
            return
        tag = item["tags"][0] + "." if item["tags"] else 'tkinter' + '.'
        class_ = f'{tag}{item["text"].strip()}'
        widget = eval(class_)
        self.window.new_obj = widget


Main()
