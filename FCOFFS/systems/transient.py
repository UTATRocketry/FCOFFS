'''
Description
'''
import numpy as np
import pandas

from ..utilities.units import UnitValue
from .system import System
from .steady import SteadySolver

class TransientSolver(System):
    def __init__(self, name: str = "Transient State Solver", ref_T: UnitValue = UnitValue("METRIC", "TEMPERATURE", "K", 293.15), ref_p: UnitValue = UnitValue("METRIC", "PRESSURE", "Pa", 1.01e5)):
        super().__init__(name, ref_T, ref_p)
        self.quasi_steady_solver = SteadySolver("Transient Qausi Intemediate", ref_T, ref_p)
        # Stuff I think we will need
        self.simulation_time = None
        self.dt = 0.1 # seconds


    def initialize(self, components: list, simulation_time: float):
        if len(components) < 1:
            raise IndexError('No component found. ')
        if components[0].BC_type != "PRESSURE":
            for component in components:
                if component.decoupler == True:
                    raise TypeError("Using a decoupled system wihtout defining the upstrem pressure. ")

        self.end_time = simulation_time
        self.conv_dataframe = pandas.DataFrame()  # provide column labels [time_step, component, rho, p, u, mdot]
        self.Init_dataframe = None #pandas dataframe

        self.components = components
        self.objects = []
        for component in components[:-1]:
                self.objects += [component, component.interface_out]
                component.initialize() # this will likely be a differtent initialization method 
        self.objects.append(components[-1])
        self.inlet_BC = components[0].BC_type
        self.outlet_BC = components[-1].BC_type

        # initialize the steady state solver
        self.quasi_steady_solver.initialize(self.components) 
        
    def state_time_marching(self):
        # time march all components
        #loop each component and time march each component state
        for component in self.components[1:-1]:
            #use array of bcs at inlet (2) and outlet (1), inteprolate if needed for dt 
            #inlet and outlet don't have interface on both sides need BCs
            dp = component.interface_in.state.p - component.interface_out.state.p
        #deal with inlet and outlet 
        pass

    def store_converged_state(self, state_type: str):
        # save state into file 1 or 2 depending on if it is converged or intialized state
        # add state to appropriate dataframe
        
        for component in self.components:
            # add to dataframe 
            

        pass

    def solve(self):
        #solve system 
        start_time = 0
        N = self.end_time / self.dt
        time = np.linspace(0, self.end_time, N)
        for _ in time:
            # initialize the steady state solver
            self.quasi_steady_solver.solve(False)
            self.output() # prints what quasi steady solver converged to
            self.store_converged_state("Conv")

            self.state_time_marching()
            self.output()
            self.store_converged_state("Init")
        
        # push datafranmes to csv
           