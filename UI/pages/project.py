from typing import Any
from customtkinter import *
import pickle

from FCOFFS.pressureSystem import PressureSystem
from ..widgets import unit_entry

class ProjectPage(CTkFrame):
    def __init__(self, master: CTk, PS: PressureSystem.PressureSystem, **kwargs):
        super().__init__(master, **kwargs)

        self.PS = PS

        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)

        self.top_bar_frm = CTkFrame(self)
        self.top_bar_frm.grid_columnconfigure((0, 1, 2), weight=1)
        self.top_bar_frm.grid_rowconfigure((0), weight=1)
        self.program_name = CTkLabel(self.top_bar_frm, text=" Fully Coupled One-Dimensional Framewokrk for Fluid Simultions   |", font=("Arial", 24))
        self.project_name = CTkLabel(self.top_bar_frm, text=f"Project: {PS.name} ", font=("Arial", 22))
        self.button_frm = CTkFrame(self)
        self.button_frm.grid_columnconfigure((0, 1), weight=1)
        self.button_frm.grid_rowconfigure((0), weight=1)
        self.save_project_btn = CTkButton(self.button_frm, text="SAVE", font=("Arial", 16), command=self.save_project)
        self.back_btn = CTkButton(self.button_frm, text="RETURN", font=("Arial", 16), command=master.start_page)
        self.program_name.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")
        self.project_name.grid(row=0, column=1, pady=10, padx=10, sticky="nsew")
        self.save_project_btn.grid(row=0, column=0, pady=10, padx=(10, 5), sticky="nsew")
        self.back_btn.grid(row=0, column=1, pady=10, padx=(0, 10), sticky="nsew")
        self.top_bar_frm.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")
        self.button_frm.grid(row=0, column=4, padx=5, pady=5, sticky="nsew")

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
        self.reference_set_btn.grid(row=3, column=0, columnspan=2, padx=10, pady=(10, 10), sticky="ns")
        self.reference_frm.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.add_component_frm = CTkFrame(self)
        self.add_component_frm.grid_columnconfigure((0, 1), weight=1)
        self.add_component_frm.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.component_lbl = CTkLabel(self.add_component_frm, text="System Components", font=("Arial", 16), anchor="center")
        self.num_components_lbl =  CTkLabel(self.add_component_frm, text=f"Number of Components: {len(self.PS.components)}", font=("Arial", 12))
        self.add_component_lbl = CTkLabel(self.add_component_frm, text="Add Component", font=("Arial", 16), anchor="center")
        self.new_component_opt = CTkOptionMenu(self.add_component_frm, font=("Arial", 14), values=["Pipe", "Injector"])
        self.add_component_btn = CTkButton(self.add_component_frm, text="ADD", font=("Arial", 14), command=self.add_component)
        self.component_lbl.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.num_components_lbl.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="nsw")
        self.add_component_lbl.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.new_component_opt.grid(row=3, column=0, padx=(10, 5), pady=(5, 10), sticky="nsew")
        self.add_component_btn.grid(row=3, column=1, padx=(0, 10), pady=(5, 10), sticky="nsew")
        self.add_component_frm.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

    def set_ps_reference(self):
        self.PS.ref_p = self.reference_pressure.unit
        self.PS.ref_T = self.reference_temperature.unit

    def add_component(self):
        pass

    def save_project(self):
        path = os.path.join(os.getcwd(), "UI", "Saved Projects")
        if not os.path.exists(path):
            os.makedirs(path)
        with open(os.path.join(path, f"{self.PS.name}.fcoffs"), "wb") as file:
            pickle.dump(self.PS, file)


