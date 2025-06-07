from numpy import log10, sqrt, log, pi
from scipy.optimize import brentq

from ..systems.steady import SteadySolver
from ..state.State import *
from .componentClass import ComponentClass
from FCOFFS.utilities.component_curve import ComponentCurve
from ..fluids.Fluid import Fluid
from FCOFFS.utilities.units import *

import warnings


class SmoothBend(ComponentClass):
    '''Ninety Degeree Smooth Bend'''
    def __init__(self, parent_system: SteadySolver, diameter: UnitValue, radius_of_curvature: UnitValue, fluid: str, name: str="SmoothBend"):
        super().__init__(parent_system, diameter, fluid, name)
        
        self.radius_of_curvature = radius_of_curvature.convert_base_metric() # note measured from centerline of the pipe
        self.diameter = diameter.convert_base_metric() 
        self.curvature_ratio = 0.5*self.diameter/self.radius_of_curvature # 2 * radius of curvature = D (diameter of curavture)

    def initialize(self):
        self.interface_in.initialize(parent_system=self.parent_system, area=pi*self.diameter**2/4, fluid=self.fluid)
        self.interface_out.initialize(parent_system=self.parent_system, area=pi*self.diameter**2/4, fluid=self.fluid, rho=self.interface_in.state.rho, u=self.interface_in.state.u, p=self.interface_in.state.p)


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
        # find upstream condition
        mdot = state_in.mdot
        rho_in = state_in.rho
        u_in = state_in.u
        p_in = state_in.p
        q_in = state_in.q
        T_in = state_in.T
        g = UnitValue("METRIC", "ACCELERATION", "m/s^2", 9.81)

        c_s = Fluid.local_speed_sound(self.fluid, T = state_in.T, rho=state_in.rho)
        # print(state_in.u)
        Mach_in = state_in.u / c_s

        state = Fluid.phase(self.fluid, state_in.T, state_in.p) 
        if Mach_in < 0.1 or state == "liquid" or state == "supercritical liquid":
            compressible = False
        else:
            compressible = True

        # compute Reynolds Number
        kinematic_viscosity = Fluid.kinematic_viscosity(self.fluid, rho_in)
        Re = u_in * self.diameter / kinematic_viscosity
        
        # Dean number characterizes how much secondary or turbulent effects dominate the flow at a given Reynolds number and curvature of pipe
        def compute_De(Re, curavture_ratio):
            return Re * curavture_ratio**0.5

        De = compute_De(Re, self.curvature_ratio)
        
        if De < 10 or De > 100:
            # bounds that define curvature of pipe, residuals only apply to Dean numbers outside this range
            warnings.warn(f"De number {De} is out of normal range of operation. Results may be innacurate. If it is less than 10 it can be modelled as a pipe so consider using a pipe instead. If it is greater 100 then the pressure loss is to high/not visibly computable")
        
        # define pressure loss coefficient across smooth bend for laminar, compressible flow through sufficiently small pipe curavture
        K = 0.7888 * (2 * self.curvature_ratio)**2.2126 * Re**(-0.7438)
            
        match compressible:
            case False: 
                #incompressible flow

                # calculate pressure differential based off pressure loss coefficient K
                dp = K * (0.5 * state_in.rho * state_in.u**2)
                p_out = p_in - dp 

                # incompressibility definition                
                res1 = (state_in.rho - state_out.rho)/(0.5 * (state_in.rho + state_out.rho))

                # from mass flow rate continuity
                res2 = (state_in.u - state_out.u)/(0.5 * (state_in.u + state_out.u))
                
                # pressure loss due to bending in the pipe
                res3 = (p_out - state_out.p)/(0.5 * (p_out + state_out.p)) 
                
            case True:
                #compressible flow
                
                R = Fluid.get_gas_constant(self.fluid)
                Cp = Fluid.Cp(self.fluid, state_in.T, state_in.p)
                Cv = Fluid.Cv(self.fluid, state_in.T, state_in.p)
                M_out = state_out.u/c_s
                
                # from mass conservation
                res1 = (state_in.mdot - state_out.mdot) / (0.5 * (state_in.mdot + state_out.mdot))  
                
                # from enthalpy conservation (need to verify this)
                Cp_out = Fluid.Cp(self.fluid, state_in.T, state_in.p)
                res2 = (Cp*state_in.T - Cp_out*state_out.T) / (0.5 * (Cp*state_in.T + Cp_out*state_out.T))
                
                # correcting incompressible pressure loss coefficient for compressbility effects, accounting for larger Mach number
                K_comp = K * (1 + 0.35*Mach_in**2)
        
                dp = K_comp * (0.5 * state_in.rho * state_in.u**2)
        
                p_out = state_in.p - dp
        
                res3 = (p_out - state_out.p)/(0.5 * (p_out + state_out.p)) 

        return [res1, res2, res3]