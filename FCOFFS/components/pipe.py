'''
Description
'''

from numpy import log10, sqrt, log
from scipy.optimize import brentq

from ..systems.steady import SteadySolver
from ..state.State import *
from ..components.componentClass import ComponentClass
from ..fluids.Fluid import Fluid
from FCOFFS.utilities.units import *

## Striaght section of the pipe
class Pipe(ComponentClass):

    # length [m]:      length of the straight pipe
    # diameter [m]:    diameter of the source outlet
    # roughtness [N/A]:relative roughness of the pipe internal wall, will be
    #                  calculated from epsilon if not specified
    # epsilon [m]:     roughness of the pipe internal wall, a function of
    #                  material
    # height_delta [m]: Difference in heigh between one end of pipe to another, a decrease in height should be a negative value
    def __init__(self, parent_system: SteadySolver, diameter: UnitValue, fluid: str, length: UnitValue, height_delta: UnitValue = UnitValue("METRIC", "DISTANCE", "m", 0), roughness: float|None=None, epsilon: float|None=None, name: str="Pipe"):
        super().__init__(parent_system, diameter, fluid, name)
        self.length = length
        self.length.convert_base_metric()
        self.height_diference = height_delta.convert_base_metric()
        if roughness == None:
            if epsilon == None:
                self.epsilon = 0.000025
            else:
                self.epsilon = epsilon
            self.roughness = self.epsilon / self.diameter.value
        else:
            self.roughness = roughness

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
        Mach_in = state_in.u / c_s

        if Mach_in < 0.3:
            compressible = True
        else:
            compressible = False  

        # find friction factor
        Re = u_in * self.diameter / Fluid.kinematic_viscosity(self.fluid, rho_in)
        def colebrook(f):
            return 1/sqrt(f) + 2*log10(self.roughness/3.7 + 2.51/(Re*sqrt(f)))
        def haaland(f):
            return 1/sqrt(f) + 1.8*log10((self.roughness/3.7)**1.11 + 6.9/Re)
        if Re > 2000:
            friction_factor = brentq(colebrook, 0.005, 0.1)
        else:
            friction_factor = 64 / Re

        match compressible:
            case True: 

                # update downstream condition
                PLC = friction_factor * self.length / self.diameter
                dp = PLC * q_in
                p_out = p_in - dp + state_in.rho*g*self.height_diference # added height factor kg/m^3
                rho_out = Fluid.density(self.fluid, T_in, p_out)
                u_out = mdot / rho_out / state_out.area
                res1 = (rho_out - state_out.rho)/rho_out
                res2 = (u_out - state_out.u)/u_out
                res3 = (p_out - state_out.p)/p_out # add delta_h

            case False:

                fanning_factor = friction_factor/4
                R = Fluid.get_gas_constant(self.fluid)
                Cp = Fluid.Cp(self.fluid, state_in.T, state_in.p)
                Cv = Fluid.Cv(self.fluid, state_in.T, state_in.p)
                gamma = Cp/Cv
                #speed_sound = sqrt(gamma*R*state_in.T)#Fluid.local_speed_sound(self.fluid, state_in.T, state_in.rho)
                #M_in = state_in.u/c_s
                M_in_sqrd = Mach_in**2
                def momentum_equation(M_out):
                    ans = (M_in_sqrd + (gamma*M_in_sqrd*M_out**2)*((4*fanning_factor*self.length/self.diameter)-(((gamma+1)/(2*gamma))*log((M_in_sqrd/M_out**2)*((1+((gamma-1)/(2*gamma))*M_out**2)/(1+((gamma-1)/(2*gamma))*M_in_sqrd))))))**0.5
                    #print(ans)
                    # check this as something weird is happening sometimes
                    return ans

   
                M_out = brentq(momentum_equation, 0.001, 10)
                state_M_out = state_out.u/c_s
                
                #mass conservation
                res1 = (state_in.mdot - state_out.mdot) / (0.5 * (state_in.mdot + state_out.mdot))
                #energy conservation
                res2 = (state_in.u**2 - (2*Cp*(state_out.T- state_in.T) + 2*g*self.height_diference + state_out.u**2)) / (0.5*(Cp*(state_out.T + state_in.T) + g*self.height_diference + 0.5*(state_in.u**2 + state_out.u**2)))
                #Momentum conservation
                res3 = (state_M_out - M_out) / (0.5*(state_M_out + M_out))


        return [res1, res2, res3]