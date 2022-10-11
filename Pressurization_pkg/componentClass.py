import numpy as np
from Pressurization_pkg.Node import Node
from numpy import log10, sqrt
from scipy.optimize import brentq

class componentClass:

    # length [m]:      length of the straight pipe
    # diameter [m]:    diameter of the source outlet
    # name []:         name of the component, if left blank will receive a label
    #                  of 'COMP #'
    def __init__(self, length, diameter, name=None):
        self.length = length
        self.diameter = diameter
        self.name = name
        self.fluid = None
        self.inlet = None
        self.outlet = Node()

    def __str__(self):
        return self.name

    def __repr__(self): #TODO
        return self.name

    # upstream_component [obj]:  the component that is immediately upstream this
    #                            component
    def _connect(self, upstream_component):
        self.inlet = upstream_component.outlet
        return self

    def _update(self):
        print('No update on',self.name)
        return self

    def _update_fluid(self, fluid):
        self.fluid = fluid
        return self

## Starting point of the flow
class Source(componentClass):
    # diameter [m]:    diameter of the source outlet
    # m_dot [kg/s]:    mass flow rate from the source
    # p [Pa]:          static pressure from the source
    def __init__(self, diameter, m_dot, p, name='Source'):
        super().__init__(0, diameter,name)
        self.outlet.set(m_dot,p_upstream=p)

    def _connect(self,dummy_parameter=None):
        if dummy_parameter != None:
            print('Source cannot be connected to the downstream of', dummy_parameter)
        return self

    def _update(self):
        v = self.outlet.m_dot / self.fluid.density / (np.pi * self.diameter**2 / 4)
        q = self.fluid.density * v**2 / 2
        self.outlet.set(p_t=self.outlet.p_upstream+q)
        return self

## Striaght section of the pipe
class Pipe(componentClass):

    # length [m]:      length of the straight pipe
    # diameter [m]:    diameter of the source outlet
    # roughtness [N/A]:relative roughness of the pipe internal wall, will be
    #                  calculated from epsilon if not specified
    # epsilon [m]:     roughness of the pipe internal wall, a function of
    #                  material
    def __init__(self, length, diameter, name=None, roughness=None, epsilon=None):
        super().__init__(length, diameter,name)
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
        def colebrook(f):
            return 1/sqrt(f) + 2*log10(self.roughness/3.7 + 2.51/(Re*sqrt(f)))
        def haaland(f):
            return 1/sqrt(f) + 1.8*log10((self.roughness/3.7)**1.11 + 6.9/Re)
        if Re > 2000:
            friction_factor = brentq(colebrook, 0.005, 0.1)
        else:
            friction_factor = 64 / Re

        # find downstream condition (upstream the next node)
        PLC = friction_factor * self.length / self.diameter
        dp = PLC * q
        self.outlet.set(m_dot, p_t=p_t_upstream-dp, p_upstream=p_upstream-dp)

        return self

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