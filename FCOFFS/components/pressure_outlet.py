
from ..systems.steady import SteadySolver
from ..components.componentClass import ComponentClass
from ..fluids.Fluid import Fluid
from ..utilities.units import UnitValue
from ..state.State import State

from math import pi

class PressureOutlet(ComponentClass):
    def __init__(self, parent_system: SteadySolver, diameter: UnitValue, fluid: str, pressure: UnitValue, name: str="Pressure Outlet") -> None:
        super().__init__(parent_system, diameter, fluid,name)

        if pressure.dimension != "PRESSURE":
            raise Exception("Entered invalid pressure")
        
        pressure.convert_base_metric()

        self.BC_type = "PRESSURE"
        self.p = pressure
        self.rho = Fluid.density(fluid, parent_system.ref_T, self.p)

    def initialize(self):
        self.interface_in.initialize(parent_system=self.parent_system, area=pi*self.diameter**2/4, fluid=self.fluid, p=self.p, rho=self.rho, u=self.interface_in.state.u, Override=True)

    def eval(self, new_states: tuple[State, State]|None=None)->list:
        if new_states is None:
            state_in = self.interface_in.state
        else:
            state_in = new_states[0]

        res1 = (self.p - state_in.p) / state_in.p
        return [res1]
