
from customtkinter import *

from FCOFFS.components import componentClass

class ComponentTab(CTkFrame):
    def __init__(self, master: CTkFrame, OverarchingMaster: CTkFrame, component: componentClass.ComponentClass, **kwargs):
        super().__init__(master, **kwargs)

        if issubclass(type(component), componentClass.ComponentClass): # temporary fox for now
            self.PS = component.parent_system
        self.component = component
        self.Master = OverarchingMaster

    def _delete(self) -> None:
        self.PS.components.remove(self.component)
        self.Master.components_tabview.delete(self.component.name)
        self.Master.new_component_index_opt.configure(values=[str(i) for i in range(len(self.PS.components) + 1)])
        self._change_move_options()

    def _move(self) -> None:
        if self.move_opt.get() and self.move_opt.get() != "Choose New Index":
            self.Master.components_tabview.move(int(self.move_opt.get()), self.component.name)
            self.PS.components.remove(self.component)
            self.PS.components.insert(int(self.move_opt.get()), self.component)
            self._change_move_options()

    def _get_available_indexes(self) -> list:
        opts = []
        for i in range(len(self.PS.components)):
            if i != self.Master.components_tabview.index(self.component.name):
                opts.append(str(i))
        return opts if opts else ["N/A"]
    
    def _change_move_options(self):
        for name in self.Master.components_tabview._tab_dict.keys():
            child = list(self.Master.components_tabview._tab_dict[name].children.keys())[1]
            frm = self.Master.components_tabview._tab_dict[name].children[child]
            opts = frm._get_available_indexes()
            frm.move_opt.configure(values=opts)
            frm.move_opt.set("Choose New Index")