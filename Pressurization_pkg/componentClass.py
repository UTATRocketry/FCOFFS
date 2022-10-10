from Pressurization_pkg.Node import Node


class componentClass:

    # length [m]:      length of the straight pipe
    # diameter [m]:    diameter of the source outlet
    # name []:         name of the component, if left blank will receive a label
    #                  of 'COMP #'
    def __init__(self, length, diameter, name=None):
        self.length = length
        self.diameter = diameter
        self.name = name
        self.inlet = None
        self.outlet = Node()

    # upstream_component [obj]:  the component that is immediately upstream this
    #                            component
    def _connect(self, upstream_component):
        self.inlet = upstream_component.outlet

    def _compute(self):
        self.dP = 0

    def _update(self):
        self.outlet.set(self.inlet.m_dot, self.inlet.P - self.dP)

## Starting point of the flow
class Source(componentClass):
    # diameter [m]:    diameter of the source outlet
    # m_dot [kg/s]:    mass flow rate from the source
    # P [Pa]:          pressure from the source
    def __init__(self, diameter, m_dot, P, name='Source'):
        super().__init__(0, diameter,name)
        self.m_dot = m_dot
        self.P = P
        self.outlet.set(self.m_dot,self.P)

    def _connect(self,dummy_parameter=None):
        pass

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

    def _compute(self):  #TODO
        self.friction_factor = 0.04
        self.dP = self.friction_factor * self.length / self.diameter