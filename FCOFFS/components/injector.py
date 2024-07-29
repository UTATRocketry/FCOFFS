'''
Description
'''

from numpy import sqrt, pi, log
from scipy.optimize import fsolve
from CoolProp.CoolProp import PropsSI
import warnings

from ..components.componentClass import ComponentClass
from ..pressureSystem import PressureSystem
from ..fluids.fluid import Fluid
from ..utilities.units import *


class Injector(ComponentClass):
    def __init__(self, parent_system: PressureSystem, diameter_in: UnitValue, diameter_out: UnitValue, diameter_hole: UnitValue, num_hole: int, fluid: str, name: str='Injector'):
        if fluid not in ['N2O','CO2']:
            raise Exception("Fluid type not supported for injector")
        super().__init__(parent_system, diameter_hole, fluid, name)
        self.diameter_in = diameter_in
        self.diameter_in.convert_base_metric()
        self.diameter_out = diameter_out
        self.diameter_out.convert_base_metric()
        self.diameter_hole = diameter_hole
        self.diameter_hole.convert_base_metric()
        self.num_hole = num_hole

    def initialize(self):
        if self.parent_system.outlet_BC != 'PressureOutlet':
            warnings.warn("Outlet BC not well posed. ")
        self.node_in.initialize(parent_system=self.parent_system, area=UnitValue("METRIC", "AREA", "m^2", pi*self.diameter.value**2/4), fluid=self.fluid)
        self.node_out.initialize(parent_system=self.parent_system, area=UnitValue("METRIC", "AREA", "m^2", pi*self.diameter.value**2/4), fluid=self.fluid, rho=self.node_in.state.rho, u=self.node_in.state.u, p=self.node_in.state.p)

    def update(self):
        self.node_in.update()
        self.node_out.update()
        p_i = self.node_in.state.p
        T_i = self.node_in.state.T
        p_o = self.node_out.state.p
        mass_flux_est = self.get_mass_flux(T_i, p_i, p_o)
        mdot_est = mass_flux_est * (pi*self.diameter_hole.value**2/4) * self.num_hole
        rho_out = Fluid.density(self.fluid, T_i, p_o)
        u_in = mdot_est / self.node_in.state.rho / self.node_in.state.area.value
        u_out = mdot_est / rho_out / self.node_out.state.area.value
        res1 = (rho_out - self.node_out.state.rho)/rho_out
        res2 = (u_out - self.node_out.state.u)/u_out
        res3 = (u_in - self.node_in.state.u)/u_in
        return [res1, res2, res3]


    def get_omega(self, T_i, P_i):
        v_l = 1/PropsSI("D", "T", T_i, "Q", 0, self.fluid)
        v_g = 1/PropsSI("D", "T", T_i, "Q", 1, self.fluid)
        v_lgi = v_g - v_l
        v_i = v_l
        c_li = PropsSI("C", "T", T_i, "Q", 0, self.fluid)
        h_l = PropsSI("H", "T", T_i, "Q", 0, self.fluid)
        h_g = PropsSI("H", "T", T_i, "Q", 1, self.fluid)
        h_lgi = h_g - h_l
        return c_li*T_i*P_i/v_i*(v_lgi/h_lgi)**2


    def get_mass_flux(self, T_i, P_i, P_o):
        P_sat = PropsSI("P", "T", T_i, "Q", 0, self.fluid)
        omega = self.get_omega(T_i, P_i) # unused?
        omega_sat = self.get_omega(T_i, P_sat)
        eta_st = 2*omega_sat/(1+2*omega_sat) # unused?

        # G_crit,sat
        func = lambda eta_crit: eta_crit**2 + (omega_sat**2 - 2*omega_sat)*(1-eta_crit)**2 + 2*(omega_sat**2)*log(eta_crit) + 2*(omega_sat**2)*(1-eta_crit)
        eta_crit = fsolve(func,1)[0]
        v_l = 1/PropsSI("D", "T", T_i, "Q", 0, self.fluid)
        G_crit_sat = eta_crit / sqrt(omega_sat) * sqrt(P_i * 1/v_l)

        # G_low
        eta_sat = P_sat / P_i
        func = lambda eta_crit_low: (omega_sat+(1/omega_sat)-2)/(2*eta_sat)*(eta_crit_low**2) - 2*(omega_sat-1)*eta_crit_low + omega_sat*eta_sat*log(eta_crit_low/eta_sat) + 3/2*omega_sat*eta_sat - 1
        eta_crit_low = fsolve(func,1)[0]
        if P_o < eta_crit_low*P_i:
            eta = eta_crit_low
        else:
            print(T_i,P_i,P_o)
            warnings.warn("Combustion Chamber Pressure does not exceed critical pressure drop; flow is not choked")
            return 0.86 * sqrt(2 * abs(P_i-P_o) * self.node_in.state.rho)
        G_low = sqrt(P_i/v_l) * sqrt(2*(1-eta_sat) + 2*(omega_sat*eta_sat*log(eta_sat/eta) - (omega_sat-1)*(eta_sat-eta)))/(omega_sat*(eta_sat/eta - 1) + 1)

        G = (P_sat/P_i)*G_crit_sat + (1-P_sat/P_i)*G_low
        return G