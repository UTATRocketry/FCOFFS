
from typing import Any, Tuple
from customtkinter import *
import pickle

from ..utilities import pop_ups

class StartPage(CTkFrame):
    def __init__(self, master: Any, func: Any, width: int = 200, height: int = 200, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, border_color: str | Tuple[str, str] | None = None, background_corner_colors: Tuple[str | Tuple[str, str]] | None = None, overwrite_preferred_drawing_method: str | None = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        self.func = func
        #self.load_project_func = load_func

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.title = CTkLabel(self, text="Start Page", text_color="lightblue", font=("Arial", 30))
        self.title.grid(row=0, column=0, columnspan=2, padx=15, pady=20, sticky="nsew")
        self.project_name_ent = CTkEntry(self, font=("Arial", 14), width=90, placeholder_text="New Project Name")
        self.project_name_ent.grid(row=1, column=0, padx=(10, 5), pady=10, sticky="nsew")
        self.new_btn = CTkButton(self, text="New Project", font=("Arial", 18), anchor="center", command=self.new_project)
        self.new_btn.grid(row=1, column=1, padx=(0, 10), pady=10, sticky="nsew")
        self.file_opt = CTkOptionMenu(self, font=("Arial", 14), values=None)
        self.file_opt.grid(row=2, column=0,  padx=(10, 5), pady=10, sticky="nsew")
        self.load_btn = CTkButton(self, text="Load Project", font=("Arial", 18), anchor="center", command=self.load_project)
        self.load_btn.grid(row=2, column=1, padx=(0, 10), pady=10, sticky="nsew")
        
    def new_project(self) -> None:
        project_name = self.project_name_ent.get()
        if project_name:
            self.func()
        else:
            pop_ups.gui_error("Invalid Project Name")

    def load_project(self) -> None:
        try:
            pressure_system = pickle.load(self.file_opt.get())
            self.func(pressure_system)
        except Exception as e:
            pop_ups.gui_error(f"Failed to Load Project: {e}")

    def _get_available_projects(self) -> list:
        pass