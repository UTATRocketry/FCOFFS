'''
Description
'''
import numpy as np

from ..utilities.units import UnitValue
from .system import System
from .steady import SteadySolver

class TransientSolver(System):
    def __init__(self, name: str = "Transient State Solver", ref_T: UnitValue = UnitValue("METRIC", "TEMPERATURE", "K", 293.15), ref_p: UnitValue = UnitValue("METRIC", "PRESSURE", "Pa", 1.01e5)):
        super().__init__(name, ref_T, ref_p)
        self.quasi_steady_state = SteadySolver("Transient Qausi Intemediate", ref_T, ref_p)
        # Stuff I think we will need
        self.end_time = None
        self.dt= None


    def initialize(self, components: list, time_step: float, end_time: float):
        if len(components) < 1:
            raise IndexError('No component found. ')
        if components[0].BC_type != "PRESSURE":
            for component in components:
                if component.decoupler == True:
                    raise TypeError("Using a decoupled system wihtout defining the upstrem pressure. ")

        self.dt = time_step
        self.end_time = end_time

        self.components = components
        self.objects = []
        for component in components[:-1]:
                self.objects += [component, component.interface_out]
                component.initialize() # this will likely be a differtent initialization method 
        self.objects.append(components[-1])
        self.inlet_BC = components[0].BC_type
        self.outlet_BC = components[-1].BC_type

        # initialize the steady state solver
        


    def solve(self):
        #solve system 
        start_time = 0
        N = self.end_time / self.dt
        time = np.linspace(0, self.end_time, N)
        for t in time:
            # initialize the steady state solver
            self.quasi_steady_state.initialize(self.components)
            # run steady state
            self.quasi_steady_state.solve(verbose=False)
            # grab new states produced by quasi solver
            self.components = self.quasi_steady_state.components

            # solve for the new partials uing euler equations
            self.components[0].solve_partials() # idk smt like this
            self.components[-1].solve_partials()

            # next step would be to use partials to step inlet and outlet
            self.components[0].step_in_time(self.dt) # smt like this 
            self.components[-1].step_in_time(self.dt)

            #Then record results of each time step 
           