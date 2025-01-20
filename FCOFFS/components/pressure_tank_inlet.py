
from ..components.componentClass import ComponentClass
from ..systems.steady import SteadySolver
from ..fluids.Fluid import Fluid
from ..utilities.units import UnitValue
from ..state.State import State

from math import pi

class PressurantTank(ComponentClass):
    def __init__(self, parent_system: SteadySolver, diameter: UnitValue, fluid: str, pressure: UnitValue, temperature: UnitValue, volume: UnitValue, velocity_guess: UnitValue = UnitValue("METRIC", "VELOCITY", "m/s", 5), name: str="Pressurant Tank") -> None:
        super().__init__(parent_system, diameter, fluid,name)
        #mass is not provided as input as we will calculate it from volume temperature and temperature

        if pressure.dimension != "PRESSURE" or temperature.dimension != "TEMPERATURE" or volume.dimension != "VOLUME":
            raise Exception("Entered invalid pressure and temperature")
        
        pressure.convert_base_metric()
        temperature.convert_base_metric()
        volume.convert_base_metric()

        self.BC_type = "PRESSURE"
        self.p = pressure
        self.T = temperature
        self.volume = volume
        self.rho = Fluid.density(self.fluid, self.T, self.p)
        self.u = velocity_guess
        self.mass = self.rho*self.volume


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
    
    def transient(self, dt: float|int, _: State, state: State):
        # time march
        mdot = state.area*state.rho*state.u
        self.mass = self.mass - dt*mdot
        new_rho = self.mass/self.volume
        Cp = Fluid.Cp(self.fluid, self.T, self.p)
        Cv = Fluid.Cv(self.fluid, self.T, self.p)
        self.p = self.p*(new_rho/self.rho)**(Cp/Cv)
        self.rho = new_rho
        self.T = Fluid.temp(self.fluid, self.rho, self.p)
        


