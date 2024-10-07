'''
Description
'''
import numpy as np
import pandas

from FCOFFS.utilities.units import UnitValue
from FCOFFS.systems.system import System
from FCOFFS.systems.steady import SteadySolver
from FCOFFS.fluids.Fluid import Fluid

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
        self.dataframe = pandas.DataFrame({"Time": [], "Interface": [], "Rho": [], "Pressure": [], "Velocity": [], "Temperature": [], "Mass Flow Rate": []})  # provide column labels [time_step, component, rho, p, u, mdot]
        self.Init_dataframe = pandas.DataFrame({"Time": [], "Interface":[], "Rho": [], "Pressure": [], "Velocity": [], "Temperature": [], "Mass Flow Rate": []}) #pandas dataframe

        self.components = components
        self.objects = []
        for component in components[:-1]:
                self.objects += [component, component.interface_out]
                component.initialize() # this will likely be a differtent initialization method 
        self.objects.append(components[-1])
        self.inlet_BC_type = components[0].BC_type
        self.outlet_BC_type = components[-1].BC_type

        # initialize the steady state solver
        self.quasi_steady_solver.initialize(self.components) 
        
    def time_marching(self):
        for component in self.components:
            if callable(getattr(component, "transient")):
                component.transient(self.dt, component.interface_out.state)

    def store_converged_state(self, time: float):
        # store convegred state
        for object in self.objects:
            if object.type == 'interface':
                pandas.concat([self.dataframe, pandas.DataFrame({"Time": [time], "Interface": [object.name], "Rho": [object.state.rho], "Pressure": [object.state.p], "Velocity": [object.state.u], "Temperature": [object.state.T], "Mass Flow Rate": [object.state.mdot]})], ignore_index=True)

    def solve(self):
        #solve system 
        start_time = 0
        N = self.end_time / self.dt
        time = np.linspace(start_time, self.end_time, N)
        for t in time:
            # initialize the steady state solver
            self.quasi_steady_solver.solve(True)
            self.output() # prints what quasi steady solver converged to
            self.store_converged_state(t)

            self.time_marching()
            # update interface state with new component values and print maybe not needed

            #self.store_converged_state("Init") # second store maybve not needed
        
        self.dataframe.to_csv("Transient Result.csv")
        # push datafranmes to csv
           