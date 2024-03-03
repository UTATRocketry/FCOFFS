from Pressurization_pkg.State import State
from Pressurization_pkg.Utilities import *


class Node:
    def __init__(self,name="NODE_AUTO"):
        self.name = name
        self.type = 'node'
        self.state = State()
        self.initialized = False

    def __repr__(self):
        return self.name

    def update(self):
        self.state.update()

    def initialize(self,parent_system=None,area=None,fluid=None,rho=None,u=None,p=None):
        if not self.initialized:
            self.parent_system = parent_system
            self.state.set(area,fluid,rho,u,p)
            self.update()
            self.initialized = True


class PressureInlet(Node):
    def __init__(self, p, T, name='PressureInlet'):
        super().__init__(name=name)
        self.BC_type = "PressureInlet"
        self.p = p
        self.T = T

    def initialize(self,parent_system=None,area=None,fluid=None,rho=None,u=None,p=None):
        if not self.initialized:
            self.parent_system = parent_system
            rho = Fluid.density(fluid,self.T,self.p)
            u = 1
            self.state.set(area,fluid,rho,u,self.p)
            self.update()
            self.initialized = True

class PressureOutlet(Node):
    def __init__(self, p, name='PressureOutlet'):
        super().__init__(name=name)
        self.BC_type = "PressureOutlet"
        self.p = p

    def initialize(self,parent_system=None,area=None,fluid=None,rho=None,u=None,p=None):
        if not self.initialized:
            self.parent_system = parent_system
            rho = Fluid.density(fluid,parent_system.ref_T,self.p)
            p = self.p
            self.state.set(area,fluid,rho,u,p)
            self.update()
            self.initialized = True

class MassOutlet(Node):
    def __init__(self, mdot, name='MassOutlet'):
        super().__init__(name=name)
        self.BC_type = "MassOutlet"
        self.mdot = mdot

    def initialize(self,parent_system=None,area=None,fluid=None,rho=None,u=None,p=None):
        if not self.initialized:
            self.parent_system = parent_system
            if rho != None:
                rho = Fluid.density(fluid,parent_system.ref_T,parent_system.ref_p)
            p = self.parent_system.ref_p
            u = self.mdot / rho / area
            self.state.set(area,fluid,rho,u,p)
            self.update()
            self.initialized = True

'''
class Outlet(Node):
    def __init__(self, name='Outlet'):
        super().__init__(name=name)
'''