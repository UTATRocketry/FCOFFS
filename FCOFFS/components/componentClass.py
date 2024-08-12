'''
Description
'''

from numpy import pi

from ..state.State import *
from ..pressureSystem.PressureSystem import PressureSystem
from ..interfaces.interface import Interface
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
        self.node_in.initialize(parent_system=self.parent_system, area=pi*self.diameter**2/4, fluid=self.fluid)
        self.node_out.initialize(parent_system=self.parent_system, area=pi*self.diameter**2/4, fluid=self.fluid, rho=self.node_in.state.rho, u=self.node_in.state.u, p=self.node_in.state.p)

    def update(self): 
        self.node_in.update()
        self.node_out.update()

    def eval(self, new_states: tuple[State, State]|None=None):
        if new_states is None:
            state_in = self.node_in.state
            state_out = self.node_out.state
        else:
            state_in = new_states[0]
            state_out = new_states[1]

        res1 = (state_in.rho - state_out.rho)/state_in.rho
        res2 = (state_in.u - state_out.u)/state_in.u
        res3 = (state_in.p - state_out.p)/state_in.p
        return [res1, res2, res3]
