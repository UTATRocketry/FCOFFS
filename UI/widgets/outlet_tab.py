
from customtkinter import *
from customtkinter import CTkFrame

from FCOFFS.interfaces.interface import PressureOutlet
from ..widgets.component_tab import ComponentTab
from ..widgets.unit_entry import UnitEntry

class OutletTab(ComponentTab):
    def __init__(self, master: CTkFrame, OverarchingMaster: CTkFrame, component: PressureOutlet, **kwargs):
        super().__init__(master, OverarchingMaster, component, **kwargs)

        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.component_name_lbl = CTkLabel(self, text=f"Component Name:", font=("Arial", 18))
        self.component_name_ent = CTkEntry(self, font=("Arial", 18), placeholder_text=self.component.name)
        self.component_type_lbl = CTkLabel(self, text="Component Type: Outlet", font=("Arial", 18))
        self.type_lbl = CTkLabel(self, text="Inlet Type: ", font=("Arial", 14))
        self.type_opt = CTkOptionMenu(self, font=("Arial", 14), values=["Pressure Outlet"])
        self.pressure_lbl = CTkLabel(self, text="Inlet Pressure: ", font=("Arial", 14))
        self.pressure = UnitEntry(self, "PRESSURE", self.component.p)
        self.set_btn = CTkButton(self, text="SET", font=("Arial", 16), command=self.__set)
        self.delete_btn = CTkButton(self, text="DELETE", font=("Arial", 16), command=self.__delete)
        #self.move_frm = CTkFrame(self)
        #self.move_btn = CTkButton(self.move_frm, text="Move", font=("Arial", 16), command=self.__move)
        #opts = self._get_available_indexes()
        #self.move_opt = CTkOptionMenu(self.move_frm, font=("Arial", 14), values=opts)
        self.component_name_lbl.grid(row=0, column=0, padx=(10, 5), pady=(10, 15), sticky="nse")
        self.component_name_ent.grid(row=0, column=1, padx=(5, 10), pady=(10, 15), sticky="nsew")
        self.component_type_lbl.grid(row=0, column=2, columnspan=2, padx=(10, 15), pady=10, sticky="nsew")
        self.type_lbl.grid(row=1, column=0, padx=(10, 5), pady=(10, 5), sticky="nsew")
        self.type_opt.grid(row=1, column=1, padx=(5, 10), pady=(10, 5), sticky="ew")
        self.pressure_lbl.grid(row=1, column=2, padx=(10, 5), pady=5, sticky="nsew")
        self.pressure.grid(row=1, column=3, padx=(0, 5), pady=5, sticky="nsew")
        self.set_btn.grid(row=2, column=2, padx=(5, 5), pady=(10, 10))
        self.delete_btn.grid(row=2, column=3, padx=(5, 10), pady=(10, 10))
        #self.move_opt.grid(row=0, column=1, padx=(10, 5), pady=(5, 5))
       # self.move_btn.grid(row=0, column=0, padx=(5, 10), pady=(5, 5))
        #self.move_frm.grid(row=2, column=0, columnspan=2, padx=(10, 5), pady=(10, 10))
        #self.move_opt.set("Choose New Index")

    def __set(self) -> None:
        name = self.component_name_ent.get()
        if name:
            self.Master.components_tabview.rename(self.component.name, name)
            self.component.name = name
            self.Master.components_tabview.set(name)
        self.component.p = self.pressure.unit

    def __delete(self) -> None: 
        super()._delete()

    # def __move(self) -> None: 
    #     super()._move()

    def _get_available_indexes(self) -> list:
        return super()._get_available_indexes()
    
    def _change_move_options(self):
        super()._change_move_options()
