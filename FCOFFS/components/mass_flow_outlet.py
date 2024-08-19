
from ..components.componentClass import ComponentClass
from ..pressureSystem.PressureSystem import PressureSystem
from ..fluids.Fluid import Fluid
from ..utilities.units import UnitValue

from math import pi

class MassFlowOutlet(ComponentClass):
    def __init__(self, parent_system: PressureSystem, diameter: UnitValue, fluid: str, mass_flow: UnitValue, name: str=None) -> None:
        super().__init__(parent_system, diameter, fluid,name)

        if mass_flow.get_dimension != "MASS FLOW RATE":
            raise Exception("Entered invalid pressure")
        
        mass_flow.convert_base_metric()

        self.BC_type = "MASS FLOW RATE"
        self.mdot = mass_flow
        self.p = self.parent_system.ref_p
        self.rho = Fluid.density(fluid, parent_system.ref_T, self.p)

    def initialize(self):
        self.interface_in.initialize(parent_system=self.parent_system, area=pi*self.diameter**2/4, fluid=self.fluid, p=self.p, rho=self.rho, u=self.interface_in.state.u, Override=True)

    def eval(self)->list:
        res1 = (self.mdot - self.interface_in.state.mdot) / self.interface_in.state.mdot
        return [res1]
