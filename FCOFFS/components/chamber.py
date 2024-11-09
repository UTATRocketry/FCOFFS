
from ..components.componentClass import ComponentClass
from ..systems.steady import SteadySolver
from ..fluids.Fluid import Fluid
from ..utilities.units import UnitValue
from ..state.State import State

from math import pi
from scipy.constants import R

class Chamber(ComponentClass): # eventually have N inlets
    def __init__(self, parent_system: SteadySolver, outlet_diameter: UnitValue, fluid: str, pressure: UnitValue, temperature: UnitValue, volume: UnitValue, name: str="Chamber") -> None:
        super().__init__(parent_system, outlet_diameter, fluid, name)
        self.p = pressure.convert_base_metric()
        self.T = temperature.convert_base_metric()
        self.volume = volume.convert_base_metric()

        self.rho = Fluid.density(self.fluid, self.T, self.p)
        self.mass = self.rho*self.volume
        # self.M_r = Fluid.get_molecular_mass(self.fluid)
        # U_R = UnitValue.create_unit("kgm^2/s^2MolK", R)
        # self.mass = (self.p*self.volume*self.M_r)/(U_R*self.T)

    def eval(self, new_states: tuple[State, State]|None=None) -> list:
        if new_states is None:
            state_in = self.interface_in.state
            state_out = self.interface_out.state
        else:
            state_in = new_states[0]
            state_out = new_states[1]

        res1 = (self.p - state_in.p)/state_in.p
        res2 = (self.T - state_out.T)/state_out.T
        res3 = (self.p - state_out.p)/state_out.p
        return [res1, res2, res3]
    
    def transient(self, dt:float, state_in: State, state_out: State):
        # time march
        mdot_in = state_in.area*state_in.rho*state_in.u
        mdot_out = state_out.area*state_out.rho*state_out.u
        self.mass = self.mass - dt*mdot_out + dt*mdot_in
        new_rho = self.mass/self.volume
        # add iterative computation of cp, cv
        Cp = Fluid.Cp(self.fluid, self.T, self.p)
        Cv = Fluid.Cv(self.fluid, self.T, self.p)
        self.p = self.p*(new_rho/self.rho)**(Cp/Cv)
        self.rho = new_rho
        self.T = Fluid.temp(self.fluid, self.rho, self.p)
    
