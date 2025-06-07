from numpy import log10, sqrt, log, pi
from scipy.optimize import brentq

from ..systems.steady import SteadySolver
from ..state.State import *
from .componentClass import ComponentClass
from FCOFFS.utilities.component_curve import ComponentCurve
from ..fluids.Fluid import Fluid
from FCOFFS.utilities.units import *


class SmoothBend(ComponentClass):
    '''Ninety Degeree bend'''
    def __init__(self, parent_system: SteadySolver, diameter: UnitValue, radius_of_curvature: UnitValue, fluid: str, name: str="SmoothBend"):
        super().__init__(parent_system, diameter, fluid, name)
        
        self.bend_radius = radius_of_curvature.convert_base_metric()
        self.diameter_to_bend_ratio = 0.5*self.diameter/self.bend_radius
        if roughness == None:
            if epsilon == None:
                self.epsilon = 0.000025
            else:
                self.epsilon = epsilon
            self.roughness = self.epsilon / self.diameter.value 
        else:
            self.roughness = roughness

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

        # find friction factor
        Re = u_in * self.diameter / Fluid.kinematic_viscosity(self.fluid, rho_in)
        
        def ito():
            return 0.029*self.diameter_to_bend_ratio**0.5 + 0.304*(Re*self.diameter_to_bend_ratio**2)**(-0.25) 
        def colebrook(f):
            return 1/sqrt(f) + 2*log10(self.roughness/3.7 + 2.51/(Re*sqrt(f)))
        
        if Re*self.diameter_to_bend_ratio**2 > 0.034 and Re*self.diameter_to_bend_ratio**2 < 300:
            friction_factor = ito()
        elif Re*self.diameter_to_bend_ratio**2 < 0.034:
            if Re > 2000:
                friction_factor = brentq(colebrook, 0.005, 0.1)
            else:
                friction_factor = 64 / Re

        

        match compressible:
            case False: 

                # update downstream condition
                PLC = friction_factor * self.length / self.diameter
                dp = PLC * q_in 
                p_out = p_in - dp + state_in.rho*g*self.height_diference # added height factor kg/m^3
                # rho_out = Fluid.density(self.fluid, state_out.T, p_out)
                res1 = (state_in.rho - state_out.rho)/(0.5 * (state_in.rho + state_out.rho))
                #Add temperature residual
                res2 = (state_in.u - state_out.u)/(0.5 * (state_in.u + state_out.u))
                res3 = (p_out - state_out.p)/(0.5 * (p_out + state_out.p)) # add delta_h

            case True:

                fanning_factor = friction_factor/4
                R = Fluid.get_gas_constant(self.fluid)
                Cp = Fluid.Cp(self.fluid, state_in.T, state_in.p)
                Cv = Fluid.Cv(self.fluid, state_in.T, state_in.p)
                gamma = Cp/Cv
                M_in_sqrd = Mach_in**2
                M_out = state_out.u/c_s
                
                #mass conservation
                res1 = (state_in.mdot - state_out.mdot) / (0.5 * (state_in.mdot + state_out.mdot))
                #energy conservation # maybe do enthalpy consevrartion  #density is not constant v^2/2 + CP(T) # only do conservation of enthalpy
                #res2 = (state_in.u**2 - (2*Cp*(state_out.T- state_in.T) + 2*g*self.height_diference + state_out.u**2)) / (0.5*(Cp*(state_out.T + state_in.T) + g*self.height_diference + 0.5*(state_in.u**2 + state_out.u**2)))
                #enthalpy conservation
                Cp_out = Fluid.Cp(self.fluid, state_in.T, state_in.p)
                res2 = (Cp*state_in.T - Cp_out*state_out.T) / (0.5 * (Cp*state_in.T + Cp_out*state_out.T))
                
                #Momentum conservation # momentum euqstion go to zero
                res3 = (M_in_sqrd + (gamma*M_in_sqrd*M_out**2)*((4*fanning_factor*self.length/(self.diameter))-(((gamma+1)/(2*gamma))*log((M_in_sqrd/M_out**2)*((1+((gamma-1)/(2*gamma))*M_out**2)/(1+((gamma-1)/(2*gamma))*M_in_sqrd))))))**0.5 - M_out


        return [res1, res2, res3]