'''
Description
'''

from numpy import log10, sqrt, log, pi
from scipy.optimize import brentq

from ..systems.steady import SteadySolver
from ..state.State import *
from ..components.componentClass import ComponentClass
from ..fluids.Fluid import Fluid
from FCOFFS.utilities.units import *
from FCOFFS.utilities.utilities import Newtons_Method

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
        def colebrook(f):
            return 1/sqrt(f) + 2*log10(self.roughness/3.7 + 2.51/(Re*sqrt(f)))
        def haaland(f):
            return 1/sqrt(f) + 1.8*log10((self.roughness/3.7)**1.11 + 6.9/Re)
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
  
if __name__ == "__main__":
    # testing items whihc can be removed
    M_in_sqrd = 0.4225
    gamma = 1.27
    fanning_factor = 0.02
    length = 0.0001
    diameter = 0.001 

    alpha = M_in_sqrd**0.5
    beta = gamma * M_in_sqrd 
    gamma2 = 4*fanning_factor*length/diameter
    delta = (gamma+1)/(2*gamma)
    sigma = (gamma-1)/2 
    epsilon = 1 + sigma*alpha**2
    
    def Newtons_Method(f,fprime):
        tolerance = 1e-9
        x_approx = 2 #initial guess
        step = 0 #to keep track of number of iterations
        while f(x_approx) > tolerance:
            #estimate the successive value
            x_approx = x_approx - f(x_approx) / fprime(x_approx)
            step += 1
            if step > 1000:
                raise Exception(f"Could not converge on root of function. Last guess was: {x_approx}")
        return x_approx
    
    def momentum_equation(M_out):
        constant = (4 * fanning_factor * length) / diameter
        first_term = (M_out**2 - M_in_sqrd)/(gamma*M_in_sqrd*M_out**2)
        mult = (gamma+1)/(2*gamma)
        top = 1 + (((gamma - 1)/2)*M_out**2)
        bottom = 1 + (((gamma - 1)/2)*M_in_sqrd)
        inside_log = (M_in_sqrd/M_out**2)*(top/bottom)
        natural_log = log(inside_log)

        ans = first_term + mult*natural_log - constant

        #ans = (M_in_sqrd + (gamma*M_in_sqrd*M_out**2)*((4*fanning_factor*length/diameter)-(((gamma+1)/(2*gamma))*log((M_in_sqrd/M_out**2)*((1+((gamma-1)/(2*gamma))*M_out**2)/(1+((gamma-1)/(2*gamma))*M_in_sqrd))))))**0.5 - M_out
        #print(ans)
        return ans
    
    def momentum_equation_derivative(M_out):
        top = 4*(M_out**2 - 1)
        bottom = (gamma*M_out**3)*((gamma-1)*M_out**2 + 2) 
        ans = -1*(top/bottom)
        return ans
    
    M_out = Newtons_Method(momentum_equation, momentum_equation_derivative) #plot in desmos for confidence # ask about solving method
    
    print(M_out)