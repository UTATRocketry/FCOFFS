'''
Description
'''

from numpy import sqrt, pi
import warnings

from ..systems.steady import SteadySolver
from ..state.State import *
from ..components.componentClass import ComponentClass
from ..fluids.Fluid import Fluid
from ..utilities.units import *

class CavitatingVenturi(ComponentClass):

    FLUID_CDS = {"N2O": 0.95, "CO2": 0.95, "C2H6O": 0.95}

    def __init__(self, parent_system: SteadySolver, diameter_in: UnitValue, diameter_out: UnitValue, throat_diameter: UnitValue, fluid: str, Cd: float|None = None, name: str='cavitating_venturi'):
        if fluid not in ['N2O','CO2', "C2H6O"]:
            raise Exception("Fluid type not supported")
        super().__init__(parent_system, diameter_in, fluid, name)
        self.diameter_in = diameter_in.convert_base_metric()
        self.diameter_out = diameter_out.convert_base_metric()
        self.throat_diameter = throat_diameter.convert_base_metric()
        if Cd is None:
            self.Cd = self.FLUID_CDS[fluid]
        else:
            self.Cd = Cd
        self.decoupler = True

    def initialize(self):
        if self.parent_system.outlet_BC != 'PRESSURE':
            warnings.warn("Outlet BC not well posed. ")
        self.interface_in.initialize(parent_system=self.parent_system, area=pi*self.diameter_in**2/4, fluid=self.fluid)
        self.interface_out.initialize(parent_system=self.parent_system, area=pi*self.diameter_out**2/4, fluid=self.fluid, rho=self.interface_in.state.rho, u=self.interface_in.state.u, p=self.interface_in.state.p*0.79)

    def update(self):
        self.interface_in.update()
        self.interface_out.update()

    def eval(self, new_states: tuple[State, State]|None=None) -> list:
        if new_states is None:
            state_in = self.interface_in.state
            state_out = self.interface_out.state
        else:
            state_in = new_states[0]
            state_out = new_states[1]


        if state_in.p * 0.8 < state_out.p:
            warnings.warn("Venrturri is likely not cavitating, do not trust flow rate") 
            # add linear coefficient to decrease the flow rate 5
            #k_eff = 
            #self.mdot = state_out.area*((2*state_in.rho*(state_in.p - state_out.p))/(1+K_eff))**0.5
            betta = self.throat_diameter/self.diameter_in
            self.mdot = state_in.rho * ((pi * self.throat_diameter**2)/4) * ((2*(state_in.p - state_out.p))/state_in.rho)**0.5 * self.Cd * (1/(1-betta**4)**0.5)
        else:
            self.mdot = self.Cd * (pi * self.throat_diameter**2)/4 * sqrt(2 * state_in.rho * state_in.p)
        
        res1 = (state_in.rho - state_out.rho)/state_out.rho
        res2 = ((pi * self.diameter_in**2)/4 * state_in.u - (pi * self.diameter_out**2)/4 * state_out.u) / ( (pi * self.diameter_in**2)/4 * state_in.u)
        res3 = (self.interface_out.state.mdot - self.mdot)/self.mdot
        return [res1, res2, res3]
