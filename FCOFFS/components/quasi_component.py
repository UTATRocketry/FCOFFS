
from ..components.componentClass import ComponentClass
from ..pressureSystem.PressureSystem import PressureSystem
from ..fluids.Fluid import Fluid
from ..utilities.units import UnitValue

from math import pi

class InletOutlet(ComponentClass):
    def __init__(self, parent_system: PressureSystem, diameter: UnitValue, fluid: str, input_quantities: tuple[UnitValue, UnitValue]=(), output_quantities: tuple[UnitValue]=(), name: str=None) -> None:
        super().__init__(parent_system, diameter, fluid,name)
        
        func_dict = {"PRESSURE": self.__pressure_residual, "MASS": self.__density_residual, "VELOCITY": self.__velocity_residual, "TEMPERATURE": self.__temperature_residual}

        if len(input_quantities) != 2 or len(output_quantities) != 1:
            raise Exception("Over/Under Constrained Problem, Provide only three intialization quantities")

        self.quantities = list(input_quantities) + list(output_quantities)
        try:
            self.res_funcs = [func_dict[self.quantities[0].get_dimension], func_dict[self.quantities[1].get_dimension], func_dict[self.quantities[2].get_dimension]]
        except Exception as e:
            raise Exception("Program is cureently not configured to handle that dimension for inlet and outlet")
        
        if self.quantities[0].get_dimension == self.quantities[2].get_dimension:
            self.BC_type = self.quantities[0].get_dimension
        elif self.quantities[1].get_dimension == self.quantities[2].get_dimension:
            self.BC_type = self.quantities[1].get_dimension
        else:
            raise Exception("Inlet and Outlet must share a set quantity dimension")

        self.set_constant_constituents()


    def __pressure_residual(self, quantity: UnitValue, type: str["Inlet", "Outlet"]) -> float:
        val = self.interface_out.state.p if type == "Inlet" else self.interface_in.state.p
        return (quantity - val)/val
    
    def __density_residual(self, quantity: UnitValue, type: str["Inlet", "Outlet"]) -> float:
        val = self.interface_out.state.rho if type == "Inlet" else self.interface_in.state.rho
        return (quantity - val)/val

    def __velocity_residual(self, quantity: UnitValue, type: str["Inlet", "Outlet"]) -> float: # this may be redundant and not needed
        val = self.interface_out.state.u if type == "Inlet" else self.interface_in.state.u
        return (quantity - val)/val

    def __temperature_residual(self, quantity: UnitValue, type: str["Inlet", "Outlet"]) -> float: 
        val = self.interface_out.state.T if type == "Inlet" else self.interface_in.state.T
        return (quantity - val)/val

    def set_constant_constituents(self):
        self.p = None
        self.T = None
        self.rho = None
        self.u = UnitValue("METRIC", "VELOCITY", "m/s", 5)
        for unit in self.quantities[:2]:
            if unit.get_dimension == "PRESSURE":
                self.p = unit
            elif unit.get_dimension == "DENSITY":
                self.rho = unit
            elif unit.get_dimension == "TEMPERATURE":
                self.T = unit
            else:
                raise Exception("Must provide two paramaters of either Pressure, density or temperature")

        if self.p is None:
            self.p = Fluid.pressure(self.fluid, self.rho.value, self.T.value)
        elif self.rho is None:
            self.rho = Fluid.density(self.fluid, self.T.value, self.p.value)

        self.u_out = UnitValue("METRIC", "VELOCITY", "m/s", 5)
        if self.BC_type == "PRESSURE":
            self.p_out = self.quantities[2]
            self.rho_out = Fluid.density(self.fluid, self.parent_system.ref_T.value, self.p_out.value)
        elif unit.get_dimension == "DENSITY":
            self.rho_out = self.quantities[2]
            self.p_out = Fluid.pressure(self.fluid, self.rho_out.value, self.parent_system.ref_T.value)
        

    def initialize(self):
        self.interface_in.initialize(parent_system=self.parent_system, area=pi*self.diameter**2/4, fluid=self.fluid, rho=self.rho_out, u=self.u_out, p=self.p_out)
        self.interface_out.initialize(parent_system=self.parent_system, area=pi*self.diameter**2/4, fluid=self.fluid, rho=self.rho, u=self.u, p=self.p)    

    def eval(self):
        return [self.res_funcs[0](self.quantities[0], "Inlet"), self.res_funcs[1](self.quantities[1], "Inlet"), self.res_funcs[2](self.quantities[2], "Outlet")]



        


class QuasiComponent(ComponentClass): # this class is to broad and allows the user to input to much varinace for how the system needs to be implemented
    # why do we guess 5 meters a second as initial velocity
    # needs to set intialize state for first interface and state of last interface

    def __init__(self, parent_system: PressureSystem, diameter: UnitValue, fluid: str, input_quantities: tuple[UnitValue]=(), output_quantities: tuple[UnitValue]=(), name: str=None) -> None:
        super().__init__(parent_system, diameter, fluid,name)
        
        func_dict = {"PRESSURE": self.__pressure_residual, "DENSITY": self.__density_residual, "VELOCITY": self.__velocity_residual, "TEMPERATURE": self.__temperature_residual}

        if len(input_quantities) + len(output_quantities) != 3:
            raise Exception("Over/Under Constrained Problem, Provide only three intialization quantities")

        self.quantities = list(input_quantities) + list(output_quantities)
        self.QuasiComponentType = [] 
        self.res_funcs = []
        try:
            for unit in input_quantities:
                self.res_funcs.append(func_dict[unit.get_dimension])
                self.QuasiComponentType.append("Inlet")
            for unit in output_quantities:
                self.res_funcs.append(func_dict[unit.get_dimension])
                self.QuasiComponentType.append("Outlet")
        except Exception as e:
            raise Exception("Program is cureently not configured to handle that dimension for inlet and outlet")

    # enquire into what quantities might be given for inlet/outlet initialization, each quantitiy will have its own private residual function
        # E.G. pressure, mass, ...etc   
        
    def __pressure_residual(self, quantity, QuasiComponentType) -> float:
        val = self.interface_out.state.p if QuasiComponentType == "Inlet" else self.interface_in.state.p
        return (quantity - val)/val
    
    def __density_residual(self, quantity, QuasiComponentType) -> float:
        val = self.interface_out.state.rho if QuasiComponentType == "Inlet" else self.interface_in.state.rho
        return (quantity - val)/val

    def __velocity_residual(self, quantity, QuasiComponentType) -> float: # this may be redundant and not needed
        val = self.interface_out.state.u if QuasiComponentType == "Inlet" else self.interface_in.state.u
        return (quantity - val)/val

    def __temperature_residual(self, quantity, QuasiComponentType) -> float: 
        val = self.interface_out.state.T if QuasiComponentType == "Inlet" else self.interface_in.state.T
        return (quantity - val)/val

    def initialize(self):
        self.interface_in.initialize(parent_system=self.parent_system, area=pi*self.diameter**2/4, fluid=self.fluid)
        self.interface_out.initialize(parent_system=self.parent_system, area=pi*self.diameter**2/4, fluid=self.fluid, rho=self.interface_in.state.rho, u=self.interface_in.state.u, p=self.interface_in.state.p)    

    def eval(self):
        return [self.res_funcs[0](self.quantities[0], self.QuasiComponentType[0]), self.res_funcs[1](self.quantities[1], self.QuasiComponentType[1]), self.res_funcs[2](self.quantities[2], self.QuasiComponentType[2])]





        




    