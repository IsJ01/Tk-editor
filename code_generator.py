import io

from xml.etree import ElementTree as et


# этот класс генерирует код, на основе виджетов, которые ему передали
class CodeGenerator:
    # в конструктор передается файл, в который записывается код
    def __init__(self, py_file: io.TextIOWrapper, ui_file: io.TextIOWrapper):
        self.py_file = py_file
        self.ui_file = ui_file
        self._generate()

    @staticmethod
    def _get_objects_code(doc: et.ElementTree, master="self", parts=False):
        var_names = []
        code = []
        if parts:
            widgets = []
            post = []
        for el in doc.getroot():
            fields = []
            class_ = el.tag
            if "ttk" == el.tag.split('.')[1]:
                class_ = '.'.join(el.tag.split('.')[1:])
            name = el.attrib['widgetName']
            if var_names.count(name) >= 1:
                name += f"_{var_names.count(name) + 1}"
            var_names.append(name)
            for field in el.attrib.keys():
                if field not in ["x", "y", "width", "height", "widgetName"]:
                    fields.append(f"{field}='{el.attrib[field]}'")
            w = f"self.{name} = {class_}(master={master}, {', '.join(fields)})"
            p = (f"self.{name}.place(x={el.attrib['x']}, y={el.attrib['y']},"
                 f" width={el.attrib['width']}, height={el.attrib['height']})")
            if not parts:
                code.append(w)
                code.append(p)
            else:
                widgets.append(w)
                post.append(p)
        return code if not parts else (widgets, post)

    def _get_window_code(self, doc: et.ElementTree):
        code = [" ", " "]
        root = doc.getroot()
        w, h, x, y = root.attrib['width'], root.attrib['height'], root.attrib['x'], root.attrib['y']
        code.append("class Window(tkinter.Tk):")
        code.append("    def __init__(self, **kw):")
        code.append("        super().__init__(**kw)")
        code.append(f"        self.title('{root.attrib['title']}')")
        code.append("        self.style = ttk.Style(self)")
        code.append(f"        self.style.theme_use('{root.attrib['theme']}')")
        code.append(f"        self.geometry('{w}x{h}+{x}+{y}')")
        code.append("        self.initUi()")
        code.append("")
        code.append("    def initUi(self):")
        code += [" " * 8 + obj for obj in self._get_objects_code(doc)]
        return code

    def _get_simple_dialog_code(self, doc: et.ElementTree):
        code = ["from tkinter import simpledialog", " ", " "]
        root = doc.getroot()
        w, h, x, y = root.attrib['width'], root.attrib['height'], root.attrib['x'], root.attrib['y']
        code.append("class Dialog(simpledialog.Dialog):")
        code.append("    def __init__(self, parent, title=None):")
        code.append("        super().__init__(parent, title)")
        code.append(f"        self.title('{root.attrib['title']}')")
        code.append("        self.style = ttk.Style(self)")
        code.append(f"        self.style.theme_use('{root.attrib['theme']}')")
        code.append("")
        code.append("    def buttonbox(self):")
        code.append("        pass")
        code.append("")
        code.append("    def body(self, master):")
        code.append(f"        self.geometry('{w}x{h}+{x}+{y}')")
        code += [" " * 8 + obj for obj in self._get_objects_code(doc)]
        return code

    def _get_common_dialog_code(self, doc: et.ElementTree):
        code = ["from tkinter import commondialog", " ", " "]
        root = doc.getroot()
        w, h, x, y = root.attrib['width'], root.attrib['height'], root.attrib['x'], root.attrib['y']
        code.append("class Dialog(commondialog.Dialog):")
        code.append("    def __init__(self, master=None, **options):")
        code.append("        super().__init__(master, **options)")
        code.append("")
        code.append("    def show(self, **options):")
        code.append("        self.win = tkinter.Toplevel(self.master)")
        code.append(f"        self.win.geometry('{w}x{h}+{x}+{y}')")
        code += [" " * 8 + obj for obj in self._get_objects_code(doc, "self.win")]
        code.append("        self.win.mainloop()")
        return code

    def _get_widget_code(self, doc: et.ElementTree):
        code = [" ", " "]
        root = doc.getroot()
        w, h, x, y = root.attrib['width'], root.attrib['height'], root.attrib['x'], root.attrib['y']
        widgets, post = self._get_objects_code(doc, parts=True)
        widgets = [" " * 8 + w for w in widgets]
        post = [" " * 8 + p for p in post]
        code.append("class Widget(tkinter.Frame):")
        code.append("    def __init__(self, master=None, cnf={}, **kw):")
        code.append("        super().__init__(master, cnf, **kw)")
        code.append("        self.initUi()")
        code.append("")
        code.append("    def initUi(self):")
        code += widgets
        code.append("")
        code.append("    def post(self):")
        code += post
        code.append("")
        code.append("    @staticmethod")
        code.append("    def state(func, **kw):")
        code.append("        def wrapper(cnf={}, **kw):")
        code.append("            func(cnf, **kw)")
        code.append("            cnf.update()")
        code.append("            cnf.post()")
        code.append("        return wrapper")
        code.append("")
        code.append("    @state")
        code.append("    def place_configure(self, cnf={}, **kw):")
        code.append("        super().place_configure(cnf, **kw)")
        code.append("")
        code.append("    @state")
        code.append("    def grid_configure(self, cnf={}, **kw):")
        code.append("        super().grid_configure(cnf, **kw)")
        code.append("")
        code.append("    @state")
        code.append("    def pack_configure(self, cnf={}, **kw):")
        code.append("        super().pack_configure(cnf, **kw)")
        code.append("")
        code.append("    def configure(self, cnf=None, **kw):")
        code.append("        return self._configure('configure', cnf, kw)")
        code.append("")
        code.append("    place = place_configure")
        code.append("    grid = grid_configure")
        code.append("    pack = pack_configure")

        return code

    def _generate(self):
        doc = et.parse(self.ui_file)
        root = doc.getroot()
        code = ["import tkinter", "from tkinter import ttk"]
        if root.tag == "tkinter.Tk":
            code += self._get_window_code(doc)
        if root.tag == "simpledialog.Dialog":
            code += self._get_simple_dialog_code(doc)
        if root.tag == "commondialog.Dialog":
            code += self._get_common_dialog_code(doc)
        if root.tag == "Widget":
            code += self._get_widget_code(doc)
        self.py_file.write('\n'.join(code))
