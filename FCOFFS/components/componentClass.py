'''
Description
'''

from numpy import log10, sqrt, pi, log
from scipy.optimize import brentq,fsolve
from CoolProp.CoolProp import PropsSI
import warnings

from ..pressureSystem import PressureSystem
from ..interfaces.interface import Interface
from ..fluids.fluid import Fluid
from ..utilities.Utilities import *
from ..utilities.units import *


class ComponentClass: # we should consider adding a varibale to hold area so we aren't re doing the calculations
    # diameter [m]:    diameter of the component at the connections
    # name []:         name of the component, if left blank will receive a label
    #                  of 'COMP #'
    def __init__(self, parent_system: PressureSystem, diameter: UnitValue, fluid: str, name: str="COMP_AUTO"):
        self.parent_system = parent_system
        self.diameter = diameter
        self.diameter.convert_base_metric()
        self.fluid = fluid
        self.name = name
        self.type = 'component'
        self.node_in = None
        self.node_out = None

    def __str__(self):
        return self.name

    def __repr__(self): #TODO
        return self.name

    def set_connection(self, upstream: Interface, downstream: Interface):
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
                self.node_out = Interface()
            else:
                raise Exception("class.type not in list")

    def initialize(self):
        self.node_in.initialize(parent_system=self.parent_system, area=UnitValue("METRIC", "AREA", "m^2", pi*self.diameter.value**2/4), fluid=self.fluid)
        self.node_out.initialize(parent_system=self.parent_system, area=UnitValue("METRIC", "AREA", "m^2", pi*self.diameter.value**2/4), fluid=self.fluid, rho=self.node_in.state.rho, u=self.node_in.state.u, p=self.node_in.state.p)

    def update(self):
        self.node_in.update()
        self.node_out.update()
        res1 = (self.node_in.state.rho - self.node_out.state.rho)/self.node_in.state.rho
        res2 = (self.node_in.state.u - self.node_out.state.u)/self.node_in.state.u
        res3 = (self.node_in.state.p - self.node_out.state.p)/self.node_in.state.p
        return [res1, res2, res3]


## Striaght section of the pipe
class Pipe(ComponentClass):

    # length [m]:      length of the straight pipe
    # diameter [m]:    diameter of the source outlet
    # roughtness [N/A]:relative roughness of the pipe internal wall, will be
    #                  calculated from epsilon if not specified
    # epsilon [m]:     roughness of the pipe internal wall, a function of
    #                  material
    def __init__(self, parent_system: PressureSystem, diameter: UnitValue, fluid: str, name: str=None, length: UnitValue=0, roughness: float|None=None, epsilon: float|None=None):
        super().__init__(parent_system, diameter, fluid,name)
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
        Re = u_in * self.diameter.value / Fluid.kinematic_viscosity(self.fluid, rho_in)
        def colebrook(f):
            return 1/sqrt(f) + 2*log10(self.roughness/3.7 + 2.51/(Re*sqrt(f)))
        def haaland(f):
            return 1/sqrt(f) + 1.8*log10((self.roughness/3.7)**1.11 + 6.9/Re)
        if Re > 2000:
            friction_factor = brentq(colebrook, 0.005, 0.1)
        else:
            friction_factor = 64 / Re

        # update downstream condition
        PLC = friction_factor * self.length.value / self.diameter.value
        dp = PLC * q_in
        p_out = p_in - dp
        rho_out = Fluid.density(self.fluid, T_in, p_out)
        u_out = mdot / rho_out / self.node_out.state.area.value
        res1 = (rho_out - self.node_out.state.rho)/rho_out
        res2 = (u_out - self.node_out.state.u)/u_out
        res3 = (p_out - self.node_out.state.p)/p_out
        return [res1, res2, res3]


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

class Tank(ComponentClass):
    def __init__(self, parent_system: PressureSystem, diameter: UnitValue, fluid: str, volume: UnitValue, name: str="Tank"):
      
        super().__init__(parent_system, diameter, fluid, name)
        self.volume = volume
        self.volume.convert_base_metric() 
        self.fluid_level = 0  
        self.pressure = None  
        self.temperature = None  

    def __str__(self):
        
        return f"{self.name}: Volume={self.volume.value} m^3, Fluid Level={self.fluid_level} m^3"

    def add_fluid(self, volume):
        
        self.fluid_level += volume
        if self.fluid_level > self.volume.value: # why not just stop users from adding over instead of doing it and throwing error?
            raise ValueError("Fluid level exceeds tank capacity")

    def remove_fluid(self, volume):

        self.fluid_level -= volume 
        if self.fluid_level < 0: #  same here why not just stop users from removing more instead of doing it and throwing error?
            raise ValueError("Cannot remove more fluid than the current level")

    def update_properties(self):
        # Update tank properties based on current state
        pass

    def initialize(self):
        # Initialize tank properties
        super().initialize() 
        # Additional initialization specific to the tank
        self.update_properties()

    def update(self):
        # Update method to adjust tank state and potentially connected nodes
        super().update()
        self.update_properties()
        return []


