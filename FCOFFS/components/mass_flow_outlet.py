
from ..components.componentClass import ComponentClass
from ..systems.steady import SteadySolver
from ..fluids.Fluid import Fluid
from ..utilities.units import UnitValue
from ..state.State import State

from math import pi

class MassFlowOutlet(ComponentClass):
    def __init__(self, parent_system: SteadySolver, diameter: UnitValue, fluid: str, mass_flow: UnitValue, name: str="Mass Flow Outlet") -> None:
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

    def eval(self, new_states: tuple[State, State]|None=None)->list:
        if new_states is None:
            state_in = self.interface_in.state
        else:
            state_in = new_states[0]

        res1 = (self.mdot - state_in.mdot) / state_in.mdot
        return [res1]
