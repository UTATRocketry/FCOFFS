'''
This module allows you to easly store numbers with units and easily convert the units and value of the numbers.
The two supported systems currently are Imperial and Metric. 
It currently suports numbers of the unit type 'DISTANCE', 'PRESSURE', 'MASS', 'VELOCITY', 'DENSITY', 'VOLUME', "AREA", "TEMPERATURE", "MASS FLOW RATE", "ENERGY".
Typically used units are supported and more can be added upon request.
'''

from enum import Enum

class UnitPressure(Enum):
    Pa = 1
    psi = 6894.76


class UnitLength(Enum):
    m = 1
    inch = 0.0254


def convert_to_si(quantity):
    if not isinstance(quantity, tuple):
        return quantity
    return quantity[0] * quantity[1].value


def convert_from_si(quantity):
    if not isinstance(quantity, tuple):
        return quantity
    return quantity[0] / quantity[1].value


class UnitValue:  # could add more units and a create value button that returns a UNit Value object given a unit and value.
    UNITS = {"IMPERIAL": {
                           "DISTANCE": {"in": 0.0254, "mi": 1609.34, "yd": 0.9144, "ft": 0.3048}, 
                           "PRESSURE": {"psi": 6894.76, "psf": 47.8803}, 
                           "MASS": {"lb": 0.453592, "ton": 907.1847,"st": 6.35029, "oz": 0.0283495}, 
                           "VELOCITY": {"ft/s": 0.3048, "mi/s": 1609.34, "mph": 0.44704, "in/s": 0.0254}, 
                           "DENSITY": {"lb/in^3": 27679.9, "lb/ft^3": 16.0185, "lb/yd^3": 0.593276},
                           "VOLUME": {"gal": 0.00378541, "yd^3": 0.764555, "ft^3": 0.0283168, "in^3": 0.0000163871}, 
                           "AREA": {"in^2": 0.00064516, "mi^2": 2590000, "yd^2": 0.836127, "ft^2": 0.092903},
                           "TEMPERATURE": {"f": None},
                           "MASS FLOW RATE": {"lb/s": 0.453592, "ton/s": 907.1847, "st/s": 6.35029, "oz": 0.0283495, "lb/min": 0.00755987},
                           "ENERGY": {"ftlb": 1.35582, "kcal": 4184, "cal": 4.184}
                         }, 
             "METRIC": {
                         "DISTANCE": {"m": 1, "km": 1000, "cm": 0.01, "mm": 0.001}, 
                         "PRESSURE": {"Pa": 1, "MPa": 1000000, "bar": 100000, "kPa": 1000, "hPa": 100}, 
                         "MASS": {"kg": 1, "tonne": 1000, "g": 0.001}, 
                         "VELOCITY": {"m/s": 1, "km/s": 1000, "km/h": 0.277778, "cm/s": 0.01, "mm/s": 0.001}, 
                         "DENSITY": {"kg/m^3": 1, "t/m^3": 1000, "g/m^3": 0.001},
                         "VOLUME": {"m^3": 1, "L": 0.001, "cm^3": 0.000001, "mm^3": 0.000000001},
                         "AREA": {"m^2": 1, "km^2": 1000000, "cm^2": 0.0001, "mm^2": 0.000001},
                         "TEMPERATURE": {"k": None, "c": None},
                         "MASS FLOW RATE": {"kg/s": 1, "t/s": 1000, "kg/min": 0.0166667, "g/s": 0.001},
                         "ENERGY": {"J": 1, "MJ": 1000000, "kJ": 1000, "Nm": 1, "kgm^2/s^2": 1, "eV": 1.602177e-19}
                        }
            }
    
    @classmethod
    def available_units(cls, system: str="", dimension: str="") -> str:
        '''param:'''
        if system:
            if system not in UnitValue.UNITS.keys():
                raise Exception(f"Unit system {system} invalid: Must be 'IMPERIAL' or 'METRIC'")
            if dimension:
                if dimension not in UnitValue.UNITS[system].keys():
                    raise Exception(f"Measurement Type {dimension} invalid: Must be 'DISTANCE', 'PRESSURE', 'MASS', 'VELOCITY', 'DENSITY', 'VOLUME', 'AREA', 'TEMPERATURE', 'MASS FLOW RATE', 'ENERGY'")
                return f"{system} {dimension}: {list(UnitValue.UNITS[system][dimension].keys())}"
            else:
                temp = ""
                for key in UnitValue.UNITS[system].keys():
                    temp += f"{key}: {list(UnitValue.UNITS[system][key].keys())}\n"
                return f"{system}:\n{temp}"
        elif dimension:
            if dimension not in UnitValue.UNITS["METRIC"].keys():
                raise Exception(f"Measurement Type {dimension} invalid: Must be 'DISTANCE', 'PRESSURE', 'MASS', 'VELOCITY', 'DENSITY', 'VOLUME', 'AREA', 'TEMPERATURE', 'MASS FLOW RATE', 'ENERGY'")
            return f"METRIC {dimension}: {list(UnitValue.UNITS['METRIC'][dimension].keys())}\nIMPERIAL {dimension}: {list(UnitValue.UNITS['IMPERIAL'][dimension].keys())}"
        else:
            temp = ""
            for key in UnitValue.UNITS["METRIC"].keys():
                temp += f"{key}: {list(UnitValue.UNITS['METRIC'][key].keys())}\n"
            res = f"METRIC:\n{temp}IMPERIAL:\n"
            temp = ""
            for key in UnitValue.UNITS["IMPERIAL"].keys():
                temp += f"{key}: {list(UnitValue.UNITS['IMPERIAL'][key].keys())}\n"
            res += temp
            return res

    def __init__(self, system: str, dimension: str, unit: str, value: float=0) -> None:
        self.value = value
        if system.lower() == "imperial":
            self.__system = "IMPERIAL"
        elif system.lower() == "metric":
            self.__system = "METRIC"
        else:
            raise Exception(f"Unit system {system} invalid: Must be 'IMPERIAL' or 'METRIC'")
        
        if dimension not in UnitValue.UNITS[self.__system]:
            raise Exception(f"Measurement Type {dimension} invalid: Must be 'DISTANCE', 'PRESSURE', 'MASS', 'VELOCITY', 'DENSITY', 'VOLUME', 'AREA', 'TEMPERATURE', 'MASS FLOW RATE', 'ENERGY'")
        self.__dimension = dimension

        if unit not in UnitValue.UNITS[self.__system][self.__dimension]:
            raise Exception(f"Unit {unit} invalid: Unit must be {list(UnitValue.UNITS[self.__system][self.__dimension].keys())} for {self.__system} {self.__dimension}")
        self.__unit = unit

    def convert_base_metric(self):
        if self.__dimension != "TEMPERATURE":
            self.value *= UnitValue.UNITS[self.__system][self.__dimension][self.__unit] # converts back to base metric unit
            self.__system = "METRIC"
            self.__unit = list(UnitValue.UNITS[self.__system][self.__dimension].keys())[0]
        else:
            self.__temperature_handler(self.__unit, "k")
            self.__system = "METRIC"
            self.__unit = "k"

    def __convert_system(self, unit: str = "") -> None:
        self.value *= UnitValue.UNITS[self.__system][self.__dimension][self.__unit] # converts back to base metric unit
        self.__system = "IMPERIAL" if self.__system == "METRIC" else "METRIC"
        
        if unit:
            if unit in UnitValue.UNITS[self.__system][self.__dimension].keys():
                self.value /= UnitValue.UNITS[self.__system][self.__dimension][unit]
                self.__unit = unit
            else:
                sys = self.__system 
                self.__system = "IMPERIAL" if self.__system == "METRIC" else "METRIC"
                self.value /= UnitValue.UNITS[self.__system][self.__dimension][self.__unit]
                raise Exception(f"Unit {unit} invalid: Unit must be {list(UnitValue.UNITS[sys][self.__dimension].keys())} for {sys} {self.__dimension}")
        else: 
            if self.__system != "METRIC":
                self.value /= UnitValue.UNITS[self.__system][self.__dimension][list(UnitValue.UNITS[self.__system][self.__dimension].keys())[0]]
            self.__unit = list(UnitValue.UNITS[self.__system][self.__dimension].keys())[0]
        
    def __convert_unit(self, unit: str) -> None:
        if unit in UnitValue.UNITS[self.__system][self.__dimension].keys():
            self.value *= UnitValue.UNITS[self.__system][self.__dimension][self.__unit] # converts back to base metric unit
            self.value /= UnitValue.UNITS[self.__system][self.__dimension][unit] 
            self.__unit = unit
        else:
            raise Exception(f"Unit {unit} invalid: Unit must be {list(UnitValue.UNITS[self.__system][self.__dimension].keys())} for {self.__system} {self.__dimension}")

    def convert_to(self, change_system: bool, unit: str = "") -> None:
        if self.__dimension == "TEMPERATURE":
            self._convert_temp(change_system, unit)
        elif change_system is True:
            self.__convert_system(unit)
        elif unit:
            self.__convert_unit(unit)
        else:
            raise Exception("No conversion performed as change_system was false and unit was empty")

    def get_unit(self) -> str:
        return self.__unit

    def get_measurement_type(self) -> str:
        return self.__dimension

    def get_system(self) -> str:
        return self.__system

    def __repr__(self) -> str:
        return f"{self.__system} {self.__dimension}: {self.value} {self.__unit}"

    def __temperature_handler(self, old_unit: str, new_unit: str):
        if new_unit == "k":
            if old_unit == "c":
                self.value += 273.15
            elif old_unit == "f":
                self.value = (self.value - 32) * (5/9) + 273.15
        elif new_unit == "c":
            if old_unit == "k":
                self.value -= 273.15
            elif old_unit == "f":
                self.value = (self.value - 32) * (5/9)
        elif new_unit == "f":
            if old_unit == "k":
                self.value = ((self.value -273.15) / (5/9)) + 32
            elif old_unit == "c":
                self.value = (self.value / (5/9)) + 32
        
    def _convert_temp(self, change_system: bool, unit: str=""):
        if change_system:
            self.__system = "IMPERIAL" if self.__system == "METRIC" else "METRIC"
            if unit in UnitValue.UNITS[self.__system][self.__dimension].keys():
                self.__temperature_handler(self.__unit, unit)
                self.__unit = unit
            else:
                raise Exception(f"Unit {unit} invalid: Unit must be {list(UnitValue.UNITS[self.__system][self.__dimension].keys())} for {self.__system} {self.__dimension}")
        elif unit:
            if unit in UnitValue.UNITS[self.__system][self.__dimension].keys():
                self.__temperature_handler(self.__unit, unit)
                self.__unit = unit
            else:
                raise Exception(f"Unit {unit} invalid: Unit must be {list(UnitValue.UNITS[self.__system][self.__dimension].keys())} for {self.__system} {self.__dimension}")
        else:
            raise Exception("No conversion performed as change_system was false and unit was empty")


def create_dimensioned_quantity(unit: str, value: float=0) -> UnitValue:
    for system in UnitValue.UNITS.keys():
        for dimension in UnitValue.UNITS[system].keys():
            for u in UnitValue.UNITS[system][dimension].keys():
                if u == unit:
                    return UnitValue(system, dimension, u, value)
    raise Exception("Invalid unit: this unit is not currently supported by the module")
