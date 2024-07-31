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

    def initialize(self, parent_system: PressureSystem=None, area: UnitValue=None, fluid: str=None, rho: UnitValue=None, u: UnitValue=None, p: UnitValue=None):
        if not self.initialized:
            self.parent_system = parent_system
            self.state.set(area, fluid, rho, u, p)
            self.update()
            self.initialized = True


class PressureInlet(Interface):
    def __init__(self, p: UnitValue, T: UnitValue, name='PressureInlet'):
        super().__init__(name=name)
        self.BC_type = "PressureInlet"
        p.convert_base_metric()
        self.p = p
        T.convert_base_metric()
        self.T = T

    def initialize(self, parent_system: PressureSystem=None, area: UnitValue=None, fluid: str=None, rho: UnitValue=None, u: UnitValue=None, p: UnitValue=None):
        if not self.initialized:
            self.parent_system = parent_system
            rho = Fluid.density(fluid, self.T, self.p)
            u = UnitValue("METRIC", "VELOCITY", "m/s", 5)
            self.state.set(area, fluid, rho, u, self.p)
            self.update()
            self.initialized = True

class PressureOutlet(Interface):
    def __init__(self, p: UnitValue, name='PressureOutlet'):
        super().__init__(name=name)
        self.BC_type = "PressureOutlet"
        p.convert_base_metric()
        self.p = p

    def initialize(self, parent_system: PressureSystem=None, area: UnitValue=None, fluid: str=None, rho: UnitValue=None, u: UnitValue=None, p: UnitValue=None):
        if not self.initialized:
            self.parent_system = parent_system
            rho = Fluid.density(fluid, parent_system.ref_T, self.p)
            p = self.p
            self.state.set(area, fluid, rho, u, p)
            self.update()
            self.initialized = True

class MassOutlet(Interface):
    def __init__(self, mdot: UnitValue, name='MassOutlet'):
        super().__init__(name=name)
        self.BC_type = "MassOutlet"
        mdot.convert_base_metric()
        self.mdot = mdot

    def initialize(self, parent_system: PressureSystem=None, area: UnitValue=None, fluid: UnitValue=None, rho: UnitValue=None, u: UnitValue=None, p: UnitValue=None):
        if not self.initialized:
            self.parent_system = parent_system
            if rho != None:
                rho = Fluid.density(fluid,parent_system.ref_T, parent_system.ref_p)
            p = self.parent_system.ref_p # should these not be self.p and self.u
            u = self.mdot / rho / area
            self.state.set(area, fluid, rho, u, p)
            self.update()
            self.initialized = True
