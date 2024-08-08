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
        self.page = start.StartPage(self, self.start_program)
        self.page.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.mainloop()

    def __clear(self) -> None:
        for child in self.children.copy():
            self.children[child].destroy() 

    def start_program(self, pressure_system: PressureSystem.PressureSystem = None) -> None:
        self.__clear()
        if pressure_system is None:
            pass
        else:
            pass