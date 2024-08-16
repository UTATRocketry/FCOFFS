from typing import Any
from customtkinter import *
import pickle

from FCOFFS.pressureSystem import PressureSystem
from FCOFFS.components import *
from FCOFFS.interfaces import interface
from FCOFFS.utilities import units
from ..widgets import unit_entry, pipe_tab, injector_tab, inlet_tab, outlet_tab
from ..utilities import pop_ups

class ProjectPage(CTkFrame):
    def __init__(self, master: CTk, PS: PressureSystem.PressureSystem, **kwargs):
        super().__init__(master, **kwargs)

        self.PS = PS
        self.interfaces = []
        self.initialized = False

        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)

        self.top_bar_frm = CTkFrame(self)
        self.top_bar_frm.grid_columnconfigure((0, 1, 2), weight=1)
        self.top_bar_frm.grid_rowconfigure((0), weight=1)
        self.program_name = CTkLabel(self.top_bar_frm, text=" Fully Coupled One-Dimensional Framewokrk for Fluid Simultions", font=("Arial", 24))
        self.project_name = CTkLabel(self.top_bar_frm, text=f"Project: {PS.name} ", font=("Arial", 22))
        self.menu_frm = CTkFrame(self)
        self.menu_frm.grid_columnconfigure((0, 1), weight=1)
        self.menu_frm.grid_rowconfigure((0), weight=1)
        self.save_project_btn = CTkButton(self.menu_frm, text="SAVE", font=("Arial", 16), command=self.save_project)
        self.back_btn = CTkButton(self.menu_frm, text="RETURN", font=("Arial", 16), command=master.start_page)
        self.program_name.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")
        self.project_name.grid(row=0, column=1, pady=10, padx=10, sticky="nsew")
        self.save_project_btn.grid(row=0, column=0, pady=10, padx=(10, 5), sticky="nsew")
        self.back_btn.grid(row=0, column=1, pady=10, padx=(0, 10), sticky="nsew")
        self.top_bar_frm.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")
        self.menu_frm.grid(row=0, column=4, padx=5, pady=5, sticky="nsew")

        self.reference_frm = CTkFrame(self)
        self.reference_frm.grid_columnconfigure((0, 1), weight=1)
        self.reference_frm.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.reference_lbl = CTkLabel(self.reference_frm, text="System References", font=("Arial", 16), anchor="center")
        self.reference_temperature_lbl = CTkLabel(self.reference_frm, text="Reference Temperature:", font=("Arial", 12))
        self.reference_pressure_lbl = CTkLabel(self.reference_frm, text="Reference Pressure:", font=("Arial", 12))
        self.reference_pressure = unit_entry.UnitEntry(self.reference_frm, "PRESSURE", self.PS.ref_p)
        self.reference_temperature = unit_entry.UnitEntry(self.reference_frm, "TEMPERATURE", self.PS.ref_T)
        self.reference_set_btn = CTkButton(self.reference_frm, text="SET", font=("Arial", 14), command=self.set_ps_reference)
        self.reference_lbl.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.reference_temperature_lbl.grid(row=1, column=0, padx=(10, 5), pady=(5, 5), sticky="e")
        self.reference_temperature.grid(row=1, column=1, padx=(5, 10), pady=(5, 5), sticky="ns")
        self.reference_pressure_lbl.grid(row=2, column=0, padx=(10, 5), pady=(5, 5), sticky="e")
        self.reference_pressure.grid(row=2, column=1, padx=(5, 10), pady=(5, 5), sticky="ns")
        self.reference_set_btn.grid(row=3, column=0, columnspan=2, padx=10, pady=(10, 10))
        self.reference_frm.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.add_component_frm = CTkFrame(self)
        self.add_component_frm.grid_columnconfigure((0, 1), weight=1)
        self.add_component_frm.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.add_component_lbl = CTkLabel(self.add_component_frm, text="Add Component", font=("Arial", 16), anchor="center")
        self.new_component_name_lbl = CTkLabel(self.add_component_frm, text="New Component Name:", font=("Arial", 12))
        self.new_component_name_ent = CTkEntry(self.add_component_frm, font=("Arial", 12), placeholder_text="Name")
        self.new_component_type_lbl = CTkLabel(self.add_component_frm, text="New Component Type:", font=("Arial", 12))
        self.new_component_opt = CTkOptionMenu(self.add_component_frm, font=("Arial", 12), values=["Pipe", "Injector", "Inlet", "Outlet"])
        self.new_component_index_lbl = CTkLabel(self.add_component_frm, text="New Component Position:", font=("Arial", 12))
        self.new_component_index_opt = CTkOptionMenu(self.add_component_frm, font=("Arial", 12), values=[str(i) for i in range(len(self.PS.components) + 1)])
        self.add_component_btn = CTkButton(self.add_component_frm, text="ADD", font=("Arial", 12), command=self.add_component)
        self.add_component_lbl.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew") 
        self.new_component_name_lbl.grid(row=1, column=0, padx=(10, 5), pady= (5, 5), sticky="nse")
        self.new_component_name_ent.grid(row=1, column=1, padx=(5, 10), pady=(5, 5), sticky="nsew")
        self.new_component_type_lbl.grid(row=2, column=0, padx=(10, 5), pady= (5, 5), sticky="nse")
        self.new_component_opt.grid(row=2, column=1, padx=(5, 10), pady=(5, 5), sticky="ew")
        self.new_component_index_lbl.grid(row=3, column=0, padx=(10, 5), pady=(5, 5), sticky="nse")
        self.new_component_index_opt.grid(row=3, column=1, padx=(5, 10), pady=(5, 5), sticky="ew")
        self.add_component_btn.grid(row=4, column=0, columnspan=2, padx=10, pady=(10, 10))
        self.add_component_frm.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        self.components = CTkFrame(self)
        self.components_tabview = CTkTabview(self.components)
        for component in self.PS.components:
            tab = self.components_tabview.add(component.name)
            if isinstance(component, pipe.Pipe):
                frm = pipe_tab.PipeTab(tab, self, component)
                frm.pack(padx=5, pady=5, fill="both", expand=True)
            elif isinstance(component, injector.Injector):
                frm = injector_tab.InjectorTab(tab, self, component)
                frm.pack(padx=5, pady=5, fill="both", expand=True)
            elif isinstance(component, interface.PressureInlet):
                frm = inlet_tab.InletTab(tab, self, component)
                frm.pack(padx=5, pady=5, fill="both", expand=True)
            elif isinstance(component, interface.PressureOutlet):  
                frm = inlet_tab.InletTab(tab, self, component)
                frm.pack(padx=5, pady=5, fill="both", expand=True)
        self.components_tabview.pack(padx=5, pady=5, fill="both", expand=True)
        self.components.grid(row=1, column=2, columnspan=3, padx=5, pady=5, sticky="nsew")

        self.buttons = CTkFrame(self)
        self.buttons.grid_columnconfigure((0), weight=1)
        self.buttons.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.initialize_btn = CTkButton(self.buttons, text="Initialize System", command=self.initialize, font=("Arial", 16))
        self.system_tree_btn = CTkButton(self.buttons, text="System Diagram", command=self.show_system_diagram, font=("Arial", 16))
        self.solve_btn = CTkButton(self.buttons, text="Solve System", command=self.solve, font=("Arial", 16))
        self.system_output_btn = CTkButton(self.buttons, text="System State", command=self.show_system_state, font=("Arial", 16))
        self.initialize_btn.grid(row=0, column=0, padx=10, pady=(20, 10), sticky="nsew")
        self.system_tree_btn.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="nsew")
        self.solve_btn.grid(row=2, column=0, padx=10, pady=(5, 10), sticky="nsew")
        self.system_output_btn.grid(row=3, column=0, padx=10, pady=(5, 20), sticky="nsew")
        self.buttons.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

        # self.display_frm = CTkFrame(self)
        # self.display_frm.grid_columnconfigure((0, 1), weight=1)
        # self.display_frm.grid_rowconfigure((0), weight=1)
        self.display_text = CTkTextbox(self, font=("arial", 14), state="disabled", wrap="word")
        self.display_text.grid(row=2, column=1, columnspan=4, padx=5, pady=5, sticky="nsew")
        #self.display_frm.grid(row=2, column=1, columnspan=4, padx=5, pady=5, sticky="nsew")

    def set_ps_reference(self):
        self.PS.ref_p = self.reference_pressure.unit
        self.PS.ref_T = self.reference_temperature.unit

    def add_component(self) -> None:
        component_type = self.new_component_opt.get()
        component_name = self.new_component_name_ent.get()

        if not component_name:
            pop_ups.gui_error("Component Name Cannot be Nothing")
            return

        match component_type:
            case "Pipe":
                comp = pipe.Pipe(self.PS, units.UnitValue("METRIC", "DISTANCE", "m", 1), "N2O", component_name, units.UnitValue("METRIC", "DISTANCE", "m", 1))
                tab = self.components_tabview.insert(int(self.new_component_index_opt.get()), component_name)
                frm = pipe_tab.PipeTab(tab, self, comp)
                frm.pack(padx=5, pady=5, fill="both", expand=True)
                self.PS.components.insert(int(self.new_component_index_opt.get()), comp)
                self.new_component_index_opt.configure(values=[str(i) for i in range(len(self.PS.components) + 1)])
                frm._change_move_options()
            case "Injector":
                comp = injector.Injector(self.PS, units.UnitValue("METRIC", "DISTANCE", "m", 1), units.UnitValue("METRIC", "DISTANCE", "m", 1), units.UnitValue("METRIC", "DISTANCE", "m", 1), 1, "N2O", component_name)
                tab = self.components_tabview.insert(int(self.new_component_index_opt.get()), component_name)
                frm = injector_tab.InjectorTab(tab, self, comp)
                frm.pack(padx=5, pady=5, fill="both", expand=True)
                self.PS.components.insert(int(self.new_component_index_opt.get()), comp)
                self.new_component_index_opt.configure(values=[str(i) for i in range(len(self.PS.components) + 1)])
                frm._change_move_options()
            case "Inlet":
                comp = interface.PressureInlet(units.UnitValue("Imperial", "PRESSURE", "psi", 1), units.UnitValue("METRIC", "TEMPERATURE", "c", 1), component_name)
                tab = self.components_tabview.insert(int(self.new_component_index_opt.get()), component_name)
                frm = inlet_tab.InletTab(tab, self, comp)
                frm.pack(padx=5, pady=5, fill="both", expand=True)
                self.interfaces.insert(0, comp)
                self.new_component_index_opt.configure(values=[str(i) for i in range(len(self.PS.components) + 1)])
                #frm._change_move_options()
            case "Outlet":
                comp = interface.PressureOutlet(units.UnitValue("Imperial", "PRESSURE", "psi", 1), component_name)
                tab = self.components_tabview.insert(int(self.new_component_index_opt.get()), component_name)
                frm = outlet_tab.OutletTab(tab, self, comp)
                frm.pack(padx=5, pady=5, fill="both", expand=True)
                self.interfaces.append(comp)
                self.new_component_index_opt.configure(values=[str(i) for i in range(len(self.PS.components) + 1)])
                #frm._change_move_options()

    def initialize(self) -> None:
        try:
            if self.initialized:
                self.interfaces = [self.interfaces[0], self.interfaces[-1]]
            for i in range(len(self.PS.components) - 1):
                inter = interface.Interface(f"INTER{i + 1}")
                self.interfaces.insert(1, inter)
            
            i = 0
            j = 1
            for comp in self.PS.components:
                comp.set_connection(self.interfaces[i], self.interfaces[j])
                i += 1
                j += 1
            
            self.PS.initialize(self.PS.components, "PressureInlet", "PressureOutlet")
            self.initialized = True
        except Exception as e:
            pop_ups.gui_error(f"Initialization Failed Due To: {e}")

    def show_system_diagram(self) -> None:
        self.display_text.insert(END, "\n")
        for i in range(len(self.objects)-1):
            self.display_text.insert(END, str(self.PS.objects[i].name))
            self.display_text.insert(END, "\n|\n")
        self.display_text.insert(END, f"{self.PS.objects[i].name}\n")  

    def solve(self) -> None:
        if self.initialized:
            try:
                self.PS.solve()
            except Exception as e:
                pop_ups.gui_error(f"Solve Failed Due To: {e}")
        else:
            pop_ups.gui_error("System Not Yet Initialized")

    def show_system_state(self) -> None:
        try:
            output = self.PS.output(False)
            self.display_text.insert(END, f"\n\n{output}\n\n")
        except Exception as e:
            pop_ups.gui_error(f"System State Display Failed Due To: {e}")
         

    def save_project(self) -> None:
        try:
            path = os.path.join(os.getcwd(), "UI", "Saved Projects")
            if not os.path.exists(path):
                os.makedirs(path)
            with open(os.path.join(path, f"{self.PS.name}.fcoffs"), "wb") as file:
                pickle.dump(self.PS, file)
            pop_ups.gui_popup("Sucessfully Saved the Project")
        except Exception as e:
            pop_ups.gui_error(f"Was unable to save the project due to: {e}")

