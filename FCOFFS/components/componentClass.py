import numpy as np
from ..nodes.Node import Node
from ..state.State import State
from ..utilities.Utilities import *
from numpy import log10, sqrt, pi, log
from scipy.optimize import brentq,fsolve,newton
from CoolProp.CoolProp import PropsSI
import warnings


class componentClass:

    # diameter [m]:    diameter of the component at the connections
    # name []:         name of the component, if left blank will receive a label
    #                  of 'COMP #'
    def __init__(self, parent_system, diameter, fluid, name="COMP_AUTO"):
        self.parent_system = parent_system
        self.diameter = convert_to_si(diameter)
        self.fluid = fluid
        self.name = name
        self.type = 'component'
        self.node_in = None
        self.node_out = None

    def __str__(self):
        return self.name

    def __repr__(self): #TODO
        return self.name

    def set_connection(self, upstream, downstream):
        if upstream != None:
            if upstream.type == 'node':
                self.node_in = upstream
            elif upstream.type == 'component':
                self.node_in = upstream.node_out
            else:
                raise Exception("class.type not in list")
        if downstream != None:
            if downstream.type == 'node':
                self.node_out = downstream
            elif downstream.type == 'component':
                self.node_out = Node()
            else:
                raise Exception("class.type not in list")

    def initialize(self):
        self.node_in.initialize(parent_system=self.parent_system,area=pi*self.diameter**2/4,fluid=self.fluid)
        self.node_out.initialize(parent_system=self.parent_system,area=pi*self.diameter**2/4,fluid=self.fluid,rho=self.node_in.state.rho,u=self.node_in.state.u,p=self.node_in.state.p)

    def update(self):
        self.node_in.update()
        self.node_out.update()
        res1 = (self.node_in.state.rho - self.node_out.state.rho)/self.node_in.state.rho
        res2 = (self.node_in.state.u - self.node_out.state.u)/self.node_in.state.u
        res3 = (self.node_in.state.p - self.node_out.state.p)/self.node_in.state.p
        return [res1, res2, res3]

## Striaght section of the pipe
class Pipe(componentClass):

    # length [m]:      length of the straight pipe
    # diameter [m]:    diameter of the source outlet
    # roughtness [N/A]:relative roughness of the pipe internal wall, will be
    #                  calculated from epsilon if not specified
    # epsilon [m]:     roughness of the pipe internal wall, a function of
    #                  material
    def __init__(self, parent_system, diameter, fluid, name=None, length=0, roughness=None, epsilon=None):
        super().__init__(parent_system, diameter,fluid,name)
        self.length = convert_to_si(length)
        if roughness == None:
            if epsilon == None:
                self.epsilon = 0.000025
            else:
                self.epsilon = epsilon
            self.roughness = self.epsilon / self.diameter
        else:
            self.roughness = roughness

    def update(self):
        # find upstream condition
        self.node_in.update()
        self.node_out.update()
        mdot = self.node_in.state.mdot
        rho_in = self.node_in.state.rho
        u_in = self.node_in.state.u
        p_in = self.node_in.state.p
        q_in = self.node_in.state.q
        T_in = self.node_in.state.T

        # find friction factor
        Re = u_in * self.diameter / Fluid.kinematic_viscosity(self.fluid,rho_in)
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
        u_out = mdot / rho_out / self.node_out.state.area
        res1 = (rho_out - self.node_out.state.rho)/rho_out
        res2 = (u_out - self.node_out.state.u)/u_out
        res3 = (p_out - self.node_out.state.p)/p_out
        return [res1, res2, res3]

class Injector(componentClass):
    def __init__(self, parent_system, diameter_in, diameter_out, diameter_hole, num_hole, fluid, name='Injector'):
        if fluid not in ['N2O','CO2']:
            raise Exception("Fluid type not supported for injector")
        super().__init__(parent_system,diameter_hole,fluid,name)
        self.diameter_in = convert_to_si(diameter_in)
        self.diameter_out = convert_to_si(diameter_out)
        self.diameter_hole = convert_to_si(diameter_hole)
        self.num_hole = num_hole

    def initialize(self):
        if self.parent_system.outlet_BC != 'PressureOutlet':
            warnings.warn("Outlet BC not well posed. ")
        self.node_in.initialize(parent_system=self.parent_system,area=pi*self.diameter_in**2/4,fluid=self.fluid)
        self.node_out.initialize(parent_system=self.parent_system,area=pi*self.diameter_out**2/4,fluid=self.fluid,rho=self.node_in.state.rho,u=self.node_in.state.u,p=self.node_in.state.p)

    def update(self):
        self.node_in.update()
        self.node_out.update()
        p_i = self.node_in.state.p
        T_i = self.node_in.state.T
        p_o = self.node_out.state.p
        mass_flux_est = self.get_mass_flux(T_i,p_i,p_o)
        mdot_est = mass_flux_est * (pi*self.diameter_hole**2/4) * self.num_hole
        rho_out = Fluid.density(self.fluid,T_i,p_o)
        u_in = mdot_est / self.node_in.state.rho / self.node_in.state.area
        u_out = mdot_est / rho_out / self.node_out.state.area
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
        omega = self.get_omega(T_i, P_i)
        omega_sat = self.get_omega(T_i, P_sat)
        eta_st = 2*omega_sat/(1+2*omega_sat)

        # G_crit,sat
        func = lambda eta_crit: eta_crit**2 + (omega_sat**2 - 2*omega_sat)*(1-eta_crit)**2 + 2*(omega_sat**2)*log(eta_crit) + 2*(omega_sat**2)*(1-eta_crit)
        eta_crit = fsolve(func,1)[0]
        v_l = 1/PropsSI("D", "T", T_i, "Q", 0, self.fluid)
        G_crit_sat = eta_crit / sqrt(omega_sat) * sqrt(P_i * 1/v_l);

        # G_low
        eta_sat = P_sat / P_i;
        func = lambda eta_crit_low: (omega_sat+(1/omega_sat)-2)/(2*eta_sat)*(eta_crit_low**2) - 2*(omega_sat-1)*eta_crit_low + omega_sat*eta_sat*log(eta_crit_low/eta_sat) + 3/2*omega_sat*eta_sat - 1
        eta_crit_low = fsolve(func,1)[0]
        if P_o < eta_crit_low*P_i:
            eta = eta_crit_low
        else:
            print(T_i,P_i,P_o)
            warnings.warn("Combustion Chamber Pressure does not exceed critical pressure drop; flow is not choked")
            return 0.86 * sqrt(2 * abs(P_i-P_o) * self.node_in.state.rho)
        G_low = sqrt(P_i/v_l) * sqrt(2*(1-eta_sat) + 2*(omega_sat*eta_sat*log(eta_sat/eta) - (omega_sat-1)*(eta_sat-eta)))/(omega_sat*(eta_sat/eta - 1) + 1)

        G = (P_sat/P_i)*G_crit_sat + (1-P_sat/P_i)*G_low;
        return G

