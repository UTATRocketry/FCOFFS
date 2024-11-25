'''
Description
'''
import numpy as np
from numpy import sqrt, pi
from scipy.interpolate import interp1d
import warnings

from ..systems.steady import SteadySolver
from ..state.State import *
from ..components.componentClass import ComponentClass
from ..fluids.Fluid import Fluid
from ..utilities.units import *


class CriticalOrifice(ComponentClass):
    # Assumes thin plate, shard edged orrifice
    FLUID_CDS = {"N2O":1, "CO2": 1, "C2H6O": 1, "N2": 1}

    def __init__(self, parent_system: SteadySolver, diameter_in: UnitValue,  diameter_out: UnitValue, orrifice_diameter: UnitValue, fluid: str, name: str='critical_orifice', Cd: float|None = None):
        if fluid not in ['N2O','CO2', 'C2H6O', 'N2']:
            raise Exception("Fluid type not supported")
        super().__init__(parent_system, diameter_in, fluid, name)
        self.diameter_out = diameter_out.convert_base_metric()
        self.diameter_in = diameter_in.convert_base_metric()
        self.orrifice_diameter = orrifice_diameter.convert_base_metric()
        self.Beta = self.orrifice_diameter/self.diameter_in
        if Cd is None:
            self.Cd = self.FLUID_CDS[fluid]
        else:
            self.Cd = Cd
        #Note K is the velocity head loss coefficient / pressure loss coefficient
        self.K = (1-self.Beta**2)/(self.Cd**2*self.Beta**4)
        self.decoupler = True 

        vals = np.array([[0, 1], [0.5, 1], [0.6, 0.9], [0.7, 0.65], [0.8, 0.46], [0.9, 0.33], [0.95, 0.23], [0.98, 0.14], [0.99, 0.1], [1, 0], [100, 0]])
        self.interp = interp1d(vals[:, 0], vals[:, 1], 'cubic') #changed to cubic form linear maybe qudratic good to.

    def initialize(self):
            if self.parent_system.outlet_BC != 'PRESSURE':
                warnings.warn("Outlet BC not well posed. ")
            self.interface_in.initialize(parent_system=self.parent_system, area=pi*self.diameter_in**2/4, fluid=self.fluid)
            self.interface_out.initialize(parent_system=self.parent_system, area=pi*self.diameter_out**2/4, fluid=self.fluid, rho=self.interface_in.state.rho, u=self.interface_in.state.u, p=self.interface_in.state.p)
            # we will assume that component adjacent to orifice has inlet diameter matching orifice diameter (up to user variability)

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
            
        Cp_in = Fluid.Cp(self.fluid, state_in.T , state_in.p)
        Cv_in = Fluid.Cv(self.fluid, state_in.T , state_in.p) 

        gamma = Cp_in / Cv_in
        R_gas = Fluid.get_gas_constant(self.fluid)
        
        try:
            c_s = Fluid.local_speed_sound(self.fluid, state_out.T, state_out.rho)
        except Exception:
            c_s = sqrt(gamma*R_gas*state_out.T)
            
        #Mach_initial = state_in.u / c_s
        #Mach_final = state_out.u / c_s   
        #something very wrong is going on as im getting negative velocity and mdot
        
                
        #from mass continuity 
        # res1 = (state_out.mdot - state_in.rho*(pi*self.diameter_in**2/4)*state_in.u) / (0.5*(state_out.mdot + (state_in.rho*(pi*self.diameter_in**2/4)*state_in.u) ) )
        
        #from isentropic nozzle flow equations
        #res2 = ( (state_in.p/state_out.p) - (1 + ((gamma-1)/2) * (Mach_final**2 - Mach_initial**2))**(gamma/(gamma-1)) ) / ( 0.5 * ( (state_in.p/state_out.p) + (1 + ((gamma-1)/2) * (Mach_final**2 - Mach_initial**2))**(gamma/(gamma-1)) ) )
        # res2 = (state_out.p - (state_in.p - 0.5*self.K*state_in.rho*state_in.u**2)) / (0.5*(state_out.p + state_in.p - 0.5*self.K*state_in.rho*state_in.u**2))
        mdot_in = state_in.u*state_in.rho*state_in.area
        mdot_out = state_out.rho*state_out.u*state_out.area
        res1 = (mdot_out - mdot_in) / (0.5 * (mdot_in + mdot_out))
        
        A_orifice = pi * self.orrifice_diameter**2/4
        
       
        # calculate percentage of upstream pressure vs downstream pressure and 
        
        P_ratio = state_out.p/state_in.p
        NC_CF =  self.interp(P_ratio)
        
        #non_critical choked flow rate correction factor = NC_CF

        # mdot_choked = (state_in.p * A_orifice * state_in.u * (1 + ((gamma-1)/2) * (Mach_final**2-Mach_initial**2))**(-gamma/(gamma-1)))/ (R_gas*state_out.T) 
        mdot_choked = NC_CF * self.Cd * (2/(gamma+1))**((gamma+1)/2*(gamma-1)) * state_in.p * sqrt(gamma/(R_gas*state_in.T)) * A_orifice
        
        res2 = (mdot_out - mdot_choked)/(0.5*(mdot_out + mdot_choked))

        h_1 = 0.5 * state_in.u**2 + Cp_in * state_in.T + state_in.p/state_in.rho             
       
        CP_out = Fluid.Cp(self.fluid, state_out.T , state_out.p)
        h_2 = 0.5 * state_out.u**2 + CP_out * state_out.T + state_out.p / state_out.rho
       
        #res3 = (state_in.T - state_out.T) / (0.5 * (state_in.T + state_out.T) ) # should be enthalpy so fix this 

        res3 = (h_2 - h_1) / (0.5 * (h_2 + h_1) ) # conservation of enthalpy 


        #output mass flux calculations that follow from isentropic nozzle flow 
        # res3 = (state_out.mdot - state_in.p * Mach_final * pi * (self.diameter_out**2)/4 * sqrt(gamma/(state_in.T*R_gas)) * (1 + ((gamma-1)/2) * (Mach_final**2 - Mach_initial**2) )**( (gamma+1) / (2*(1-gamma)) ) ) / ( 0.5 * (state_out.mdot+state_in.p * Mach_final * pi * (self.diameter_out**2)/4 * sqrt(gamma/(state_in.T*R_gas)) * (1 + ((gamma-1)/2) * (Mach_final**2 - Mach_initial**2) )**( (gamma+1) / (2*(1-gamma)) ) ))
        # chnaged above to orrifivce diameter is this what it should be????
        # verify what the optimal two state variable are to input for CoolProps equation of state calculations-->temperature and density
        return [res1, res2, res3]

        

