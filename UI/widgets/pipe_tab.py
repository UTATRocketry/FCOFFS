
from customtkinter import *

from FCOFFS.components import pipe
from FCOFFS.fluids import fluid
from ..widgets.component_tab import ComponentTab
from .unit_entry import UnitEntry
from ..utilities.pop_ups import gui_error

class PipeTab(ComponentTab): 
    def __init__(self, master: CTkFrame, OverarchingMaster: CTkFrame, component: pipe.Pipe, **kwargs):
        super().__init__(master, OverarchingMaster, component, **kwargs)

        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)

        self.component_name_lbl = CTkLabel(self, text=f"Component Name:", font=("Arial", 18))
        self.component_name_ent = CTkEntry(self, font=("Arial", 18), placeholder_text=self.component.name)
        self.component_type_lbl = CTkLabel(self, text="Component Type: Pipe", font=("Arial", 18))
        self.fluid_lbl = CTkLabel(self, text="Fluid: ", font=("Arial", 14))
        self.fluid_opt = CTkOptionMenu(self, font=("Arial", 14), values=list(fluid.Fluid.supported_fluids))
        self.fluid_opt.set(component.fluid)
        self.diameter_lbl = CTkLabel(self, text="Diameter: ", font=("Arial", 14))
        self.diameter = UnitEntry(self, "DISTANCE", self.component.diameter)
        self.length_lbl = CTkLabel(self, text="Length: ", font=("Arial", 14))
        self.length = UnitEntry(self, "DISTANCE", self.component.length)
        self.roughness_lbl = CTkLabel(self, text="Roughness: ", font=("Arial", 14))
        self.roughness = CTkEntry(self, font=("Arial", 14))
        self.roughness.insert(0, str(self.component.roughness))
        self.epsilon_lbl = CTkLabel(self, text="Epsilon: ", font=("Arial", 14))
        self.epsilon = CTkEntry(self, font=("Arial", 14))
        self.epsilon.insert(0, str(self.component.epsilon))
        self.set_btn = CTkButton(self, text="SET", font=("Arial", 16), command=self.__set)
        self.delete_btn = CTkButton(self, text="DELETE", font=("Arial", 16), command=self.__delete)
        self.move_frm = CTkFrame(self)
        self.move_btn = CTkButton(self.move_frm, text="Move", font=("Arial", 16), command=self.__move)
        opts = self._get_available_indexes()
        self.move_opt = CTkOptionMenu(self.move_frm, font=("Arial", 14), values=opts)
        self.component_name_lbl.grid(row=0, column=0, padx=(10, 5), pady=(10, 15), sticky="nse")
        self.component_name_ent.grid(row=0, column=1, padx=(5, 10), pady=(10, 15), sticky="nsew")
        self.component_type_lbl.grid(row=0, column=2, columnspan=2, padx=(10, 15), pady=10, sticky="nsew")
        self.fluid_lbl.grid(row=1, column=0, padx=(10, 5), pady=(10, 5), sticky="nsew")
        self.fluid_opt.grid(row=1, column=1, padx=(5, 10), pady=(10, 5), sticky="ew")
        self.diameter_lbl.grid(row=2, column=0, padx=(10, 5), pady=5, sticky="nsew")
        self.diameter.grid(row=2, column=1, padx=(0, 5), pady=5, sticky="nsew")
        self.length_lbl.grid(row=2, column=2, padx=(5, 5), pady=5, sticky="nsew")
        self.length.grid(row=2, column=3, padx=(0, 10), pady=5, sticky="nsew")
        self.roughness_lbl.grid(row=3, column=0, padx=(10, 5), pady=(5, 10), sticky="nsew")
        self.roughness.grid(row=3, column=1, padx=(0, 5), pady=(5, 10), sticky="nsew")
        self.epsilon_lbl.grid(row=3, column=2, padx=(5, 5), pady=(5, 10), sticky="nsew")
        self.epsilon.grid(row=3, column=3, padx=(0, 10), pady=(5, 10), sticky="nsew")
        self.set_btn.grid(row=4, column=2, padx=(5, 5), pady=(10, 10))
        self.delete_btn.grid(row=4, column=3, padx=(5, 10), pady=(10, 10))
        self.move_opt.grid(row=0, column=1, padx=(10, 5), pady=(5, 5))
        self.move_btn.grid(row=0, column=0, padx=(5, 10), pady=(5, 5))
        self.move_frm.grid(row=4, column=0, columnspan=2, padx=(10, 5), pady=(10, 10))
        self.move_opt.set("Choose New Index")
        super

    def __set(self) -> None:
        name = self.component_name_ent.get()
        if name:
            self.Master.components_tabview.rename(self.component.name, name)
            self.component.name = name
            self.Master.components_tabview.set(name)
        self.component.fluid = self.fluid_opt.get()
        self.component.diameter = self.diameter.unit
        self.component.length = self.length.unit
        try:
            self.component.roughness = float(self.roughness.get())
            self.component.epsilon = float(self.epsilon.get())
        except:
            gui_error(f"Invalid Input Value, Must be a number, not a string")

    def __delete(self) -> None: 
        super()._delete()

    def __move(self) -> None: 
        super()._move()

    def _get_available_indexes(self) -> list:
        return super()._get_available_indexes()
    
    def _change_move_options(self):
        super()._change_move_options()
