import io

from xml.etree import ElementTree as et
from tkinter import *
from tkinter import ttk


# этот класс генерирует код, на основе виджетов, которые ему передали
class CodeGenerator:
    # в конструктор передается файл, в который записывается код
    def __init__(self, py_file: io.TextIOWrapper, ui_file: io.TextIOWrapper):
        self.py_file = py_file
        self.ui_file = ui_file
        self._generate()

    def _generate(self):
        var_names = []
        code = ["import tkinter", "from tkinter import ttk", "", ""]
        doc = et.parse(self.ui_file)
        root = doc.getroot()
        code.append(f"class Window(tkinter.{root.tag}):")
        code.append(" " * 4 + "def __init__(self, **kw):")
        code.append(" " * 8 + "super().__init__(**kw)")
        code.append(" " * 8 + f"self.title('{root.attrib['title']}')")
        code.append(" " * 8 + f"self.style = ttk.Style(self)")
        code.append(" " * 8 + f"self.style.theme_use('{root.attrib['theme']}')")
        code.append(" " * 8 + f"self.geometry('{root.attrib['width']}x{root.attrib['height']}"
                    f"+{root.attrib['x']}+{root.attrib['y']}')")
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
            code.append(" " * 8 + f"self.{name} = {class_}({', '.join(fields)})")
            code.append(" " * 8 + f"self.{name}.place(x={el.attrib['x']}, y={el.attrib['y']},"
                        f" width={el.attrib['width']}, height={el.attrib['height']})")
        code.append("")
        self.py_file.write('\n'.join(code))