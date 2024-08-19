
from typing import Any
from customtkinter import *
import pickle
import os

from FCOFFS.pressureSystem import PressureSystem
from ..utilities import pop_ups

class StartPage(CTkFrame):
    def __init__(self, master: CTk, func: Any, **kwargs):
        super().__init__(master, **kwargs)
        self.func = func
        #self.load_project_func = load_func

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        title_frm = CTkFrame(self)
        self.title = CTkLabel(title_frm, text="Start Page", text_color="lightblue", font=("Arial", 30), anchor="center")
        self.title.pack(pady=20, fill="both", expand=True)
        buttons_frm = CTkFrame(self)
        buttons_frm.grid_columnconfigure((0, 1, 2), weight=1)
        buttons_frm.grid_rowconfigure((0, 1), weight=1)
        self.new_project_title = CTkLabel(buttons_frm, text="New Project:", font=("Arial", 20), anchor="center")
        self.new_project_title.grid(row=0, column=0, padx=(10, 5), pady=(10, 15), sticky="e")
        self.project_name_ent = CTkEntry(buttons_frm, font=("Arial", 14), width=90, placeholder_text="New Project Name")
        self.project_name_ent.grid(row=0, column=1, padx=(5, 5), pady=(10, 15), sticky="ew")
        self.new_btn = CTkButton(buttons_frm, text="Create Project", font=("Arial", 18), anchor="center", command=self.new_project)
        self.new_btn.grid(row=0, column=2, padx=(5, 10), pady=(10, 15), sticky="ew")
        self.load_project_title = CTkLabel(buttons_frm, text="Existing Project:", font=("Arial", 20), anchor="center")
        self.load_project_title.grid(row=1, column=0, padx=(10, 5), pady=(15, 10), sticky="e")
        self.file_opt = CTkOptionMenu(buttons_frm, font=("Arial", 14), values=self._get_available_projects())
        self.file_opt.grid(row=1, column=1,  padx=(5, 5), pady=(15, 10), sticky="ew")
        self.load_btn = CTkButton(buttons_frm, text="Load Project", font=("Arial", 18), anchor="center", command=self.load_project)
        self.load_btn.grid(row=1, column=2, padx=(5, 10), pady=(15, 10), sticky="ew")

        title_frm.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        buttons_frm.grid(row=1, rowspan=2, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

    def new_project(self) -> None:
        project_name = self.project_name_ent.get()
        if project_name:
            self.func(PressureSystem.PressureSystem(project_name))
        else:
            pop_ups.gui_error("Invalid Project Name")

    def load_project(self) -> None:
        try:
            if self.file_opt.get() == "None":
                pop_ups.gui_error(f"No Project to Open")
                return
            with open(os.path.join(os.getcwd(), "UI", "Saved Projects", self.file_opt.get()), "rb") as file:
                pressure_system = pickle.load(file)
        except Exception as e:
            pop_ups.gui_error(f"Failed to Load Project: {e}")
            return
        self.func(pressure_system)

    def _get_available_projects(self) -> list:
        cur_dir = os.path.join(os.getcwd(), "UI", "Saved Projects")
        if os.path.exists(cur_dir):
            available_files = []
            dir_items = os.scandir(cur_dir)
            for itm in dir_items:
                if os.path.splitext(itm.name)[1] == ".fcoffs":
                    available_files.append(itm.name)
            return available_files
        else:
            os.makedirs(cur_dir)
        return ["None"]