
from ..components.componentClass import ComponentClass
from ..pressureSystem.PressureSystem import PressureSystem
from ..fluids.Fluid import Fluid
from ..utilities.units import UnitValue

from math import pi

# chnage this for later
class MassFlowInlet(ComponentClass):
    def __init__(self, parent_system: PressureSystem, diameter: UnitValue, fluid: str, pressure: UnitValue, temperature: UnitValue, name: str=None) -> None:
        super().__init__(parent_system, diameter, fluid,name)

        if pressure.get_dimension != "PRESSURE" or temperature.get_dimension != "TEMPERATURE":
            raise Exception("Entered invalid pressure and temperature")
        
        pressure.convert_base_metric()
        temperature.convert_base_metric()

        self.BC_type = "PRESSURE"
        self.p = pressure
        self.T = temperature
        self.rho = Fluid.density(self.fluid, self.T, self.p)
        self.u = UnitValue("METRIC", "VELOCITY", "m/s", 5)

    def initialize(self):
        self.interface_out.initialize(parent_system=self.parent_system, area=pi*self.diameter**2/4, fluid=self.fluid, rho=self.rho, u=self.u, p=self.p)

    def eval(self)->list:
        res1 = (self.p - self.interface_out.state.p) / self.interface_out.state.p
        res2 = (self.T - self.interface_out.state.T) / self.interface_out.state.T
        return [res1, res2]
