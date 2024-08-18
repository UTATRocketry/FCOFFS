
from ..pressureSystem.PressureSystem import PressureSystem
from ..components.componentClass import ComponentClass
from ..fluids.Fluid import Fluid
from ..utilities.units import UnitValue

from math import pi

class PressureOutlet(ComponentClass):
    def __init__(self, parent_system: PressureSystem, diameter: UnitValue, fluid: str, pressure: UnitValue, name: str=None) -> None:
        super().__init__(parent_system, diameter, fluid,name)

        if pressure.get_dimension != "PRESSURE":
            raise Exception("Entered invalid pressure")
        
        pressure.convert_base_metric()

        self.BC_type = "PRESSURE"
        self.p = pressure
        self.rho = Fluid.density(fluid, parent_system.ref_T, self.p)

    def initialize(self):
        self.interface_in.initialize(parent_system=self.parent_system, area=pi*self.diameter**2/4, fluid=self.fluid, p=self.p, rho=self.rho, u=self.interface_in.state.u)

    def eval(self)->list:
        res1 = (self.p - self.interface_in.state.p) / self.interface_in.state.p
        return [res1]
