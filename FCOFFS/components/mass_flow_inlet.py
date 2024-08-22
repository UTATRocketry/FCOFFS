
from math import pi

from ..components.componentClass import ComponentClass
from ..pressureSystem.PressureSystem import PressureSystem
from ..fluids.Fluid import Fluid
from ..utilities.units import UnitValue
from ..state.State import *

# chnage this for later
class MassFlowInlet(ComponentClass):
    def __init__(self, parent_system: PressureSystem, diameter: UnitValue, fluid: str, mass_flow_rate: UnitValue, temperature: UnitValue, name: str=None) -> None:
        super().__init__(parent_system, diameter, fluid,name)

        if mass_flow_rate.get_dimension != "MASS FLOW RATE" or temperature.get_dimension != "TEMMPERATURE":
            raise Exception("Entered invalid mass flow rate and/or temperature")

        self.BC_type = "MASS FLOW RATE"
        self.mass_flow = mass_flow_rate.convert_base_metric()
        self.p = self.parent_system.ref_p
        self.T = temperature.convert_base_metric()
        self.rho = Fluid.density(self.fluid, self.T, self.p)
        self.u = UnitValue("METRIC", "VELOCITY", "m/s", 5)

    def initialize(self):
        self.interface_out.initialize(parent_system=self.parent_system, area=pi*self.diameter**2/4, fluid=self.fluid, rho=self.rho, u=self.u, p=self.p)

    def eval(self, new_states: tuple[State, State]|None=None)->list:
        if new_states is None:
            state_out = self.interface_out.state
        else:
            state_out = new_states[1]

        res1 = (self.mass_flow - state_out.mdot) / state_out.mdot
        res2 = (self.T - state_out.T) / state_out.T
        return [res1, res2]
