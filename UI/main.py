from typing import Any, Tuple
from customtkinter import *

from FCOFFS.pressureSystem import PressureSystem
from .pages import *

class Application(CTk):
    def __init__(self, Title: str = "FCOFFS", color_theme: str = "blue", apearance_mode: str = "dark", fg_color: str | Tuple[str] | None = None, **kwargs):
        super().__init__(fg_color, **kwargs)

        set_appearance_mode(apearance_mode) 
        set_default_color_theme(color_theme) 
        self.title(Title)
        self.page = start.StartPage(self, self.project_page)
        self.page.pack(padx=5, pady=5, fill="both", expand=True)
        self.mainloop()

    def __clear(self) -> None:
        for child in self.children.copy():
            self.children[child].destroy() 

    def start_page(self):
        self.__clear()
        self.page = start.StartPage(self, self.project_page)
        self.page.pack(padx=5, pady=5, fill="both", expand=True)

    def project_page(self, pressure_system: PressureSystem.PressureSystem) -> None:
        self.__clear()
        self.PS = pressure_system
        self.page = project.ProjectPage(self, self.PS)
        self.page.pack(padx=1, pady=1, fill="both", expand=True)
        
