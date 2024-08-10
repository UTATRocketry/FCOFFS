from typing import Any
import customtkinter as CTk

from FCOFFS.utilities import units

class UnitEntry(CTk.CTkFrame):
    def __init__(self, master: Any, dimension: str, value: Any = 0, **kwargs):
        super().__init__(master, **kwargs)

        self.dimension = dimension

        if dimension not in units.UnitValue.UNITS["METRIC"]:
            raise Exception(f"Dimension not valid must be one of the following: {units.UnitValue.UNITS['METRIC']}")
        
        unit = list(units.UnitValue.UNITS["METRIC"][dimension].keys())
        unit += list(units.UnitValue.UNITS["IMPERIAL"][dimension].keys())

        self.grid_rowconfigure((0), weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        self.value_ent = CTk.CTkEntry(self, placeholder_text="Value", font=("Arial", 12), width=120)
        self.unit_opt = CTk.CTkOptionMenu(self, font=("Arial", 12), values=unit, width=100, command=self.__convert)
        self.value_ent.grid(row=0, column=0, padx=(10, 3), pady=5, sticky="ns")
        self.unit_opt.grid(row=0, column=1, padx=(0, 10), pady=5, sticky="ns")

        self.__set(value)

    def __set(self, value: Any) -> None:
        self.value_ent.delete(0, CTk.END)
        if isinstance(value, units.UnitValue):
            self.value_ent.insert(0, value())
            self.unit_opt.set(value.get_unit)
            self.cur_unit = value
        elif isinstance(value, str):
            self.value_ent.insert(0, value)
        elif isinstance(value, int) or isinstance(value, float):
            self.value_ent.insert(0, str(value))
        else:
            raise Exception(f"Invalid type for setting UnitEntry Box, must be type str or UnitValue, but was type {type(value)}")
        
    def __convert(self, choice):
        if self.cur_unit:
            self.cur_unit.to(choice)
            self.__set(self.cur_unit)
        else:
            self.unit_opt.set(choice)

    @property
    def unit(self) -> units.UnitValue:
        if self.unit_opt.get() in units.UnitValue.UNITS["METRIC"][self.dimension]:
            self.cur_unit = units.UnitValue("METRIC", self.dimension, self.unit_opt.get(), float(self.value_ent.get()))
        else:
            self.cur_unit = units.UnitValue("IMPERIAL", self.dimension, self.unit_opt.get(), float(self.value_ent.get()))
        return self.cur_unit
        
  

        