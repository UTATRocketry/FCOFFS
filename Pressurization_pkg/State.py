'''
This class tracks the state of fluid at each node.
'''

from Pressurization_pkg.Utilities import *

import warnings

class State:
    def __init__(self,area=None,fluid=None,rho=None,u=None,p=None):
        self.area = area         # connection area, typically should not change
        self.fluid = fluid       # fluid type in string
        self.rho = rho           # primitive property; density
        self.u = u               # primitive property; velocity
        self.p = p               # primitive property; pressure

    def __repr__(self):
        return "area = " + str(self.area) + "\nfluid = " + str(self.fluid) + "\nrho = " + str(self.rho) + "\nu = " + str(self.u) + "\np = " + str(self.p) + "\n"

    def update(self):
        # Update other fluid properties based on the primitives
        self.mdot = self.rho * self.u * self.area
        self.q = self.rho * self.u**2 / 2
        self.T = Fluid.T(self.fluid,self.rho,self.p)

    def set(self,area=None,fluid=None,rho=None,u=None,p=None):
        if area != None:
            self.area = area
            if self.area != None and area != self.area:
                warnings.warn("The area changed from " + str(self.area) + " to " + str(area))
        if fluid != None: self.fluid = fluid
        if rho != None: self.rho = rho
        if u != None: self.u = u
        if p != None: self.p = p
        self.update()



