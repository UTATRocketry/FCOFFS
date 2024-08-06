'''
This module allows you to easly store numbers with units and easily convert the units and value of the numbers.
The two supported systems currently are Imperial and Metric. 
It currently suports numbers of the unit type 'DISTANCE', 'PRESSURE', 'MASS', 'VELOCITY', 'DENSITY', 'VOLUME', "AREA", "TEMPERATURE", "MASS FLOW RATE", "ENERGY".
Typically used units are supported and more can be added upon request.
'''

class UnitValue: 
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
                           "PRESSURE": {"psi": 6894.76, "psf": 47.8803}, 
                           "MASS": {"lb": 0.453592, "ton": 907.1847, "slug": 14.59390, "st": 6.35029, "oz": 0.0283495}, 
                           "VELOCITY": {"ft/s": 0.3048, "mi/s": 1609.34, "mph": 0.44704, "in/s": 0.0254}, 
                           "DENSITY": {"lb/in^3": 27679.9, "lb/ft^3": 16.0185, "lb/yd^3": 0.593276},
                           "VOLUME": {"gal": 0.00378541, "yd^3": 0.764555, "ft^3": 0.0283168, "in^3": 0.0000163871}, 
                           "AREA": {"in^2": 0.00064516, "mi^2": 2590000, "yd^2": 0.836127, "ft^2": 0.092903},
                           "TEMPERATURE": {"f": None, "R":None},
                           "MASS FLOW RATE": {"lb/s": 0.453592, "ton/s": 907.1847, "st/s": 6.35029, "oz": 0.0283495, "lb/min": 0.00755987},
                           "ENERGY": {"ftlb": 1.35582, "kcal": 4184, "cal": 4.184},
                           "TIME": {"s": 1, "h": 3600, "min": 60, "ms": 0.001},
                           "MOMENTUM": {"slugft/s": 4.449670915354, "lbft/s": 0.1383}, 
                           "FREQUENCY": {"rpm": 0.016667},
                           "ACCELERATION": {"ft/s^2": 0.3048},
                           "FORCE": {"lbf": 4.44822},
                           "ENERGY PER UNIT MASS": {"ft^2/s^2": 0.09290304}, 
                           "MASS PER UNIT LENGTH": {"lb/ft": 1.48816, "oz/in": 1.11612},
                           "MASS PER AREA": {"lb/ft^2": 4.88243},
                           "VOLUMETRIC FLOW RATE": {"ft^3/s": 0.0283168, "gal/s": 0.00378541},
                           "DYNAMIC VISCOCITY": {"lb/fts": 1.488163943568},
                           "KINEMATIC VISCOCITY": {"ft^2/s": 0.092903},
                           "MASS FLUX": {"lb/ft^2s": 4.88243} 
                         }, 
             "METRIC": {
                         "DISTANCE": {"m": 1, "km": 1000, "cm": 0.01, "mm": 0.001}, 
                         "PRESSURE": {"kg/ms^2": 1, "MPa": 1000000, "bar": 100000, "kPa": 1000, "hPa": 100, "Pa": 1}, 
                         "MASS": {"kg": 1, "tonne": 1000, "g": 0.001}, 
                         "VELOCITY": {"m/s": 1, "km/s": 1000, "km/h": 0.277778, "cm/s": 0.01, "mm/s": 0.001}, 
                         "DENSITY": {"kg/m^3": 1, "t/m^3": 1000, "g/m^3": 0.001},
                         "VOLUME": {"m^3": 1, "L": 0.001, "cm^3": 0.000001, "mL": 0.000001, "mm^3": 0.000000001},
                         "AREA": {"m^2": 1, "km^2": 1000000, "cm^2": 0.0001, "mm^2": 0.000001},
                         "TEMPERATURE": {"k": None, "c": None},
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
                         "MASS FLUX": {"kg/m^2s": 1}
                        }
            }
    
    SPELLING = {"m": {"meter": None, "metre": None, "mtr": None, "mtr.": None, "m ": None},
                "km": {"kilometer": None, "kilometre": None, "kmeter": None, "klometer": None, "kilo meter": None, "k meter": None, "kmtr": None, "km ": None},
                "cm": {"centimeter": None, "centimetre": None, "cmeter": None, "centemeter": None, "centi meter": None, "c meter": None, "cmtr": None, "cn": None, "cm ": None},
                "mm": {"millimeter": None, "millimetre": None, "mmeter": None, "milimeter": None, "milli meter": None, "m meter": None, "mmtr": None, "mn": None, "mm ": None},
                "g": {"gram": None, "gramme": None, "gm": None, "gms": None, "grm": None, "gramm": None, "g ": None, "gram ": None},
                "kg": {"kilogram": None, "kilogramme": None, "kgrm": None, "kilo gram": None, "k gram": None, "kilograms": None, "kilogrammes": None, "kilogramme ": None, "kg ": None, "kilogram ": None},
                "L": {"liter": None, "litre": None, "ltr": None, "liters": None, "litres": None, "ltrs": None, "litter": None, "l": None, "litre ": None, "liters ": None, "liter ": None},
                "mL": {"milliliter": None, "millilitre": None, "mltr": None, "milli liter": None, "milli litre": None, "mliters": None, "mlitres": None, "ml": None},
                "s": {"second": None, "sec": None, "secs": None, "sconds": None, "sedonds": None, "secnd": None, "seconds": None},
                "m": {"minute": None, "min": None, "mins": None, "minut": None, "minuts": None, "minutes": None},
                "h": {"hour": None, "hr": None, "hrs": None, "houer": None, "howr": None, "hou": None, "hours": None},
                "m^2": {"square meter": None, "sq meter": None, "sqm": None, "sqr meter": None, "square metre": None, "sqmetre": None, "sq metres": None, "square meters": None},
                "m^3": {"cubic meter": None, "cbm": None, "cu meter": None, "cubic metre": None, "cube meter": None, "cu m": None, "cubic meters": None},
                "c": {"degree celsius": None, "degree centigrade": None, "deg c": None, "celsius degree": None, "deg celsius": None, "celsus": None, "celcius": None, "celsius": None},
                "f": {"degree fahrenheit": None, "deg f": None, "fahrenheit degree": None, "deg fahrenheit": None, "farhenheit": None, "fahrenhiet": None},
                "kgm/s^2": {"Newton": None, "newton": None, "nwt": None, "newtn": None, "nwton": None, "force": None},
                "kgm^2/s^2": {"joule": None, "joules": None, "jl": None, "juole": None, "juul": None, "energy": None},
                "in": {"inch": None, "inc": None, "inck": None, "inche": None, "inchh": None, "inch ": None},
                "ft": {"foot": None, "fot": None, "foor": None, "foot ": None, "foott": None},
                "yd": {"yard": None, "yardd": None, "yarrd": None, "yad": None, "yard ": None, "yarrd": None},
                "mi": {"mile": None, "milee": None, "mile ": None, "mil": None, "mille": None},
                "lb": {"pound": None, "poundd": None, "pound ": None, "pounnd": None},
                "gal": {"gallon": None, "galln": None, "gallon ": None, "gllon": None, "galllon": None},
                "oz": {"ounce": None, "ounze": None, "ounce ": None, "ounc": None, "ouncce": None, "ounc ": None},
                "st": {"stone": None, "stn": None, "st ": None, "stone ": None},
                "ft^2": {"square foot": None, "sq foot": None, "sqft": None, "square feet": None, "ft2": None},
                "ft^3": {"cubic foot": None, "cu ft": None, "cubic feet": None, "ft3": None, "cft": None}
                }

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

    def __init__(self, system: str|None, dimension: str|None, unit: str, value: float=0) -> None:
        """
        Initialize a UnitValue object.

        Args:
            system (str): The measurement system.
            dimension (str): The dimension of the unit.
            unit (str): The unit of the value.
            value (float): The numerical value.
        """
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
        """ # check for dot
        i = 0
        while i < len(unit_str):
            if unit_str[i] == "/":
                opp *= -1
                i += 1
                continue
            if unit_str[i] == "k":
                if len(unit_str) > 1:
                    key = unit_str[i:i+2]
                    if key not in units:
                        units[key] = 0
                    units[key] += opp
                    i += 1
            elif unit_str[i] == "^":
                if i > 1 and unit_str[i-2] == "k":
                    if i + 2 < len(unit_str) and unit_str[i+2] == ".":
                        key = unit_str[i-1]
                        if key not in units: units[key] = 0
                        units[key] += opp * float(unit_str[i+1:i+4]) - opp 
                        i += 4
                        continue
                    key = unit_str[i-2:i]
                    if key not in units:
                        units[key] = 0
                    units[key] += opp * int(unit_str[i+1]) - opp
                    i += 2
                    continue
                elif i + 2 < len(unit_str) and unit_str[i+2] == ".":
                    key = unit_str[i-1]
                    if key not in units: units[key] = 0
                    units[key] += opp * float(unit_str[i+1:i+4]) - opp 
                    i += 4
                    continue
                key = unit_str[i-1]
                if key not in units:
                    units[key] = 0
                units[key] += opp * int(unit_str[i+1]) - opp
                i += 1
            else:
                key = unit_str[i]
                if key not in units:
                    units[key] = 0
                units[key] += opp
            i += 1
    
    def __mul__(self, m):
        """
        Multiplies UnitValue object by another Unitvlue or dimensionless value.
        """
        if isinstance(m, UnitValue):
            self.convert_base_metric()
            m.convert_base_metric()
            units = {}
            self.__process_unit(self.__unit, units, 1)
            self.__process_unit(m.__unit, units, 1)

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
            
            for dimension, units_dict in UnitValue.UNITS["METRIC"].items():
                for unit in units_dict:
                    if unit == new_unit:
                        return UnitValue("METRIC", dimension, unit, self.value * m.value)
            for dimension, units_dict in UnitValue.UNITS["METRIC"].items():
                for unit in units_dict:
                    if len(unit) == len(new_unit) and sorted(unit) == sorted(new_unit):
                        return UnitValue("METRIC", dimension, unit, self.value * m.value)
                    
            return UnitValue(None, None, new_unit, self.value * m.value)
        else:
            if not isinstance(m, (int, float)):
                raise TypeError(f"Invalid operation * between types: UnitValue and {type(m)}")
            return UnitValue(self.__system, self.__dimension, self.__unit, self.value * m)
            
    __rmul__ = __mul__

    def __truediv__(self, d):
        """
        Divides UnitValue object by another Unitvlue or dimensionless value.
        """
        if isinstance(d, UnitValue):
            self.convert_base_metric()
            d.convert_base_metric()
            units = {}
            self.__process_unit(self.__unit, units, 1)
            self.__process_unit(d.__unit, units, -1)

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
            
            for dimension, units_dict in UnitValue.UNITS["METRIC"].items():
                for unit in units_dict:
                    if unit == new_unit:
                        return UnitValue("METRIC", dimension, unit, self.value / d.value)
            for dimension, units_dict in UnitValue.UNITS["METRIC"].items():
                for unit in units_dict:
                    if len(unit) == len(new_unit) and sorted(unit) == sorted(new_unit):
                        return UnitValue("METRIC", dimension, unit, self.value / d.value)
                    
            return UnitValue(None, None, new_unit, self.value / d.value)
        else:
            if not isinstance(d, (int, float)):
                raise TypeError(f"Invalid operation * between types: UnitValue and {type(d)}")
            return UnitValue(self.__system, self.__dimension, self.__unit, self.value / d)
        
    def __rtruediv__(self, d):
        """
        Divides another Unitvlue or dimensionless value by UnitValue object.
        """
        if isinstance(d, UnitValue):
            self.convert_base_metric()
            d.convert_base_metric()
            units = {}
            self.__process_unit(self.__unit, units, -1)
            self.__process_unit(d.__unit, units, 1)

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
            
            for dimension, units_dict in UnitValue.UNITS["METRIC"].items():
                for unit in units_dict:
                    if unit == new_unit:
                        return UnitValue("METRIC", dimension, unit, d.value / self.value)
            for dimension, units_dict in UnitValue.UNITS["METRIC"].items():
                for unit in units_dict:
                    if len(unit) == len(new_unit) and sorted(unit) == sorted(new_unit):
                        return UnitValue("METRIC", dimension, unit, d.value / self.value)
                    
            return UnitValue(None, None, new_unit, d.value / self.value)
        else:
            if not isinstance(d, (int, float)):
                raise TypeError(f"Invalid operation * between types: UnitValue and {type(d)}")
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
            for dimension, units_dict in UnitValue.UNITS["METRIC"].items():
                for unit in units_dict:
                    if unit == new_unit:
                        return UnitValue("METRIC", dimension, unit, d / self.value)
            for dimension, units_dict in UnitValue.UNITS["METRIC"].items():
                for unit in units_dict:
                    if len(unit) == len(new_unit) and sorted(unit) == sorted(new_unit):
                        return UnitValue("METRIC", dimension, unit, d / self.value)
            return UnitValue(None, None, new_unit, d / self.value)

    def __pow__(self, p):
        """
        Raises UnitValue object to the power of a float or interger.
        """
        if isinstance(p, int) or p % 0.5 == 0:
            if p == 1:
                return self
            
            self.convert_base_metric()
            units = {}
            self.__process_unit(self.__unit, units, 1)

            numer = ""
            denom = "/"
            if p > 0:
                for key in units.keys():
                    if abs(units[key]*p) == 1:
                        numer += key 
                    elif abs(units[key]*p) < 1:
                        numer += f"{key}^{units[key]*p}"
                    elif units[key] > 0:
                        numer += f"{key}^{units[key]*p}" if units[key] % 1 != 0 or units[key]*p % 1 != 0 else f"{key}^{int(units[key]*p)}"
                    elif units[key] < 0:
                        denom += f"{key}^{-1*units[key]*p}" if units[key] % 1 != 0 or units[key]*p % 1 != 0 else f"{key}^{-1*int(units[key]*p)}"
            else:
                for key in units.keys():
                    if abs(units[key]*p) == 1:
                        denom += key
                    elif abs(units[key]*p) < 1:
                        denom += f"{key}^{units[key]*p}"
                    elif units[key] == 1:
                        denom += key if p == -1 else f"{key}^{-1*units[key]*p}"
                    elif units[key] > 1:
                        denom += f"{key}^{-1*units[key]*p}" if units[key] % 1 != 0 or units[key]*p % 1 != 0 else f"{key}^{-1*int(units[key]*p)}"
                    elif units[key] == -1:
                        numer += key if p == -1 else f"{key}^{units[key]*p}"
                    elif units[key] < -1:
                        numer += f"{key}^{units[key]*p}" if units[key] % 1 != 0 or units[key]*p % 1 != 0 else f"{key}^{int(units[key]*p)}"

            new_unit = numer + denom if denom != "/" else numer
            for dimension, units_dict in UnitValue.UNITS["METRIC"].items():
                for unit in units_dict:
                    if unit == new_unit:
                        return UnitValue("METRIC", dimension, unit, self.value**p)
            for dimension, units_dict in UnitValue.UNITS["METRIC"].items():
                for unit in units_dict:
                    if len(unit) == len(new_unit) and sorted(unit) == sorted(new_unit):
                        return UnitValue("METRIC", dimension, unit, self.value**p)
                    
            return UnitValue(None, None, new_unit, self.value**p)
        elif isinstance(p, float):
            Warning("Performing non dimensional power on UnitValue, ignoring dimension change")
            return UnitValue(self.__system, self.__dimension, self.__unit, self.value ** p)
        else:
            raise TypeError(f"Cannot raise UnitValue to the power of type: {type(p)}")

    def __add__(self, a):
        """
        Adds UnitValue object by another Unitvlue or dimensionless value.
        """
        if isinstance(a, UnitValue):
            if self.__dimension != a.__dimension:
                raise TypeError(f"Cannot add type: UnitValue and type: {type(a)}")
            self.convert_base_metric()
            a.convert_base_metric()
            return UnitValue(self.__system, self.__dimension, self.__unit, self.value + a.value)
        
        if isinstance(a, (int, float)):
            Warning("Adding dimensionless value to value with dimensions thus assumed same dimension")
            return UnitValue(self.__system, self.__dimension, self.__unit, self.value + a)
        
    __radd__ = __add__

    def __sub__(self, s):
        """
        Subtracts UnitValue object by another Unitvlue or dimensionless value.
        """
        if isinstance(s, UnitValue):
            if self.__dimension != s.__dimension:
                raise TypeError(f"Cannot subtract type: UnitValue and type: {type(s)}")
            self.convert_base_metric()
            s.convert_base_metric()
            return UnitValue(self.__system, self.__dimension, self.__unit, self.value - s.value)
        if isinstance(s, (int, float)):
            Warning("Subtracting value with dimensions by dimensionless value, thus assumed same dimension")
            return UnitValue(self.__system, self.__dimension, self.__unit, self.value - s)   
        
    def __rsub__(self, s):
        """
        Subtracts another Unitvlue or dimensionless value by UnitValue object.
        """
        if isinstance(s, UnitValue):
            if self.__dimension != s.__dimension:
                raise TypeError(f"Cannot subtract type: UnitValue and type: {type(s)}")
            self.convert_base_metric()
            s.convert_base_metric()
            return UnitValue(self.__system, self.__dimension, self.__unit, s.value - self.value)
        if isinstance(s, (int, float)):
            Warning("Subtracting dimensionless value by value with dimensions, thus assumed same dimension")
            return UnitValue(self.__system, self.__dimension, self.__unit, s - self.value) 

    def __abs__(self):
        return UnitValue(self.__system, self.__dimension, self.__unit, abs(self.value))         

    def __eq__(self, other) -> bool:
        """
        Checks if UnitValue object is equal to other.
        """
        if isinstance(other, UnitValue):
            a = self.__cpy().convert_base_metric()
            b = other.__cpy().convert_base_metric()
            return a.value == b.value and a.__unit == b.__unit
        elif isinstance(other, (int, float)):
            return self.value == other
        return False

    def __ne__(self, other) -> bool:
        if isinstance(other, UnitValue):
            a = self.__cpy().convert_base_metric()
            b = other.__cpy().convert_base_metric()
            return a.value != b.value and a.__unit != b.__unit
        elif isinstance(other, (int, float)):
            return self.value != other
        return True
    
    def __lt__(self, other) -> bool:
        if isinstance(other, UnitValue):
            a = self.__cpy().convert_base_metric()
            b = other.__cpy().convert_base_metric()
            return a.value < b.value
        elif isinstance(other, (int, float)):
            return self.value < other
        raise TypeError(f"Cannot compare type UnitValue and type {type(other)}")
    
    def __le__(self, other) -> bool:
        if isinstance(other, UnitValue):
            a = self.__cpy().convert_base_metric()
            b = other.__cpy().convert_base_metric()
            return a.value <= b.value
        elif isinstance(other, (int, float)):
            return self.value <= other
        raise TypeError(f"Cannot compare type UnitValue and type {type(other)}")
    
    def __gt__(self, other) -> bool:
        if isinstance(other, UnitValue):
            a = self.__cpy().convert_base_metric()
            b = other.__cpy().convert_base_metric()
            return a.value > b.value
        elif isinstance(other, (int, float)):
            return self.value > other
        raise TypeError(f"Cannot compare type UnitValue and type {type(other)}")
    
    def __ge__(self, other) -> bool:
        if isinstance(other, UnitValue):
            a = self.__cpy().convert_base_metric()
            b = other.__cpy().convert_base_metric()
            return a.value >= b.value
        elif isinstance(other, (int, float)):
            return self.value >= other
        raise TypeError(f"Cannot compare type UnitValue and type {type(other)}")
    
    def __float__(self) -> float:
        return float(self.value)
    
    def __int__(self) -> int:
        return int(self.value)
    
    def __round__(self, ndigits: int=0):
        self.value = round(self.value, ndigits)
        return self
    
    def __repr__(self) -> str:
        return f"{self.value} {self.__unit}"
    
    def __str__(self) -> str:
        return f"{self.value} {self.__unit}"
    
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

    def __cpy(self):
        return UnitValue(self.__system, self.__dimension, self.__unit, self.value)
    
    def __temperature_handler(self, old_unit: str, new_unit: str): # add Rankine
        if new_unit == "k":
            if old_unit == "c":
                self.value += 273.15
            elif old_unit == "f":
                self.value = (self.value - 32) * (5/9) + 273.15
            elif old_unit == "R":
                self.value *= 5/9
        elif new_unit == "c":
            if old_unit == "k":
                self.value -= 273.15
            elif old_unit == "f":
                self.value = (self.value - 32) * (5/9)
            elif old_unit == "R":
                self.value = (self.value - 491.67) * (5/9)
        elif new_unit == "f":
            if old_unit == "k":
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
            elif old_unit == "k":
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

    def convert_base_metric(self):
        """
        Convert the current value to it's base SI/Metric unit.
        
        Returns:
            UnitValue: The UnitValue object with the converted units.
        """
        if self.__system is None:
            return
        elif self.__dimension != "TEMPERATURE":
            self.value *= UnitValue.UNITS[self.__system][self.__dimension][self.__unit] # converts back to base metric unit
            self.__system = "METRIC"
            self.__unit = list(UnitValue.UNITS[self.__system][self.__dimension].keys())[0]
        else:
            self.__temperature_handler(self.__unit, "k")
            self.__system = "METRIC"
            self.__unit = "k"
        return self
    
    def to(self, unit:str):
        """
        Convert the current value to a new unit.

        Args:
            unit (str): The unit to convert to.
        
        Returns:
            UnitValue: The UnitValue object with the converted value.
        
        Raises:
            Exception: If the unit is not recognized or conversion is not possible.
        """
        if self.__system is None:
            raise Exception(f"Invalid unit {self.__unit}: this unit is not currently supported by the module")
        elif self.__dimension == "TEMPERATURE":
            if unit in UnitValue.UNITS[self.__system][self.__dimension]:
                self.__convert_temp(False, unit)
            else:
                self.__convert_temp(True, unit) 
        else:
            if unit in UnitValue.UNITS[self.__system][self.__dimension]:
                self.__convert_unit(unit)
            else:
                self.__convert_system(unit)
        return self

    @property
    def get_unit(self) -> str:
        return self.__unit

    @property
    def get_dimension(self) -> str:
        return self.__dimension

    @property
    def get_system(self) -> str:
        return self.__system


def create_dimensioned_quantity(unit: str, value: float=0) -> UnitValue:
    """
    Create a UnitValue object based on the unit and value. Will also account for speeling mistakes/alternate names of units.

    Args:
        unit (str): The unit of the value.
        value (float): The numerical value.
    
    Returns:
        UnitValue: A UnitValue object with the specified unit and value.
    """
    for u, spelings in UnitValue.SPELLING.items():
        if unit in spelings:
            unit = u
            break

    for system, dimensions in UnitValue.UNITS.items():
        for dimension, units in dimensions.items():
            if unit in units:
                return UnitValue(system, dimension, unit, value)
    Warning("Creating unit not recongized by module")
    return UnitValue(None, None, unit, value)
