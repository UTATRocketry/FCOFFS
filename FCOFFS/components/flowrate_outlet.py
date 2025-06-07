
from .componentClass import ComponentClass
from ..systems.steady import SteadySolver
from ..fluids.Fluid import Fluid
from ..utilities.units import UnitValue
from ..state.State import State

from math import pi

class FlowRateOutlet(ComponentClass):
    def __init__(self, parent_system: SteadySolver, diameter: UnitValue, fluid: str, flow_rate: UnitValue, name: str="Flow Rate Outlet") -> None:
        super().__init__(parent_system, diameter, fluid,name)

        if flow_rate.dimension != "VOLUMETRIC FLOW RATE":
            raise Exception("Entered invalid pressure")
        if flow_rate.unit == "SLPM" or flow_rate.unit == "SCFM":
            self.STD = True
        else:
            self.STD = False

        if self.STD is False:
            flow_rate.convert_base_metric()
        self.flowrate = flow_rate.copy()
        
        self.BC_type = "MASS FLOW RATE"
        self.p = self.parent_system.ref_p
        self.rho = Fluid.density(fluid, parent_system.ref_T, self.p)
        self.mdot = flow_rate.convert_base_metric(temperature=parent_system.ref_T, pressure=self.p) * self.rho 

    def initialize(self):
        self.interface_in.initialize(parent_system=self.parent_system, area=pi*self.diameter**2/4, fluid=self.fluid, p=self.p, rho=self.rho, u=self.interface_in.state.u, Override=True)
        self.interface_in.state.mdot = self.mdot

    def eval(self, new_states: tuple[State, State]|None=None)->list:
        if new_states is None:
            state_in = self.interface_in.state
        else:
            state_in = new_states[0]

        if self.STD is False:
            res1 = (self.flowrate - state_in.mdot/state_in.rho) / (0.5*(state_in.mdot/state_in.rho + self.flowrate))
        else:
            flowrate = state_in.mdot/state_in.rho
            flowrate.to(self.flowrate.unit, temperature=state_in.T, pressure=state_in.p)
            res1 = (self.flowrate.value - flowrate.value) / (0.5*(flowrate.value + self.flowrate.value))

        return [res1]
