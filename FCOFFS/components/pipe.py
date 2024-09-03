'''
Description
'''

from numpy import log10, sqrt
from scipy.optimize import brentq

from ..pressureSystem.PressureSystem import PressureSystem
from ..state.State import *
from ..components.componentClass import ComponentClass
from ..fluids.Fluid import Fluid
from ..utilities.units import *

## Striaght section of the pipe
class Pipe(ComponentClass):

    # length [m]:      length of the straight pipe
    # diameter [m]:    diameter of the source outlet
    # roughtness [N/A]:relative roughness of the pipe internal wall, will be
    #                  calculated from epsilon if not specified
    # epsilon [m]:     roughness of the pipe internal wall, a function of
    #                  material
    def __init__(self, parent_system: PressureSystem, diameter: UnitValue, fluid: str, name: str=None, length: UnitValue= UnitValue.create_unit("m", 1), roughness: float|None=None, epsilon: float|None=None):
        super().__init__(parent_system, diameter, fluid, name)
        self.length = length
        self.length.convert_base_metric()
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

        # update downstream condition
        PLC = friction_factor * self.length / self.diameter
        dp = PLC * q_in
        p_out = p_in - dp
        rho_out = Fluid.density(self.fluid, T_in, p_out)
        u_out = mdot / rho_out / state_out.area
        res1 = (rho_out - state_out.rho)/rho_out
        res2 = (u_out - state_out.u)/u_out
        res3 = (p_out - state_out.p)/p_out
        return [res1, res2, res3]