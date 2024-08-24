from customtkinter import *

from FCOFFS.components import injector
from FCOFFS.fluids import Fluid
from ..widgets.component_tab import ComponentTab
from .unit_entry import UnitEntry
from ..utilities.pop_ups import gui_error

class InjectorTab(ComponentTab): 
    def __init__(self, master: CTkFrame, OverarchingMaster: CTkFrame, component: injector.Injector, **kwargs):
        super().__init__(master, OverarchingMaster, component, **kwargs)

        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)

        self.component_name_lbl = CTkLabel(self, text=f"Component Name:", font=("Arial", 18))
        self.component_name_ent = CTkEntry(self, font=("Arial", 18), placeholder_text=self.component.name)
        self.component_type_lbl = CTkLabel(self, text="Component Type: Injector", font=("Arial", 18))
        self.fluid_lbl = CTkLabel(self, text="Fluid: ", font=("Arial", 14))
        self.fluid_opt = CTkOptionMenu(self, font=("Arial", 14), values=list(Fluid.Fluid.supported_fluids))
        self.fluid_opt.set(component.fluid)
        self.diameter_in_lbl = CTkLabel(self, text="Diameter In: ", font=("Arial", 14))
        self.diameter_in = UnitEntry(self, "DISTANCE", self.component.diameter_in)
        self.diameter_out_lbl = CTkLabel(self, text="Diameter Out: ", font=("Arial", 14))
        self.diameter_out = UnitEntry(self, "DISTANCE", self.component.diameter_out)
        self.diameter_hole_lbl = CTkLabel(self, text="Hole Diameter: ", font=("Arial", 14))
        self.diameter_hole = UnitEntry(self, "DISTANCE", self.component.diameter)
        self.num_holes_lbl = CTkLabel(self, text="Number of Holes: ", font=("Arial", 14))
        self.num_holes = CTkEntry(self, font=("Arial", 14), placeholder_text=self.component.num_hole)
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
        self.diameter_in_lbl.grid(row=2, column=0, padx=(10, 5), pady=5, sticky="nsew")
        self.diameter_in.grid(row=2, column=1, padx=(0, 5), pady=5, sticky="nsew")
        self.diameter_out_lbl.grid(row=2, column=2, padx=(10, 5), pady=5, sticky="nsew")
        self.diameter_out.grid(row=2, column=3, padx=(0, 5), pady=5, sticky="nsew")
        self.diameter_hole_lbl.grid(row=3, column=0, padx=(10, 5), pady=5, sticky="nsew")
        self.diameter_hole.grid(row=3, column=1, padx=(0, 5), pady=5, sticky="nsew")
        self.num_holes_lbl.grid(row=3, column=2, padx=(10, 5), pady=5, sticky="nsew")
        self.num_holes.grid(row=3, column=3, padx=(0, 5), pady=5, sticky="nsew")
        self.set_btn.grid(row=4, column=2, padx=(5, 5), pady=(10, 10))
        self.delete_btn.grid(row=4, column=3, padx=(5, 10), pady=(10, 10))
        self.move_opt.grid(row=0, column=1, padx=(10, 5), pady=(5, 5))
        self.move_btn.grid(row=0, column=0, padx=(5, 10), pady=(5, 5))
        self.move_frm.grid(row=4, column=0, columnspan=2, padx=(10, 5), pady=(10, 10))
        self.move_opt.set("Choose New Index")

    def __set(self) -> None:
        name = self.component_name_ent.get()
        if name:
            self.Master.components_tabview.rename(self.component.name, name)
            self.component.name = name
            self.Master.components_tabview.set(name)
        self.component.fluid = self.fluid_opt.get()
        self.component.diameter = self.diameter_hole.unit().convert_base_metric()
        self.component.diameter_hole = self.diameter_hole.unit().convert_base_metric()
        self.component.diameter_in = self.diameter_in.unit().convert_base_metric()
        self.component.diameter_out = self.diameter_out.unit().convert_base_metric()
        try:
            self.component.num_hole = int(self.num_holes.get())
        except:
            gui_error(f"Invalid Input Value, Must be a number, not a string")
        self.Master.write_to_display(f"\nSet new parameters for component: {self.component.name} \n")
        self.Master.PS.initialized = False

    def __delete(self) -> None: 
        super()._delete()

    def __move(self) -> None: 
        super()._move()

    def _get_available_indexes(self) -> list:
        return super()._get_available_indexes()
    
    def _change_move_options(self):
        super()._change_move_options()