'''
Description
'''

from ..pressureSystem import PressureSystem
from ..state.State import State
from ..fluids.fluid import Fluid

from ..utilities import *
from ..utilities.units import *


class Interface:
    def __init__(self, name: str="NODE_AUTO"):
        self.name = name
        self.type = 'node'
        self.state = State()
        self.initialized = False

    def __repr__(self):
        return self.name

    def update(self):
        self.state.update()

    def initialize(self, parent_system: PressureSystem=None, area: UnitValue=None, fluid: str=None, rho: float=None, u: float=None, p: float=None):
        if not self.initialized:
            self.parent_system = parent_system
            self.state.set(area, fluid, rho, u, p)
            self.update()
            self.initialized = True


class PressureInlet(Interface):
    def __init__(self, p, T, name='PressureInlet'):
        super().__init__(name=name)
        self.BC_type = "PressureInlet"
        self.p = convert_to_si(p)
        self.T = T

    def initialize(self,parent_system=None,area=None,fluid=None,rho=None,u=None,p=None):
        if not self.initialized:
            self.parent_system = parent_system
            rho = Fluid.density(fluid,self.T,self.p)
            u = 5
            self.state.set(area,fluid,rho,u,self.p)
            self.update()
            self.initialized = True

class PressureOutlet(Interface):
    def __init__(self, p, name='PressureOutlet'):
        super().__init__(name=name)
        self.BC_type = "PressureOutlet"
        self.p = convert_to_si(p)

    def initialize(self,parent_system=None,area=None,fluid=None,rho=None,u=None,p=None):
        if not self.initialized:
            self.parent_system = parent_system
            rho = Fluid.density(fluid,parent_system.ref_T,self.p)
            p = self.p
            self.state.set(area,fluid,rho,u,p)
            self.update()
            self.initialized = True

class MassOutlet(Interface):
    def __init__(self, mdot, name='MassOutlet'):
        super().__init__(name=name)
        self.BC_type = "MassOutlet"
        self.mdot = mdot

    def initialize(self,parent_system=None,area=None,fluid=None,rho=None,u=None,p=None):
        if not self.initialized:
            self.parent_system = parent_system
            if rho != None:
                rho = Fluid.density(fluid,parent_system.ref_T, parent_system.ref_p.value)
            p = self.parent_system.ref_p.value # should these not be self.p and self.u
            u = self.mdot / rho / area
            self.state.set(area,fluid,rho,u,p)
            self.update()
            self.initialized = True
