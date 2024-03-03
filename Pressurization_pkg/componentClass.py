import numpy as np
from Pressurization_pkg.Node import Node
from Pressurization_pkg.State import State
from Pressurization_pkg.Utilities import *
from numpy import log10, sqrt, pi
from scipy.optimize import brentq
from CoolProp.CoolProp import PropsSI


class componentClass:

    # diameter [m]:    diameter of the component at the connections
    # name []:         name of the component, if left blank will receive a label
    #                  of 'COMP #'
    def __init__(self, parent_system, diameter, fluid, name="COMP_AUTO"):
        self.parent_system = parent_system
        self.diameter = diameter
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
        mdot = self.node_in.state.mdot
        rho = self.node_in.state.rho
        u = mdot / rho / self.node_out.state.area
        p = self.node_in.state.p
        self.node_out.state.set(rho=rho,u=u,p=p)
        self.node_out.update()

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
        self.length = length
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
        mdot = self.node_in.state.mdot
        rho_in = self.node_in.state.rho
        u_in = self.node_in.state.u
        p_in = self.node_in.state.p
        q_in = self.node_in.state.q
        T_in =PropsSI('T', 'D', rho_in, 'P', p_in, self.fluid)

        # find friction factor
        Re = u_in * self.diameter / fluid_N2O.kinematic_viscosity
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
        rho_out =PropsSI('D', 'T', T_in, 'P', p_out, self.fluid)
        u_out = mdot / rho_out / self.node_out.state.area
        self.node_out.state.set(rho=rho_out,u=u_out,p=p_out)
        self.node_out.update()

'''
## Bend section of the pipe
class Bend(componentClass):

    # length [m]:      length of the straight pipe
    # diameter [m]:    diameter of the source outlet
    # bend_radius [m]  radius of the pipe bend
    # roughtness [N/A]:relative roughness of the pipe internal wall, will be
    #                  calculated from epsilon if not specified
    # epsilon [m]:     roughness of the pipe internal wall, a function of
    #                  material
    def __init__(self, length, diameter, bend_radius, name=None, roughness=None, epsilon=None):
        super().__init__(length, diameter,name)
        self.bend_radius = bend_radius
        if roughness == None:
            if epsilon == None:
                self.epsilon = 0.000025
            else:
                self.epsilon = epsilon
            self.roughness = self.epsilon / self.diameter
        else:
            self.roughness = roughness

    def _update(self):
        # find upstream condition (downstream the prev node)
        p_t_upstream = self.inlet.p_t
        m_dot = self.inlet.m_dot
        v = m_dot / self.fluid.density / (np.pi * self.diameter**2 / 4)
        q = self.fluid.density * v**2 / 2
        p_upstream = p_t_upstream - q
        self.inlet.set(p_downstream=p_upstream)

        # find friction factor
        Re = v * self.diameter / self.fluid.kinematic_viscosity
        non_dim_num = Re * (self.bend_radius/(self.diameter/2))**2
        if non_dim_num > 6:
            friction_factor = 0.316/non_dim_num**0.2 * ((self.diameter/2)/self.bend_radius)**(-0.5)
        elif non_dim_num > 0.034:
            friction_factor = (0.029+0.304*non_dim_num**(-0.25)) * ((self.diameter/2)/self.bend_radius)**(-0.5)
        else:
            print('Bend',self.name,'should be approximated as a straight pipe.')

        # find K value
        K = 0.3 #TODO

        # find downstream condition (upstream the next node)
        PLC = friction_factor * self.length / self.diameter + K
        dp = PLC * q
        self.outlet.set(m_dot, p_t=p_t_upstream-dp, p_upstream=p_upstream-dp)

        return self

## Ball valves
class BallValve(componentClass):

    # length [m]:      length of the straight pipe
    # diameter [m]:    diameter of the source outlet
    # bend_radius [m]  radius of the pipe bend
    # roughtness [N/A]:relative roughness of the pipe internal wall, will be
    #                  calculated from epsilon if not specified
    # epsilon [m]:     roughness of the pipe internal wall, a function of
    #                  material
    def __init__(self, length, diameter, PLC, name=None):
        super().__init__(length, diameter,name)
        self.PLC = PLC

    def _update(self):
        # find upstream condition (downstream the prev node)
        p_t_upstream = self.inlet.p_t
        m_dot = self.inlet.m_dot
        v = m_dot / self.fluid.density / (np.pi * self.diameter**2 / 4)
        q = self.fluid.density * v**2 / 2
        p_upstream = p_t_upstream - q
        self.inlet.set(p_downstream=p_upstream)

        dp = self.PLC * q
        self.outlet.set(m_dot, p_t=p_t_upstream-dp, p_upstream=p_upstream-dp)

        return self
'''