'''
Description
'''

from numpy import pi

from ..state.State import *
from ..interfaces.interface import Interface
from ..utilities.utilities import *
from ..utilities.units import *


class ComponentClass: # we should consider adding a varibale to hold area so we aren't re doing the calculations
    # diameter [m]:    diameter of the component at the connections
    # name []:         name of the component, if left blank will receive a label
    #                  of 'COMP #'
    def __init__(self, parent_system, diameter: UnitValue, fluid: str, name: str="COMP_AUTO"):
        self.parent_system = parent_system
        self.diameter = diameter
        self.diameter.convert_base_metric()
        self.fluid = fluid
        self.name = name
        self.type = 'component'
        self.decoupler = False
        self.interface_in = None
        self.interface_out = None
        
    def __str__(self):
        return self.name

    def __repr__(self): #TODO
        return self.name

    def set_connection(self, upstream: Interface|None = None, downstream: Interface|None = None):
        if upstream is not None:
            if upstream.type == 'interface':
                self.interface_in = upstream
            elif upstream.type == 'component':
                self.interface_in = upstream.interface_out
            else:
                raise Exception("class.type not in list")
        if downstream is not None:
            if downstream.type == 'interface':
                self.interface_out = downstream
            elif downstream.type == 'component':
                self.interface_out = Interface()
            else:
                raise Exception("class.type not in list")

    def initialize(self):
        if self.interface_in is not None:
            self.interface_in.initialize(parent_system=self.parent_system, area=pi*self.diameter**2/4, fluid=self.fluid)
        if self.interface_out is not None:
            self.interface_out.initialize(parent_system=self.parent_system, area=pi*self.diameter**2/4, fluid=self.fluid, rho=self.interface_in.state.rho, u=self.interface_in.state.u, p=self.interface_in.state.p)

    def update(self):
        if self.interface_in is not None:
            self.interface_in.update()
        if self.interface_out is not None:
            self.interface_out.update()

    def eval(self, new_states: tuple[State, State]|None=None) -> list:
        if new_states is None:
            state_in = self.interface_in.state
            state_out = self.interface_out.state
        else:
            state_in = new_states[0]
            state_out = new_states[1]

        res1 = (state_in.rho - state_out.rho)/state_in.rho
        res2 = (state_in.u - state_out.u)/state_in.u
        res3 = (state_in.p - state_out.p)/state_in.p
        return [res1, res2, res3]

    def transient(self, dt, state_in, state_out):
        pass