'''
This class tracks the state of fluid at each node.
'''

import warnings

from ..fluids.fluid import Fluid
from ..utilities.units import UnitValue
from ..utilities.Utilities import *


class State:
    def __init__(self, area: UnitValue=None, fluid: str=None, rho: UnitValue=None, u: UnitValue=None, p: UnitValue=None) -> None:
        self.area = area         # connection area, typically should not change
        self.fluid = fluid       # fluid type in string
        self.rho = rho           # primitive property; density
        self.u = u               # primitive property; velocity
        self.p = p               # primitive property; pressure

    def __repr__(self) -> str:
        return "area = " + str(self.area) + "\nfluid = " + str(self) + "\nrho = " + str(self.rho) + "\nu = " + str(self.u) + "\np = " + str(self.p) + "\n"

    def update(self) -> None:
        # Update other fluid properties based on the primitives
        self.mdot = self.rho * self.u * self.area 
        self.q = self.rho * self.u**2 / 2
        self.T = Fluid.temp(self.fluid, self.rho, self.p)

    def set(self, area: UnitValue=None, fluid: str=None, rho: float=None, u: float=None, p: float=None) -> None:
        if area != None:
            self.area = area
            if self.area != None and area.value != self.area.value: # why is their a secon check if  None twice
                warnings.warn("The area changed from " + str(self.area.value) + " to " + str(area.value))
        if fluid != None: self.fluid = fluid
        if rho != None: self.rho = rho
        if u != None: self.u = u
        if p != None: self.p = p
        self.update()



