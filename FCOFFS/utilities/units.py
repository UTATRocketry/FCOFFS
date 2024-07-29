'''
This module allows you to easly store numbers with units and easily convert the units and value of the numbers.
The two supported systems currently are Imperial and Metric. 
It currently suports numbers of the unit type 'DISTANCE', 'PRESSURE', 'MASS', 'VELOCITY', 'DENSITY', 'VOLUME'.
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

class UnitValue: # add mass flow rate, q?
    UNITS = {"IMPERIAL": {
                           "DISTANCE": {"in": 0.0254, "mi": 1609.34, "yd": 0.9144, "ft": 0.3048}, 
                           "PRESSURE": {"psi": 6894.76, "psf": 47.8803}, 
                           "MASS": {"lb": 0.453592, "ton": 907.1847,"st": 6.35029, "oz": 0.0283495}, 
                           "VELOCITY": {"ft/s": 0.3048, "mi/s": 1609.34, "mph": 0.44704, "in/s": 0.0254}, 
                           "DENSITY": {"lb/in^3": 27679.9, "lb/ft^3": 16.0185, "lb/yd^3": 0.593276},
                           "VOLUME": {"gal": 0.00378541, "yd^3": 0.764555, "ft^3": 0.0283168, "in^3": 0.0000163871}, 
                           "AREA": {"in^2": 0.00064516, "mi^2": 2590000, "yd^2": 0.836127, "ft^2": 0.092903},
                           "TEMPERATURE": {"f": None}
                         }, 
             "METRIC": {
                         "DISTANCE": {"m": 1, "km": 1000, "cm": 0.01, "mm": 0.001}, 
                         "PRESSURE": {"Pa": 1, "MPa": 1000000, "bar": 100000, "kPa": 1000, "hPa": 100}, 
                         "MASS": {"kg": 1, "tonne": 1000, "g": 0.001}, 
                         "VELOCITY": {"m/s": 1, "km/s": 1000, "km/h": 0.277778, "cm/s": 0.01, "mm/s": 0.001}, 
                         "DENSITY": {"kg/m^3": 1, "t/m^3": 1000, "g/m^3": 0.001},
                         "VOLUME": {"m^3": 1, "L": 0.001, "cm^3": 0.000001, "mm^3": 0.000000001},
                         "AREA": {"m^2": 1, "km^2": 1000000, "cm^2": 0.0001, "mm^2": 0.000001},
                         "TEMPERATURE": {"k": None, "c": None}
                        }
            }

    def __init__(self, system: str, measurement_type: str, unit: str, value: float=0) -> None:
        self.value = value
        if system.lower() == "imperial":
            self.__system = "IMPERIAL"
        elif system.lower() == "metric":
            self.__system = "METRIC"
        else:
            raise Exception(f"Unit system {system} invalid: Must be 'IMPERIAL' or 'METRIC'")
        
        if measurement_type not in UnitValue.UNITS[self.__system]:
            raise Exception(f"Measurement Type {measurement_type} invalid: Must be 'DISTANCE', 'PRESSURE', 'MASS', 'VELOCITY', 'DENSITY', 'VOLUME'")
        self.__type = measurement_type

        if unit not in UnitValue.UNITS[self.__system][self.__type]:
            raise Exception(f"Unit {unit} invalid: Unit must be {list(UnitValue.UNITS[self.__system][self.__type].keys())} for {self.__system} {self.__type}")
        self.__unit = unit

    def convert_base_metric(self):
        if self.__type != "TEMPERATURE":
            self.value *= UnitValue.UNITS[self.__system][self.__type][self.__unit] # convert back to base metric unit
            self.__system = "METRIC"
            self.__unit = list(UnitValue.UNITS[self.__system][self.__type].keys())[0]
        else:
            self.temperature_handler(self.__unit, "k")
            self.__system = "METRIC"
            self.__unit = "k"

    def convert_system(self, unit: str = "") -> None:
        if self.__type != "TEMPERATURE":
            self.value *= UnitValue.UNITS[self.__system][self.__type][self.__unit] # convert back to base metric unit
            self.__system = "IMPERIAL" if self.__system == "METRIC" else "METRIC"
            
            if unit:
                if unit in UnitValue.UNITS[self.__system][self.__type].keys():
                    self.value /= UnitValue.UNITS[self.__system][self.__type][unit]
                    self.__unit = unit
                else:
                    sys = self.__system 
                    self.__system = "IMPERIAL" if self.__system == "METRIC" else "METRIC"
                    self.value /= UnitValue.UNITS[self.__system][self.__type][self.__unit] # convert back to base metric unit
                    raise Exception(f"Unit {unit} invalid: Unit must be {list(UnitValue.UNITS[sys][self.__type].keys())} for {sys} {self.__type}")
            else: # need to convert to other system and then change unit
                if self.__system != "METRIC":
                    self.value /= UnitValue.UNITS[self.__system][self.__type][list(UnitValue.UNITS[self.__system][self.__type].keys())[0]]
                self.__unit = list(UnitValue.UNITS[self.__system][self.__type].keys())[0]
        else:
            self.change_temp(True, unit)
        
    def convert_unit(self, unit: str) -> None:
        if self.__type != "TEMPERATURE":
            if unit in UnitValue.UNITS[self.__system][self.__type].keys():
                self.value *= UnitValue.UNITS[self.__system][self.__type][self.__unit] # convert back to base metric unit
                self.value /= UnitValue.UNITS[self.__system][self.__type][unit] 
                self.__unit = unit
            else:
                raise Exception(f"Unit {unit} invalid: Unit must be {list(UnitValue.UNITS[self.__system][self.__type].keys())} for {self.__system} {self.__type}")
        else:
            self.change_temp(False, unit)

    def convert_to(self, change_system: bool, unit: str = "") -> None:
        if change_system is True:
            self.convert_system(unit)
        elif unit:
            self.convert_unit(unit)
        else:
            raise Exception("No conversion performed as change_system was false and unit was empty")

    def get_unit(self) -> str:
        return self.__unit

    def get_measurement_type(self) -> str:
        return self.__type

    def get_system(self) -> str:
        return self.__system

    def __repr__(self) -> str:
        return f"{self.__system} {self.__type}: {self.value} {self.__unit}"

    def temperature_handler(self, old_unit: str, new_unit: str):
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
        
    
    def change_temp(self, change_system: bool, unit: str=""):
        if change_system:
            self.__system = "IMPERIAL" if self.__system == "METRIC" else "METRIC"
            if unit in UnitValue.UNITS[self.__system][self.__type].keys():
                self.temperature_handler(self.__unit, unit)
                self.__unit = unit
            else:
                raise Exception(f"Unit {unit} invalid: Unit must be {list(UnitValue.UNITS[self.__system][self.__type].keys())} for {self.__system} {self.__type}")
        elif unit:
            if unit in UnitValue.UNITS[self.__system][self.__type].keys():
                self.temperature_handler(self.__unit, unit)
                self.__unit = unit
            else:
                raise Exception(f"Unit {unit} invalid: Unit must be {list(UnitValue.UNITS[self.__system][self.__type].keys())} for {self.__system} {self.__type}")
        else:
            raise Exception("No conversion performed as change_system was false and unit was empty")
