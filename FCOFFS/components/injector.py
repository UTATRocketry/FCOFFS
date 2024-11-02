'''
Description
'''

from numpy import sqrt, pi, log
from scipy.optimize import fsolve
from CoolProp.CoolProp import PropsSI
import warnings

from ..systems.steady import SteadySolver
from ..state.State import *
from ..components.componentClass import ComponentClass
from ..fluids.Fluid import Fluid
from ..utilities.units import *

class Injector(ComponentClass):
    def __init__(self, parent_system: SteadySolver, diameter_in: UnitValue, diameter_out: UnitValue, diameter_hole: UnitValue, num_hole: int, fluid: str, name: str='Injector'):
        if fluid not in ['N2O','CO2','N2']:
            raise Exception("Fluid type not supported for injector")
        super().__init__(parent_system, diameter_hole, fluid, name)
        self.diameter_in = diameter_in
        self.diameter_in.convert_base_metric()
        self.diameter_out = diameter_out
        self.diameter_out.convert_base_metric()
        self.diameter_hole = diameter_hole
        self.diameter_hole.convert_base_metric()
        self.num_hole = num_hole
        self.decoupler = True

    def initialize(self):
        if self.parent_system.outlet_BC != 'PRESSURE':
            warnings.warn("Outlet BC not well posed. ")
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

        p_i = state_in.p
        T_i = state_in.T
        p_o = state_out.p
        mass_flux_est = UnitValue("METRIC", "MASS FLUX", "kg/m^2s", self.get_mass_flux(T_i, p_i, p_o, state_in.rho))
        mdot_est = mass_flux_est * (pi*self.diameter_hole**2/4) * self.num_hole
        rho_out = Fluid.density(self.fluid, T_i, p_o)
        u_in = mdot_est / state_in.rho / state_in.area
        u_out = mdot_est / rho_out / state_out.area
        res1 = (rho_out - state_out.rho)/rho_out
        res2 = (u_out - state_out.u)/u_out
        res3 = (u_in - state_in.u)/u_in
        return [res1, res2, res3]


    def get_omega(self, T_i: float, P_i: float):
        v_l = 1/PropsSI("D", "T", T_i, "Q", 0, self.fluid)
        v_g = 1/PropsSI("D", "T", T_i, "Q", 1, self.fluid)
        v_lgi = v_g - v_l
        v_i = v_l
        c_li = PropsSI("C", "T", T_i, "Q", 0, self.fluid)
        h_l = PropsSI("H", "T", T_i, "Q", 0, self.fluid)
        h_g = PropsSI("H", "T", T_i, "Q", 1, self.fluid)
        h_lgi = h_g - h_l
        return c_li*T_i*P_i/v_i*(v_lgi/h_lgi)**2


    def get_mass_flux(self, T_i, P_i, P_o, rho_in):
        P_sat = PropsSI("P", "T", T_i.value, "Q", 0, self.fluid)
        omega = self.get_omega(T_i.value, P_i.value) # unused?
        omega_sat = self.get_omega(T_i.value, P_sat)
        eta_st = 2*omega_sat/(1+2*omega_sat) # unused?

        # G_crit,sat
        func = lambda eta_crit: eta_crit**2 + (omega_sat**2 - 2*omega_sat)*(1-eta_crit)**2 + 2*(omega_sat**2)*log(eta_crit) + 2*(omega_sat**2)*(1-eta_crit)
        eta_crit = fsolve(func,1)[0]
        v_l = 1/PropsSI("D", "T", T_i.value, "Q", 0, self.fluid)
        G_crit_sat = eta_crit / sqrt(omega_sat) * sqrt(P_i.value * 1/v_l)

        # G_low
        eta_sat = P_sat / P_i.value
        func = lambda eta_crit_low: (omega_sat+(1/omega_sat)-2)/(2*eta_sat)*(eta_crit_low**2) - 2*(omega_sat-1)*eta_crit_low + omega_sat*eta_sat*log(eta_crit_low/eta_sat) + 3/2*omega_sat*eta_sat - 1
        eta_crit_low = fsolve(func,1)[0]
        if P_o < eta_crit_low*P_i:
            eta = eta_crit_low
        else:
            print(T_i,P_i,P_o)
            warnings.warn("Combustion Chamber Pressure does not exceed critical pressure drop; flow is not choked")
            return 0.86 * sqrt(2 * abs(P_i.value-P_o.value) * rho_in.value)
        G_low = sqrt(P_i.value/v_l) * sqrt(2*(1-eta_sat) + 2*(omega_sat*eta_sat*log(eta_sat/eta) - (omega_sat-1)*(eta_sat-eta)))/(omega_sat*(eta_sat/eta - 1) + 1)

        G = (P_sat/P_i.value)*G_crit_sat + (1-P_sat/P_i.value)*G_low
        return G