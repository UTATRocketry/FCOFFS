
from ..components.componentClass import ComponentClass
from ..pressureSystem.PressureSystem import PressureSystem
from ..fluids.Fluid import Fluid
from ..utilities.units import UnitValue
from ..state.State import State

from math import pi

class PressureInlet(ComponentClass):
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

    
    def eval(self, new_states: tuple[State, State]|None=None)->list:
        if new_states is None:
            state_out = self.interface_out.state
        else:
            state_out = new_states[1]

        res1 = (self.p - state_out.p) / state_out.p
        res2 = (self.T - state_out.T) / state_out.T
        return [res1, res2]
