from typing import Any
from customtkinter import *
import pickle

from FCOFFS.pressureSystem import PressureSystem

class ProjectPage(CTkFrame):
    def __init__(self, master: CTk, PS: PressureSystem.PressureSystem, **kwargs):
        super().__init__(master, **kwargs)

        self.PS = PS

        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

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
        self.top_bar_frm.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
        self.button_frm.grid(row=0, column=3, padx=5, pady=5, sticky="nsew")

        self.add_component_frm = CTkFrame(self)

    def save_project(self):
        path = os.path.join(os.getcwd(), "UI", "Saved Projects")
        if not os.path.exists(path):
            os.makedirs(path)
        with open(os.path.join(path, f"{self.PS.name}.fcoffs"), "wb") as file:
            pickle.dump(self.PS, file)


