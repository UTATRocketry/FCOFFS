from typing import Any, Tuple
from customtkinter import *
from pages import *

class main(CTk):
    def __init__(self, Title: str = "FCOFFS", color_theme: str = "blue", apearance_mode: str = "dark", fg_color: str | Tuple[str] | None = None, **kwargs):
        super().__init__(fg_color, **kwargs)

        set_appearance_mode(apearance_mode) 
        set_default_color_theme(color_theme) 
        self.title(Title)

        self.mainloop()

    def clear(self):
        pass