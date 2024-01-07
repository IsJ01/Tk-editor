class EventKeeper:
    master = None
    events = []
    redo_events = []

    def __init__(self, master):
        self.master = master

    def addEvent(self, event: str, *args):
        if event == "delete" or event == "cut":
            self.events.append({"delete": args[0]})
        else:
            self.events.append({event: args[0]})

    def removeDelEvent(self, event):
        self.redo_events.append({"delete": event})
        for wid, x, y, w, h in event:
            wid.place(x=x, y=y, width=w, height=h)

    def removeAppendEvent(self, event, paste=False):
        if not paste:
            self.redo_events.append({"append": (event[0], event[0].winfo_x(), event[0].winfo_y(),
                                                event[0].winfo_width(), event[0].winfo_height())})
        self.master.window.delete_object(event[0], del_=False)

    def removePasteEvent(self, event):
        self.redo_events.append({"paste": event})
        for wid in event:
            self.removeAppendEvent([wid], paste=True)

    def redoApplyEvent(self, event):
        self.addEvent("apply", event)
        obj, fields = event[0], event[2]
        if obj == self.master.window:
            self.master.window.geometry(f"{fields['width']}x{fields['height']}+{fields['x']}+{fields['y']}")
            self.master.window.title(fields["title"])
            self.master.window.style.theme_use(fields["theme"])
            self.master.window["background"] = fields["background"]
        else:
            obj.place(x=fields["x"], y=fields["y"], width=fields["width"], height=fields["height"])
            for field in fields:
                if field == "widgetName":
                    obj.widgetName = ''.join(list(fields[field]))
                if field not in ["widgetName", "x", "y", "width", "height"]:
                    obj[field] = fields[field]
        self.master.conf_panel.addPropertyFields(obj)

    def removeApplyEvent(self, event):
        self.redo_events.append({"apply": event})
        obj, fields = event[:2]
        if obj == self.master.window:
            self.master.window.geometry(f"{fields['width']}x{fields['height']}+{fields['x']}+{fields['y']}")
            self.master.window.title(fields["title"])
            self.master.window.style.theme_use(fields["theme"])
            self.master.window["background"] = fields["background"]
        else:
            obj.place(x=fields["x"], y=fields["y"], width=fields["width"], height=fields["height"])
            for field in fields:
                if field == "widgetName":
                    obj.widgetName = ''.join(list(fields[field]))
                if field not in ["widgetName", "x", "y", "width", "height"]:
                    obj[field] = fields[field]
        self.master.conf_panel.addPropertyFields(obj)

    def redoDelEvent(self, event):
        self.addEvent("delete", (event))
        for wid, x, y, w, h in event:
            self.master.window.delete_object(wid, del_=False)

    def redoAppendEvent(self, event, paste=False):
        if not paste:
            self.addEvent("append", event)
        event[0].place(x=event[1], y=event[2], width=event[3], height=event[4])

    def redoPasteEvent(self, event):
        self.addEvent("paste", event)
        for wid in event:
            self.redoAppendEvent((wid, wid.winfo_x(), wid.winfo_y(),
                                  wid.winfo_width(), wid.winfo_height()), paste=True)

    def removeMoveEvent(self, event):
        self.redo_events.append({"move": event})
        event[0].place(x=event[1][0], y=event[1][1], width=event[1][2], height=event[1][3])

    def redoMoveEvent(self, event):
        self.events.append({"move": event})
        event[0].place(x=event[2][0], y=event[2][1], width=event[2][2], height=event[2][3])

    def redoEvent(self):
        if not self.redo_events:
            return
        if "delete" in self.redo_events[-1]:
            self.redoDelEvent(self.redo_events[-1]["delete"])
        elif "append" in self.redo_events[-1]:
            self.redoAppendEvent(self.redo_events[-1]["append"])
        elif "paste" in self.redo_events[-1]:
            self.redoPasteEvent(self.redo_events[-1]["paste"])
        elif "apply" in self.redo_events[-1]:
            self.redoApplyEvent(self.redo_events[-1]["apply"])
        elif "move" in self.redo_events[-1]:
            self.redoMoveEvent(self.redo_events[-1]["move"])
        del self.redo_events[-1]
        self.master.win_panel.render() if self.master.menu.win_panel_var.get() else ...

    def removeEvent(self):
        if not self.events:
            return
        if "delete" in self.events[-1]:
            self.removeDelEvent(self.events[-1]["delete"])
        elif "append" in self.events[-1]:
            self.removeAppendEvent(self.events[-1]["append"])
        elif "paste" in self.events[-1]:
            self.removePasteEvent(self.events[-1]["paste"])
        elif "apply" in self.events[-1]:
            self.removeApplyEvent(self.events[-1]["apply"])
        elif "move" in self.events[-1]:
            self.removeMoveEvent(self.events[-1]["move"])
        del self.events[-1]
        self.master.win_panel.render() if self.master.menu.win_panel_var.get() else ...
