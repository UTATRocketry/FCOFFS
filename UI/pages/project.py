
from typing import Any
from customtkinter import *
import pickle
from queue import Queue
from _thread import *

from FCOFFS.pressureSystem import PressureSystem
from FCOFFS.components import *
from FCOFFS.interfaces import interface
from FCOFFS.utilities import units
from ..widgets import pressure_inlet_tab, pressure_outlet_tab, unit_entry, pipe_tab, injector_tab, mass_outlet_tab
from ..utilities import pop_ups

class ProjectPage(CTkFrame):
    def __init__(self, master: CTk, PS: PressureSystem.PressureSystem, **kwargs):
        super().__init__(master, **kwargs)

        self.PS = PS
        self.interfaces = []
        self.PS.initialized = False

        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        self.top_bar_frm = CTkFrame(self)
        self.top_bar_frm.grid_columnconfigure((0, 1, 2), weight=1)
        self.top_bar_frm.grid_rowconfigure((0), weight=1)
        self.program_name = CTkLabel(self.top_bar_frm, text=" Fully Coupled One-Dimensional Framework for Fluid Simulations", font=("Arial", 24))
        self.project_name = CTkLabel(self.top_bar_frm, text=f"Project: {PS.name} ", font=("Arial", 22))
        self.program_name.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")
        self.project_name.grid(row=0, column=1, pady=10, padx=10, sticky="nsew")
        self.top_bar_frm.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")
        self.menu_opt = CTkOptionMenu(self, font=("Arial", 26), dropdown_font=("Arial", 20), values=["SAVE", "RETURN"], fg_color="black" ,button_color="black", button_hover_color="black", anchor="center", command=self.menu_func) 
        self.menu_opt.set("MENU")
        self.menu_opt.grid(row=0, column=4, padx=5, pady=5, sticky="nsew")
        

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
        self.new_component_opt = CTkOptionMenu(self.add_component_frm, font=("Arial", 12), values=["Pressure Inlet", "Pipe", "Injector", "Pressure Outlet", "Mass Outlet"])
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
            elif isinstance(component, pressure_inlet.PressureInlet):
                frm = pressure_inlet_tab.PressureInletTab(tab, self, component)
                frm.pack(padx=5, pady=5, fill="both", expand=True)
            elif isinstance(component, pressure_outlet.PressureOutlet):  
                frm = pressure_outlet_tab.PressureOutletTab(tab, self, component)
                frm.pack(padx=5, pady=5, fill="both", expand=True)
            elif isinstance(component, mass_flow_outlet.MassFlowOutlet):
                frm = mass_outlet_tab.MassOutletTab(tab, self, component)
                frm.pack(padx=5, pady=5, fill="both", expand=True)
        self.components_tabview.pack(padx=5, pady=5, fill="both", expand=True)
        self.components.grid(row=1, column=2, columnspan=3, padx=5, pady=5, sticky="nsew")

        self.buttons = CTkFrame(self)
        self.buttons.grid_columnconfigure((0), weight=1)
        self.buttons.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.initialize_btn = CTkButton(self.buttons, text="Initialize System", command=self.initialize, font=("Arial", 16))
        self.system_tree_btn = CTkButton(self.buttons, text="System Diagram", command=self.show_system_diagram, font=("Arial", 16))
        self.solve_btn = CTkButton(self.buttons, text="Solve System", command=self.solve, font=("Arial", 16))
        self.system_output_btn = CTkButton(self.buttons, text="System Output", command=self.show_system_state, font=("Arial", 16))
        self.initialize_btn.grid(row=0, column=0, padx=10, pady=(20, 10), sticky="nsew")
        self.system_tree_btn.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="nsew")
        self.solve_btn.grid(row=2, column=0, padx=10, pady=(5, 10), sticky="nsew")
        self.system_output_btn.grid(row=3, column=0, padx=10, pady=(5, 20), sticky="nsew")
        self.buttons.grid(row=2, rowspan=2, column=0, padx=5, pady=5, sticky="nsew")

        self.display_text = CTkTextbox(self, font=("arial", 14), state="disabled", wrap="word")
        self.display_text.grid(row=2, rowspan=2, column=1, columnspan=4, padx=5, pady=5, sticky="nsew")

    def set_ps_reference(self):
        self.PS.ref_p = self.reference_pressure.unit.convert_base_metric()
        self.PS.ref_T = self.reference_temperature.unit.convert_base_metric()
        self.write_to_display(f"\nUpdated System References: Pressure = {self.PS.ref_p}, Temperature = {self.PS.ref_T}\n")

    def add_component(self) -> None:
        component_type = self.new_component_opt.get()
        component_name = self.new_component_name_ent.get()

        if not component_name:
            pop_ups.gui_error("Component Name Cannot be Nothing")
            return
        elif component_name in self.components_tabview._name_list:
            pop_ups.gui_error("Component Name Already Exists")
            return

        match component_type:
            case "Pipe":
                comp = pipe.Pipe(self.PS, units.UnitValue("METRIC", "DISTANCE", "m", 1), "N2O", component_name, units.UnitValue("METRIC", "DISTANCE", "m", 1))
                tab = self.components_tabview.insert(int(self.new_component_index_opt.get()), component_name)
                frm = pipe_tab.PipeTab(tab, self, comp)   
            case "Injector":
                comp = injector.Injector(self.PS, units.UnitValue("METRIC", "DISTANCE", "m", 1), units.UnitValue("METRIC", "DISTANCE", "m", 1), units.UnitValue("METRIC", "DISTANCE", "m", 1), 1, "N2O", component_name)
                tab = self.components_tabview.insert(int(self.new_component_index_opt.get()), component_name)
                frm = injector_tab.InjectorTab(tab, self, comp)    
            case "Pressure Inlet":
                comp = pressure_inlet.PressureInlet(self.PS, units.UnitValue("METRIC", "DISTANCE", "m", 1), "N2O", units.UnitValue("IMPERIAL", "PRESSURE", "psi", 1), units.UnitValue("METRIC", "TEMPERATURE", "c", 1), component_name)
                tab = self.components_tabview.insert(int(self.new_component_index_opt.get()), component_name)
                frm = pressure_inlet_tab.PressureInletTab(tab, self, comp)   
            case "Pressure Outlet":
                comp = pressure_outlet.PressureOutlet(self.PS, units.UnitValue("METRIC", "DISTANCE", "m", 1), "N2O", units.UnitValue("IMPERIAL", "PRESSURE", "psi", 1), component_name)
                tab = self.components_tabview.insert(int(self.new_component_index_opt.get()), component_name)
                frm = pressure_outlet_tab.PressureOutletTab(tab, self, comp)
            case "Mass Outlet":
                comp = mass_flow_outlet.MassFlowOutlet(self.PS, units.UnitValue("METRIC", "DISTANCE", "m", 1), "N2O", units.UnitValue("METRIC", "MASS FLOW RATE", "kg/s", 1), component_name)
                tab = self.components_tabview.insert(int(self.new_component_index_opt.get()), component_name)
                frm = mass_outlet_tab.MassOutletTab(tab, self, comp)
                
        frm.pack(padx=5, pady=5, fill="both", expand=True)
        self.PS.components.insert(int(self.new_component_index_opt.get()), comp)
        self.new_component_index_opt.configure(values=[str(i) for i in range(len(self.PS.components) + 1)])
        frm._change_move_options()


    def initialize(self) -> None:
        try:
            self.PS.objects = []
            if not isinstance(self.PS.components[0], (pressure_inlet.PressureInlet)):
                pop_ups.gui_error("System does not start with an Inlet please change system")
            if not isinstance(self.PS.components[-1], (pressure_outlet.PressureOutlet, mass_flow_outlet.MassFlowOutlet)):
                pop_ups.gui_error("System does not end with an Outlet please change system")
            
            for i, comp in enumerate(self.PS.components):
                next_interface = interface.Interface(f"Interface {i+1}")
                if isinstance(comp, (pressure_inlet.PressureInlet)):
                    comp.set_connection(downstream=next_interface)
                elif isinstance(comp, (pressure_outlet.PressureOutlet, mass_flow_outlet.MassFlowOutlet)):
                    comp.set_connection(upstream=prev_interface)
                else:
                    comp.set_connection(prev_interface, next_interface)
                prev_interface = next_interface

            self.PS.initialize(self.PS.components)
            self.PS.initialized = True
            self.write_to_display("\nSystem Initialized Succesffuly \n")
        except Exception as e:
            pop_ups.gui_error(f"Initialization Failed Due To: {e}")

    def show_system_diagram(self) -> None:
        res_string = "\n"
        for i in range(len(self.PS.objects)-1):
            res_string += str(self.PS.objects[i].name) + "\n  |\n"
        res_string += f"{self.PS.objects[i+1].name}\n"
        self.write_to_display(res_string)

    def solve(self) -> None:
        def solve_system(queue: Queue):
            if self.PS.initialized:
                try:
                    self.PS.solve(verbose=False, queue=queue)
                    queue.put("DONE")
                    return
                except Exception as e:
                    queue.put(f"ERROR:Solve Failed Due To: {e}")
            else:
                queue.put("ERROR:System Not Yet Initialized")
            return
        
        q = Queue()
        iter = 1
        start_new_thread(solve_system, tuple([q]))
        while True:
            out = q.get()
            if out == "DONE":
                self.write_to_display("\nFinsihed Solving System \n")
                return
            elif isinstance(out, str) and len(out) > 5 and out[:5] == "ERROR":
                pop_ups.gui_error(out[6:-1])
                return
            else:
                self.write_to_display(f"\nIteration:{iter}, Residual = {out}\n")
            iter += 1

    def show_system_state(self) -> None:
        try:
            output = self.PS.output(False)
            self.write_to_display("\n" + output)
        except Exception as e:
            pop_ups.gui_error(f"System State Display Failed Due To: {e}")
         
    def write_to_display(self, text: str="", pos=END):
        self.display_text.configure(state="normal")
        self.display_text.insert(pos, text)
        self.display_text.configure(state="disabled")
        self.display_text.see(END)

    def menu_func(self, choice):
        match choice:
            case "SAVE":
                self.save_project()
            case "RETURN":
                self.master.start_page()

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

