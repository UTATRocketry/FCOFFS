from typing import Any
from customtkinter import *

from FCOFFS.utilities import units
from ..utilities.pop_ups import gui_error

class UnitEntry(CTkFrame):
    def __init__(self, master: Any, dimension: str, value: Any = 0, **kwargs):
        super().__init__(master, **kwargs)

        self.dimension = dimension

        if dimension not in units.UnitValue.UNITS["METRIC"]:
            gui_error(f"Dimension not valid must be one of the following: {units.UnitValue.UNITS['METRIC']}")
            return
        
        unit = list(units.UnitValue.UNITS["METRIC"][dimension].keys())
        unit += list(units.UnitValue.UNITS["IMPERIAL"][dimension].keys())

        self.grid_rowconfigure((0), weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        self.value_ent = CTkEntry(self, placeholder_text="Value", font=("Arial", 12), width=90)
        self.unit_opt = CTkOptionMenu(self, font=("Arial", 12), values=unit, width=85, command=self.__convert)
        self.value_ent.grid(row=0, column=0, padx=(10, 3), pady=5)
        self.unit_opt.grid(row=0, column=1, padx=(0, 10), pady=5)

        self.__set(value)
        self.unit()

    def __set(self, value: Any) -> None:
        self.value_ent.delete(0, END)
        if isinstance(value, units.UnitValue):
            self.value_ent.insert(0, value())
            self.unit_opt.set(value.unit)
            self.cur_unit = value
        elif isinstance(value, str):
            self.value_ent.insert(0, value)
        elif isinstance(value, int) or isinstance(value, float):
            self.value_ent.insert(0, str(value))
        else:
            gui_error(f"Invalid type for setting UnitEntry Box, must be type str or UnitValue, but was type {type(value)}")
        
    def __convert(self, choice):
        if self.cur_unit:
            self.cur_unit.to(choice)
            self.__set(self.cur_unit)
        else:
            self.unit_opt.set(choice)

    def unit(self) -> units.UnitValue:
        try:
            if self.unit_opt.get() in units.UnitValue.UNITS["METRIC"][self.dimension]:
                self.cur_unit = units.UnitValue("METRIC", self.dimension, self.unit_opt.get(), float(self.value_ent.get()))
            else:
                self.cur_unit = units.UnitValue("IMPERIAL", self.dimension, self.unit_opt.get(), float(self.value_ent.get()))
        except Exception as e:
            gui_error(f"Invalid Input Value, Must be a number, not a string| {e}")
            return units.UnitValue(None, None, "", 0)
        return self.cur_unit
        
  
if __name__ == "__main__":

    main = CTk()
    set_appearance_mode('dark') 
    set_default_color_theme('blue')
    temp = UnitEntry(main, "DISTANCE", 1)
    temp.pack(padx=5, pady=5, fill="both", expand=True)

    def update():
        test = temp.unit()

    but = CTkButton(main, text="set", command=update)
    but.pack()
    main.mainloop()

    


