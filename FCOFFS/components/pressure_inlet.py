
from ..components.componentClass import ComponentClass
from ..systems.steady import SteadySolver
from ..fluids.Fluid import Fluid
from ..utilities.units import UnitValue
from ..state.State import State

from math import pi

class PressureInlet(ComponentClass):
    def __init__(self, parent_system: SteadySolver, diameter: UnitValue, fluid: str, pressure: UnitValue, temperature: UnitValue, velocity_guess:UnitValue = UnitValue("METRIC", "VELOCITY", "m/s", 5), name: str="Pressure Inlet") -> None:
        super().__init__(parent_system, diameter, fluid,name)

        if pressure.get_dimension != "PRESSURE" or temperature.get_dimension != "TEMPERATURE":
            raise Exception("Entered invalid pressure and temperature")
        
        pressure.convert_base_metric()
        temperature.convert_base_metric()

        self.BC_type = "PRESSURE"
        self.p = pressure
        self.T = temperature
        self.rho = Fluid.density(self.fluid, self.T, self.p)
        self.u = velocity_guess

    def initialize(self):
        self.interface_out.initialize(parent_system=self.parent_system, area=pi*self.diameter**2/4, fluid=self.fluid, rho=self.rho, u=self.u, p=self.p)

    
    def eval(self, new_states: tuple[State, State]|None=None)->list:
        if new_states is None:
            state_out = self.interface_out.state
        else:
            state_out = new_states[1]

        res1 = (self.p - state_out.p) / self.p
        res2 = (self.T - state_out.T) / self.T
        return [res1, res2]
