'''
This module allows you to easly store numbers with units and easily convert the units and value of the numbers.
The two supported systems currently are Imperial and Metric. 
Typically used units are supported and more can be added upon request or in your instance.
'''
import warnings
import numpy as np


class _gauge_conversion():
    '''
    This class is used for specifc units which can have guage versus absolute values and facilatest the conversion of these values to absolute or back to gauge. 
    Mainly useful for pressure. Do not use outside of this file 
    '''
    def __init__(self, unit_conversion_to_SI: float|int, conv_to_absolute: float|int) -> None:
        '''
        Args:
        unit_conversion_to_SI (float|int): value to multiply the non gauge unit value by to convert it to the standard SI unit.
        conv_to_absolute (float|int): value to add to get from gauge to absolute value, note this value must be negative if you subtract to convert to absolute from gauge
        '''
        self.__to_SI = unit_conversion_to_SI
        self.__to_ABSOLUTE = conv_to_absolute
    
    def __mul__(self, m) -> int|float:
        '''
        Used in unit class to convert the unit to SI. Thus converts the guage value to absolute and then SI base unit.

        Args:
            d : the current value of the gauge unit.

        Returns:
            float|int : The base SI absolute value of the gauge value
        '''
        absolute_value = m + self.__to_ABSOLUTE
        return absolute_value * self.__to_SI
    
    __rmul__ = __mul__

    def __truediv__(self, d):
        '''
        Used in unit class to convert to the gauge unit. Thus converts the absolute base SI value to the gauge unit value.

        Args:
            d : the current value of theabsolute SI unit.

        Returns:
            float|int : The base SI absolute value of the gauge value
        '''
        new_unit_value = d / self.__to_SI
        return new_unit_value - self.__to_ABSOLUTE
    
    __rtruediv__ = __truediv__


class UnitValue: # add specific heat
    """
    Represents a value with dimension/units.

    Attributes:
        __system (str): The measurement system (e.g., METRIC, IMPERIAL).
        __dimension (str): The dimension of the unit (e.g., LENGTH, MASS).
        __unit (str): The unit of the value (e.g., m, kg).
        value (float): The numerical value.
    """ 
    UNITS = {"IMPERIAL": {
                           "DISTANCE": {"in": 0.0254, "mi": 1609.34, "yd": 0.9144, "ft": 0.3048}, 
                           "PRESSURE": {"psi": 6894.76, "psig": _gauge_conversion(6894.76, 14.696), "psf": 47.8803}, 
                           "MASS": {"lb": 0.453592, "ton": 907.1847, "slug": 14.59390, "st": 6.35029, "oz": 0.0283495}, 
                           "VELOCITY": {"ft/s": 0.3048, "mi/s": 1609.34, "mph": 0.44704, "in/s": 0.0254}, 
                           "DENSITY": {"lb/in^3": 27679.9, "lb/ft^3": 16.0185, "lb/yd^3": 0.593276},
                           "VOLUME": {"gal": 0.00378541, "yd^3": 0.764555, "ft^3": 0.0283168, "in^3": 0.0000163871}, 
                           "AREA": {"in^2": 0.00064516, "mi^2": 2590000, "yd^2": 0.836127, "ft^2": 0.092903},
                           "TEMPERATURE": {"f": None, "R":None},
                           "MASS FLOW RATE": {"lb/s": 0.453592, "ton/s": 907.1847, "st/s": 6.35029, "oz": 0.0283495, "lb/min": 0.00755987},
                           "ENERGY": {"BTU": 1055.05585, "ftlb": 1.35582, "kcal": 4184, "cal": 4.184},
                           "TIME": {"s": 1, "h": 3600, "min": 60, "ms": 0.001},
                           "MOMENTUM": {"slugft/s": 4.449670915354, "lbft/s": 0.1383}, 
                           "FREQUENCY": {"rpm": 0.016667},
                           "ACCELERATION": {"ft/s^2": 0.3048},
                           "FORCE": {"lbf": 4.44822},
                           "ENERGY PER UNIT MASS": {"ft^2/s^2": 0.09290304}, 
                           "MASS PER UNIT LENGTH": {"lb/ft": 1.48816, "oz/in": 1.11612},
                           "MASS PER AREA": {"lb/ft^2": 4.88243},
                           "VOLUMETRIC FLOW RATE": {"ft^3/s": 0.0283168, "gal/s": 0.00378541, "ft^3/min": 0.000471947},
                           "DYNAMIC VISCOCITY": {"lb/fts": 1.488163943568},
                           "KINEMATIC VISCOCITY": {"ft^2/s": 0.092903},
                           "MASS FLUX": {"lb/ft^2s": 4.88243},
                           "GAS CONSTANTS": {"BTU/lbf": 4186.8000000087}
                         }, 
             "METRIC": {
                         "DISTANCE": {"m": 1, "km": 1000, "cm": 0.01, "mm": 0.001}, 
                         "PRESSURE": {"kg/ms^2": 1, "MPa": 1000000, "atm": 101325, "bar": 100000, "kPa": 1000, "hPa": 100, "Pa": 1}, 
                         "MASS": {"kg": 1, "tonne": 1000, "g": 0.001}, 
                         "VELOCITY": {"m/s": 1, "km/s": 1000, "km/h": 0.277778, "cm/s": 0.01, "mm/s": 0.001}, 
                         "DENSITY": {"kg/m^3": 1, "t/m^3": 1000, "g/m^3": 0.001},
                         "VOLUME": {"m^3": 1, "L": 0.001, "cm^3": 0.000001, "mL": 0.000001, "mm^3": 0.000000001},
                         "AREA": {"m^2": 1, "km^2": 1000000, "cm^2": 0.0001, "mm^2": 0.000001},
                         "TEMPERATURE": {"K": None, "c": None}, 
                         "MASS FLOW RATE": {"kg/s": 1, "t/s": 1000, "kg/min": 0.0166667, "g/s": 0.001},
                         "ENERGY": {"kgm^2/s^2": 1, "MJ": 1000000, "kJ": 1000, "Nm": 1, "J": 1, "eV": 1.602177e-19},
                         "TIME": {"s": 1, "h": 3600, "min": 60, "ms": 0.001},
                         "MOMENTUM": {"kgm/s": 1, "Ns": 1}, 
                         "FREQUENCY": {"/s": 1, "Hz": 1},
                         "ACCELERATION": {"m/s^2": 1, "g": 9.80665},
                         "FORCE": {"kgm/s^2": 1, "N": 1, "gcm/s^2": 0.00001},
                         "ENERGY PER UNIT MASS": {"m^2/s^2": 1},
                         "MASS PER LENGTH": {"kg/m": 1, "kg/cm": 100, "g/cm": 0.1},
                         "MASS PER AREA": {"kg/m^2": 1, "g/cm^2": 10},
                         "VOLUMETRIC FLOW RATE": {"m^3/s": 1, "cm^3/s": 0.000001},
                         "DYNAMIC VISCOCITY": {"kg/ms": 1, "g/cms":0.1},
                         "KINEMATIC VISCOCITY": {"m^2/s": 1, "cm^2/s": 0.0001},
                         "MASS FLUX": {"kg/m^2s": 1},
                         "GAS CONSTANTS": {"m^2/s^2K": 1, "J/kgK": 1, "J/kgc": 1}
                        }
            }
    
    SPELLING_MAP = {'mtr': 'm', 'meters': 'm', 'mtr.': 'm', 'metres': 'm', 'metre': 'm', 'm ': 'm', 'meter': 'm', 'kilometer': 'km', 'kilometre': 'km', 'kilo meter': 'km', 'k meter': 'km', 'klometer': 'km', 'km ': 'km', 'kmeter': 'km', 'kmtr': 'km', 'centemeter': 'cm', 'centimetre': 'cm', 'cn': 'cm', 'c meter': 'cm', 'cm ': 'cm', 'centi meter': 'cm', 'centimeter': 'cm', 'cmeter': 'cm', 'cmtr': 'cm', 'mmeter': 'mm', 'millimeter': 'mm', 'milimeter': 'mm', 'milli meter': 'mm', 'millimetre': 'mm', 'm meter': 'mm', 'mn': 'mm', 'mmtr': 'mm', 'mm ': 'mm', 'g ': 'g', 'gramme': 'g', 'grm': 'g', 'gms': 'g', 'gram': 'g', 'gm': 'g', 'gramm': 'g', 'gram ': 'g', 'kilograms': 'kg', 'k gram': 'kg', 'kilogramme': 'kg', 'kilogram ': 'kg', 'kilogramme ': 'kg', 'kilogrammes': 'kg', 'kg ': 'kg', 'kilogram': 'kg', 'kilo gram': 'kg', 'kgrm': 'kg', 'liters': 'L', 'l': 'L', 'litres': 'L', 'ltrs': 'L', 'liter': 'L', 'litre ': 'L', 'litre': 'L', 'liters ': 'L', 'liter ': 'L', 'litter': 'L', 'ltr': 'L', 'ml': 'mL', 'milliliter': 'mL', 'mlitres': 'mL', 'millilitre': 'mL', 'milli litre': 'mL', 'mliters': 'mL', 'milli liter': 'mL', 'mltr': 'mL', 'sec': 's', 'seconds': 's', 'sedonds': 's', 'sconds': 's', 'second': 's', 'secs': 's', 'secnd': 's', 'minute': 'min', 'minuts': 'min', 'mins': 'min', 'minutes': 'min', 'min': 'min', 'minut': 'min', 'hours': 'h', 'hr': 'h', 'howr': 'h', 'houer': 'h', 'hour': 'h', 'hou': 'h', 'hrs': 'h', 'square meters': 'm^2', 'square meter': 'm^2', 'sqr meter': 'm^2', 'square metre': 'm^2', 'sq meter': 'm^2', 'sqmetre': 'm^2', 'sq metres': 'm^2', 'sqm': 'm^2', 'cube meter': 'm^3', 'cu meter': 'm^3', 'cbm': 'm^3', 'cubic meters': 'm^3', 'cubic metre': 'm^3', 'cubic meter': 'm^3', 'cu m': 'm^3', 'C': 'c','degree centigrade': 'c', 'degree celsius': 'c', 'celcius': 'c', 'deg celsius': 'c', 'celsius degree': 'c', 'celsus': 'c', 'celsius': 'c', 'deg c': 'c', 'fahrenheit degree': 'f', 'deg f': 'f', 'deg fahrenheit': 'f', 'fahrenhiet': 'f', 'degree fahrenheit': 'f', 'farhenheit': 'f', 'force': 'kgm/s^2', 'Newton': 'kgm/s^2', 'newtn': 'kgm/s^2', 'nwton': 'kgm/s^2', 'nwt': 'kgm/s^2', 'newton': 'kgm/s^2', 'joule': 'kgm^2/s^2', 'energy': 'kgm^2/s^2', 'juole': 'kgm^2/s^2', 'jl': 'kgm^2/s^2', 'joules': 'kgm^2/s^2', 'juul': 'kgm^2/s^2', 'inck': 'in', 'inche': 'in', 'inch': 'in', 'inc': 'in', 'inch ': 'in', 'inchh': 'in', 'foot': 'ft', 'foott': 'ft', 'fot': 'ft', 'foor': 'ft', 'foot ': 'ft', 'feet': 'ft', 'yardd': 'yd', 'yad': 'yd', 'yarrd': 'yd', 'yard ': 'yd', 'yard': 'yd', 'mille': 'mi', 'mile ': 'mi', 'milee': 'mi', 'mil': 'mi', 'mile': 'mi', 'pounds': 'lb', 'pounnd': 'lb', 'pound ': 'lb', 'pound': 'lb', 'lbs': 'lb', 'poundd': 'lb', 'galln': 'gal', 'gllon': 'gal', 'gallon': 'gal', 'galllon': 'gal', 'gallon ': 'gal', 'ounze': 'oz', 'ouncce': 'oz', 'ounce ': 'oz', 'ozs': 'oz', 'ounce': 'oz', 'ounc': 'oz', 'ounc ': 'oz', 'stn': 'st', 'stone ': 'st', 'sts': 'st', 'stone': 'st', 'st ': 'st', 'ft2': 'ft^2', 'square foot': 'ft^2', 'sqft': 'ft^2', 'square feet': 'ft^2', 'sq foot': 'ft^2', 'ft3': 'ft^3', 'cft': 'ft^3', 'cubic foot': 'ft^3', 'cu ft': 'ft^3', 'cubic feet': 'ft^3'}
    
    @classmethod
    def add_custom_unit(cls, system: str, dimension:str, unit:str, conversion_factor: float) -> None:
        """
        Add your own units to the package instance whihc you can then use in conversion and arithmatic. Note there is a small chance new SI/Metric units will mess with unit conversion during arithmatic. 

        Args:
            system (str): The measurement system ('IMPERIAL' or 'METRIC'). 
            dimension (str): The dimension of the unit (e.g., 'DISTANCE', 'PRESSURE', 'MASS'). 
            unit (str): The string representing the new unit e.g., 'kg'
            conversion_factor (float): The conversion factor to convert from this unit to the SI base for this units dimension. Must be > 0 or throws error.

        Raises:
            Exception: If the provided system or dimension is invalid, if the unit already exists or if the conversion factor is less than 0.
        """
        if system == "METRIC" or system == "IMPERIAL":
            if dimension not in cls.UNITS[system]:
                raise ValueError(f"Dimension {dimension} is invalid must be one of {list(cls.UNITS[system].keys())}")
            elif dimension == "TEMPERATURE":
                raise NotImplementedError("Currently their is no support for adding custom temperature units")
            elif unit in cls.UNITS[system][dimension]:
                raise ValueError(f"Unit {unit} already exists")
            elif conversion_factor <= 0:
                raise ValueError(f"Conversion Factor {conversion_factor} invalid")
            cls.UNITS[system][dimension][unit] = conversion_factor
        raise ValueError(f"System {system} is invalid must be one of ('METRIC', 'IMPERIAL')")
        
    @classmethod
    def available_units(cls, system: str="", dimension: str="") -> str:
        """
        Get available units for the specified measurement system and dimension.

        Args:
            system (str, optional): The measurement system ('IMPERIAL' or 'METRIC'). Defaults to an empty string, which returns units for all systems.
            dimension (str, optional): The dimension of the unit (e.g., 'DISTANCE', 'PRESSURE', 'MASS'). Defaults to an empty string, which returns units for all dimensions.

        Returns:
            str: A string listing available units for the specified system and dimension.

        Raises:
            Exception: If the provided system or dimension is invalid.
        """
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
    
    @classmethod
    def create_unit(cls, unit: str, value: float=0) -> 'UnitValue':
        """
        Create a UnitValue object based on the unit and value. Will also account for spelling mistakes/alternate names of units.

        Args:
            unit (str): The unit of the value.
            value (float): The numerical value.
        
        Returns:
            UnitValue: A UnitValue object with the specified unit and value.
        """
        u = cls.SPELLING_MAP.get(unit)
        if u: unit  = u
            
        for system, dimensions in cls.UNITS.items():
            for dimension, units in dimensions.items():
                if unit in units:
                    return UnitValue(system, dimension, unit, value)
        warnings.warn("Creating unit not recongized by package") 
        return UnitValue(None, None, unit, value)
    
    @classmethod
    def unit_from_string(cls, unit_str:str) -> 'UnitValue':
        """
    Create a UnitValue object from a formatted string (e.g., '10 m').
    
    Args:
        unit_str (str): The string containing the value and unit.
    
    Returns:
        UnitValue: A UnitValue object.
    
    Raises:
        ValueError: If the string is not in the correct format.
    """
        res = unit_str.split()
        if len(res) > 2:
            raise ValueError(f"String {unit_str} is not in right format 'value unit' e.g,. '10 kg")
        try:
            val = float(res[0])
            return UnitValue.create_unit(res[1], val)
        except:
            raise ValueError("First element of string could not be converted to number, ensure string of the form e.g., '10 kg'")
    
    @classmethod
    def from_dict(cls, data: dict) -> 'UnitValue':
        """
        Create a UnitValue object from a dictionary.
        
        Args:
            data (dict): A dictionary containing the system, dimension, unit, and value.
        
        Returns:
            UnitValue: A UnitValue object.
        """
        try:
            return cls(data['system'], data['dimension'], data['unit'], data['value'])
        except:
            raise ValueError(f"Dictionary {data}, doesn't contain the correct keys 'system', 'dimension',  unit, and value")
    

    def __init__(self, system: str|None, dimension: str|None, unit: str, value: float=0) -> None:
        """
        Initialize a UnitValue object.

        Args:
            system (str): The measurement system.
            dimension (str): The dimension of the unit.
            unit (str): The unit of the value.
            value (float): The numerical value.
        """
        self._conversion_cache = {}
        self.value = value
        if system is None:
            self.__system = None
            self.__dimension = None
            self.__unit = unit
            return
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

    def __call__(self) -> int|float:
        """
        Get the value of the unit.

        Returns:
            int|float: The magnitude of the dimensioned quatity
        """
        return self.value
    
    @staticmethod
    def __process_unit(unit_str: str, units: str, opp: int) -> None:
        """
        Processes a unit string and updates the units dictionary with the appropriate values.

        Args:
            unit_str (str): The unit string to be processed.
            units (dict): A dictionary to store the processed units and their values.
            opp (int): An integer used to determine the operation (1 for multiplication, -1 for division).

        Returns:
            None: This function updates the units dictionary in place.
        """ 
        i = 0
        while i < len(unit_str):
            if unit_str[i] == "/":
                opp *= -1
                i += 1
                continue
            elif unit_str[i] == "k":
                key = unit_str[i:i+2]
                i += 1      
            else:
                key = unit_str[i]

            if key not in units:
                units[key] = 0 

            if i + 1 < len(unit_str) and unit_str[i+1] == "^":
                index = 2
                is_float = False
                for j in range(i+2, len(unit_str)):
                    if unit_str[j] == ".":
                        is_float = True
                        index += 1
                    else:
                        try:
                            int(unit_str[j])
                            index += 1
                        except:
                            break
                if is_float:
                    units[key] += opp * float(unit_str[i+2:i+index])
                else:
                    units[key] += opp * int(unit_str[i+2:i+index])
                i += index
            else:
                units[key] += opp
                i += 1

    def __mul__(self, m) -> 'UnitValue':
        """
        Multiplies UnitValue object by another Unitvlue or dimensionless value.
        """
        if isinstance(m, UnitValue):
            self.convert_base_metric()
            m.convert_base_metric()
            units = {}
            self.__process_unit(self.__unit, units, 1)
            self.__process_unit(m.__unit, units, 1)
            
            for dimension, units_dict in UnitValue.UNITS["METRIC"].items():
                    temp = {}
                    self.__process_unit(list(units_dict)[0], temp, 1)
                    if temp == units:
                        return UnitValue("METRIC", dimension, list(units_dict)[0], self.value * m.value)

            numer = ""
            denom = "/"
            for key in units.keys():
                if units[key] > 1:
                    numer += f"{key}^{units[key]}" if units[key] % 1 != 0 else f"{key}^{int(units[key])}"
                elif units[key] == 1:
                    numer += key
                elif units[key] == -1:
                    denom += key
                elif units[key] < -1:
                    denom += f"{key}^{-1*units[key]}" if units[key] % 1 != 0 else f"{key}^{-1*int(units[key])}"

            new_unit = numer + denom if denom != "/" else numer
            if new_unit == "":
                return self.value * m.value
                    
            return UnitValue(None, None, new_unit, self.value * m.value)
        elif isinstance(m, (int, float)):
            return UnitValue(self.__system, self.__dimension, self.__unit, self.value * m)
        else:
            try: 
                return self * float(m) # checking if whatever the type is if it can be converted to float and then used 
            except:
                return NotImplemented
            
    def __rmul__(self, m) -> 'UnitValue':
        return self.__mul__(m)

    def __truediv__(self, d) -> 'UnitValue':
        """
        Divides UnitValue object by another Unitvlue or dimensionless value.
        """
        if isinstance(d, UnitValue):
            self.convert_base_metric()
            d.convert_base_metric()
            units = {}
            self.__process_unit(self.__unit, units, 1)
            self.__process_unit(d.__unit, units, -1)

            for dimension, units_dict in UnitValue.UNITS["METRIC"].items():
                    temp = {}
                    self.__process_unit(list(units_dict)[0], temp, 1)
                    if temp == units:
                        return UnitValue("METRIC", dimension, list(units_dict)[0], self.value / d.value)

            numer = ""
            denom = "/"
            for key in units.keys():
                if units[key] > 1:
                    numer += f"{key}^{units[key]}" if units[key] % 1 != 0 else f"{key}^{int(units[key])}"
                elif units[key] == 1:
                    numer += key
                elif units[key] == -1:
                    denom += key
                elif units[key] < -1:
                    denom += f"{key}^{-1*units[key]}" if units[key] % 1 != 0 else f"{key}^{-1*int(units[key])}"

            new_unit = numer + denom if denom != "/" else numer
            if new_unit == "": 
                return self.value / d.value
                    
            return UnitValue(None, None, new_unit, self.value / d.value)
        elif isinstance(d, (int, float)):
            return UnitValue(self.__system, self.__dimension, self.__unit, self.value / d)
        else:
            try: 
                return self / float(d) 
            except:
                return NotImplemented
        
    def __rtruediv__(self, d) -> 'UnitValue':
        """
        Divides another Unitvlue or dimensionless value by UnitValue object.
        """
        if isinstance(d, UnitValue):
            self.convert_base_metric()
            d.convert_base_metric()
            units = {}
            self.__process_unit(self.__unit, units, -1)
            self.__process_unit(d.__unit, units, 1)

            for dimension, units_dict in UnitValue.UNITS["METRIC"].items():
                    temp = {}
                    self.__process_unit(list(units_dict)[0], temp, 1)
                    if temp == units:
                        return UnitValue("METRIC", dimension, list(units_dict)[0], d.value / self.value)

            numer = ""
            denom = "/"
            for key in units.keys():
                if units[key] > 1:
                    numer += f"{key}^{units[key]}" if units[key] % 1 != 0 else f"{key}^{int(units[key])}"
                elif units[key] == 1:
                    numer += key
                elif units[key] == -1:
                    denom += key
                elif units[key] < -1:
                    denom += f"{key}^{-1*units[key]}" if units[key] % 1 != 0 else f"{key}^{int(units[key])}"

            new_unit = numer + denom if denom != "/" else numer
            if new_unit == "": 
                return d.value / self.value
                    
            return UnitValue(None, None, new_unit, d.value / self.value)
        elif isinstance(d, (int, float)):
            
            units = {}
            self.__process_unit(self.__unit, units, -1)
            for dimension, units_dict in UnitValue.UNITS["METRIC"].items():
                    temp = {}
                    self.__process_unit(list(units_dict)[0], temp, 1)
                    if temp == units:
                        return UnitValue("METRIC", dimension, list(units_dict)[0], d / self.value)

            temp = self.__unit.split("/")
            b = True
            denom = "/"
            numer = ""
            for units in temp:
                if b:
                    denom += units
                    b = False
                else:
                    numer += units
                    b = True

            new_unit = numer + denom
            return UnitValue(None, None, new_unit, d / self.value)
        else:
            try: 
                return  float(d) / self
            except:
                return NotImplemented

    def __pow__(self, p)  -> 'UnitValue':
        """
        Raises UnitValue object to the power of a float or interger.
        """
        if isinstance(p, (int, float)):
            if p == 1:
                return self
            
            self.convert_base_metric()
            units = {}
            self.__process_unit(self.__unit, units, 1)
            for unit in units.keys():
                units[unit] *= p
            for dimension, units_dict in UnitValue.UNITS["METRIC"].items():
                    temp = {}
                    self.__process_unit(list(units_dict)[0], temp, 1)
                    if temp == units:
                        return UnitValue("METRIC", dimension, list(units_dict)[0], self.value ** p)

            numer = ""
            denom = "/"
            for key in units.keys():
                if units[key] == 1:
                    numer += key 
                elif units[key] == -1:
                    denom += key
                elif units[key] > 0:
                    numer += f"{key}^{units[key]}" if units[key] % 1 != 0 else f"{key}^{int(units[key])}"
                elif units[key] < 0:
                    denom += f"{key}^{-1*units[key]}" if units[key] % 1 != 0 else f"{key}^{-1*int(units[key])}"

            new_unit = numer + denom if denom != "/" else numer       
            return UnitValue(None, None, new_unit, self.value ** p)

        else:
            try: 
                return self ** float(p) 
            except:
                return NotImplemented

    def __add__(self, a)  -> 'UnitValue':
        """
        Adds UnitValue object by another Unitvlue or dimensionless value.
        """
        if isinstance(a, UnitValue):
            if self.__dimension != a.__dimension:
                if self.__unit != a.__unit:
                    raise TypeError(f"Cannot add unit {self.__unit} and unit {a.__unit}")
                return UnitValue(self.__system, self.__dimension, self.__unit, self.value + a.value)
            self.convert_base_metric()
            a.convert_base_metric()
            return UnitValue(self.__system, self.__dimension, self.__unit, self.value + a.value)
        elif isinstance(a, (int, float)):
            warnings.warn("Adding unitless value to quantity with units")
            return UnitValue(self.__system, self.__dimension, self.__unit, self.value + a)
        else:
            try: 
                return self + float(a) 
            except:
                return NotImplemented
        
    def __radd__(self, a)  -> 'UnitValue':
        return self.__add__(a)

    def __sub__(self, s)  -> 'UnitValue':
        """
        Subtracts UnitValue object by another Unitvlue or dimensionless value.
        """
        if isinstance(s, UnitValue):
            if self.__dimension != s.__dimension:
                if self.__unit != s.__unit:
                    raise TypeError(f"Cannot subtract unit {self.__unit} and unit {s.__unit}")
                return UnitValue(self.__system, self.__dimension, self.__unit, self.value - s.value)
            self.convert_base_metric()
            s.convert_base_metric()
            return UnitValue(self.__system, self.__dimension, self.__unit, self.value - s.value)
        elif isinstance(s, (int, float)):
            warnings.warn("Subtracting unitless value to quantity with units")
            return UnitValue(self.__system, self.__dimension, self.__unit, self.value - s) 
        else:
            try: 
                return self - float(s) 
            except:
                return NotImplemented
        
    def __rsub__(self, s)  -> 'UnitValue':
        return -self.__sub__(s)

    def __neg__(self):
        return UnitValue(self.__system, self.__dimension, self.__unit, -self.value)
    
    def __mod__(self, other) -> int:
        if isinstance(other, UnitValue):
            return self.value % other.value
        elif isinstance(other, (int, float)):
            return self.value % other
        else:
            return NotImplemented
        
    def __rmod__(self, other) -> int:
        if isinstance(other, UnitValue):
            return  other.value % self.value
        elif isinstance(other, (int, float)):
            return other % self.value
        else:
            return NotImplemented

    def __abs__(self):
        """
        Returns a Unitvalue object with the absolute value of the original UnitValue value.
        """
        return UnitValue(self.__system, self.__dimension, self.__unit, abs(self.value))         

    def __eq__(self, other) -> bool:
        """
        Checks if UnitValue object is equal to other.
        """
        if isinstance(other, UnitValue):
            a = self.copy().convert_base_metric()
            b = other.copy().convert_base_metric()
            return a.value == b.value and a.__unit == b.__unit
        elif isinstance(other, (int, float)):
            return self.value == other
        return False

    def __ne__(self, other) -> bool:
        if isinstance(other, UnitValue):
            a = self.copy().convert_base_metric()
            b = other.copy().convert_base_metric()
            return a.value != b.value and a.__unit != b.__unit
        elif isinstance(other, (int, float)):
            return self.value != other
        return True
    
    def __lt__(self, other) -> bool:
        if isinstance(other, UnitValue):
            a = self.copy().convert_base_metric()
            b = other.copy().convert_base_metric()
            return a.value < b.value
        elif isinstance(other, (int, float)):
            return self.value < other
        raise TypeError(f"Cannot compare type UnitValue and type {type(other)}")
    
    def __le__(self, other) -> bool:
        if isinstance(other, UnitValue):
            a = self.copy().convert_base_metric()
            b = other.copy().convert_base_metric()
            return a.value <= b.value
        elif isinstance(other, (int, float)):
            return self.value <= other
        raise TypeError(f"Cannot compare type UnitValue and type {type(other)}")
    
    def __gt__(self, other) -> bool:
        if isinstance(other, UnitValue):
            a = self.copy().convert_base_metric()
            b = other.copy().convert_base_metric()
            return a.value > b.value
        elif isinstance(other, (int, float)):
            return self.value > other
        raise TypeError(f"Cannot compare type UnitValue and type {type(other)}")
    
    def __ge__(self, other) -> bool:
        if isinstance(other, UnitValue):
            a = self.copy().convert_base_metric()
            b = other.copy().convert_base_metric()
            return a.value >= b.value
        elif isinstance(other, (int, float)):
            return self.value >= other
        raise TypeError(f"Cannot compare type UnitValue and type {type(other)}")
    
    def __float__(self) -> float:
        return float(self.value)
    
    def __int__(self) -> int:
        return int(self.value)
    
    def __round__(self, ndigits: int=0)  -> 'UnitValue':
        """
        Rounds UnitValue to ndigts returns rounded Unitvale
        """
        self.value = round(self.value, ndigits)
        return self
    
    def __repr__(self) -> str:
        return f"{self.value} {self.__unit}"
    
    def __str__(self) -> str:
        return f"{self.value} {self.__unit}"
    
    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        """
        Handle NumPy ufunc (universal function) operations for UnitValue objects.
        """
        out = kwargs.get('out', ())
        
        if method == "__call__":
            if isinstance(inputs[0], np.ndarray):
                inputs = [inputs[0], inputs[1]]
                for ind, element in enumerate(inputs[0]):
                    inputs[0][ind] = ufunc(element, inputs[1], **kwargs)
                return inputs[0]
            elif len(inputs) > 1 and isinstance(inputs[1], np.ndarray):
                inputs = [inputs[0], inputs[1]]
                for ind, element in enumerate(inputs[1]):
                    inputs[1][ind] = ufunc(inputs[0], element, **kwargs)
                return inputs[1]
            else:
                if isinstance(inputs[0], (np.float64, np.int64)):
                    inputs = [float(inputs[0]), inputs[1]]
                if ufunc == np.add:
                    return inputs[0] + inputs[1]
                elif ufunc == np.subtract:
                    return inputs[0] - inputs[1]
                elif ufunc == np.multiply:
                    return inputs[0] * inputs[1]
                elif ufunc == np.divide:
                    return inputs[0] / inputs[1]
                elif ufunc == np.sqrt:
                    return inputs[0] ** 0.5
                elif ufunc == np.power:
                    return inputs[0] ** inputs[1]
                elif ufunc == np.mod:
                    return inputs[0] % inputs[1]
                elif ufunc == np.log10:
                    return np.log10(inputs[0].value)
                else:
                    return NotImplemented
    
    def __array_function__(self, func, types, *args, **kwargs):
        if func is np.concatenate:
            unit_cache = []
            for arr in args[0]:
                unit_cache += [item.get_unit if isinstance(item, UnitValue) else None for item in arr]
                for i in range(len(arr)):
                    arr[i] = arr[i].value if isinstance(arr[i], UnitValue) else arr[i]
            new_array = np.concatenate(args[0], **kwargs)
            for ind, unit in enumerate(unit_cache):
                if unit is not None:
                    new_array[ind] = self.create_unit(unit, new_array[ind])
            return new_array
        else:
            return NotImplemented

    def __convert_system(self, unit: str = "") -> None:
        self.value *= UnitValue.UNITS[self.__system][self.__dimension][self.__unit] 
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
            self.value *= UnitValue.UNITS[self.__system][self.__dimension][self.__unit]
            self.value /= UnitValue.UNITS[self.__system][self.__dimension][unit] 
            self.__unit = unit
        else:
            raise Exception(f"Unit {unit} invalid: Unit must be {list(UnitValue.UNITS[self.__system][self.__dimension].keys())} for {self.__system} {self.__dimension}")

    def copy(self)  -> 'UnitValue':
        return UnitValue(self.__system, self.__dimension, self.__unit, self.value)
    
    def __temperature_handler(self, old_unit: str, new_unit: str): # add Rankine
        if new_unit == "K":
            if old_unit == "c":
                self.value += 273.15
            elif old_unit == "f":
                self.value = (self.value - 32) * (5/9) + 273.15
            elif old_unit == "R":
                self.value *= 5/9
        elif new_unit == "c":
            if old_unit == "K":
                self.value -= 273.15
            elif old_unit == "f":
                self.value = (self.value - 32) * (5/9)
            elif old_unit == "R":
                self.value = (self.value - 491.67) * (5/9)
        elif new_unit == "f":
            if old_unit == "K":
                self.value = ((self.value -273.15) / (5/9)) + 32
            elif old_unit == "c":
                self.value = (self.value / (5/9)) + 32 
            elif old_unit == "R":
                self.value -= 459.67
        elif new_unit == "R":
            if old_unit == "c":
                self.value = self.value * (9/5) + 491.67
            elif old_unit == "f":
                self.value += 459.67
            elif old_unit == "K":
                self.value *= 1.8
        
    def __convert_temp(self, change_system: bool, unit: str=""):
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

    def convert_base_metric(self) -> 'UnitValue':
        """
        Convert the current value to it's base SI/Metric unit.
        
        Returns:
            UnitValue: The UnitValue object with the converted units.
        """
        if self.__system is None:
            return
        elif self.__dimension != "TEMPERATURE":
            self.value *= UnitValue.UNITS[self.__system][self.__dimension][self.__unit] 
            self.__system = "METRIC"
            self.__unit = list(UnitValue.UNITS[self.__system][self.__dimension].keys())[0]
        else:
            self.__temperature_handler(self.__unit, "K")
            self.__system = "METRIC"
            self.__unit = "K"
        return self
    
    def to(self, unit:str) -> 'UnitValue':
        """
        Convert the current value to a new unit.

        Args:
            unit (str): The unit to convert to.
        
        Returns:
            UnitValue: The UnitValue object with the converted value.
        
        Raises:
            Exception: If the unit is not recognized or conversion is not possible.
        """
        u = UnitValue.SPELLING_MAP.get(unit)
        if u: unit  = u

        cache_key = (self.__system, self.__dimension, self.__unit, unit)
        if cache_key in self._conversion_cache:
            cached_value = self._conversion_cache[cache_key]
            return UnitValue(self.__system, self.__dimension, unit, cached_value)

        other_system = "IMPERIAL" if self.__system == "METRIC" else "METRIC"
        if self.__system is None:
            raise Exception(f"Invalid unit {self.__unit}: this unit is not currently supported by the module")
        elif self.__dimension == "TEMPERATURE":
            if unit in UnitValue.UNITS[self.__system][self.__dimension]:
                self.__convert_temp(False, unit)
            elif unit in UnitValue.UNITS[other_system][self.__dimension]:
                self.__convert_temp(True, unit) 
            else:
                raise TypeError(f"Cannot convert unit of dimension {self.__dimension} to {unit}")
        else:
            if unit in UnitValue.UNITS[self.__system][self.__dimension]:
                self.__convert_unit(unit)
            elif unit in UnitValue.UNITS[other_system][self.__dimension]:
                self.__convert_system(unit)
            else:
                raise TypeError(f"Cannot convert unit of dimension {self.__dimension} to {unit}")
        
        self._conversion_cache[cache_key] = self.value
        return self

    def to_dict(self) -> dict:
        """
        Convert the UnitValue object to a dictionary.
        
        Returns:
            dict: A dictionary representation of the UnitValue object.
        """
        return {
            'system': self.__system,
            'dimension': self.__dimension,
            'unit': self.__unit,
            'value': self.value
        }

    @property
    def get_unit(self) -> str:
        return self.__unit

    @property
    def get_dimension(self) -> str:
        return self.__dimension

    @property
    def get_system(self) -> str:
        return self.__system

