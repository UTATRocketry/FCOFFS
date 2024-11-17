'''
Description
'''
import numpy as np
import pandas

from FCOFFS.utilities.units import UnitValue
from FCOFFS.systems.system import System
from FCOFFS.systems.steady import SteadySolver
from FCOFFS.fluids.Fluid import Fluid
from .output import OutputHandler

class TransientSolver(System):
    def __init__(self, name: str = "Transient State Solver", ref_T: UnitValue = UnitValue("METRIC", "TEMPERATURE", "K", 293.15), ref_p: UnitValue = UnitValue("METRIC", "PRESSURE", "Pa", 1.01e5)):
        super().__init__(name, ref_T, ref_p)
        self.quasi_steady_solver = SteadySolver("Transient Quasi Intemediate", ref_T, ref_p)
        self.dt = 0.1

    def initialize(self, components: list):
        if len(components) < 1:
            raise IndexError('No component found. ')
        if components[0].BC_type != "PRESSURE":
            for component in components:
                if component.decoupler == True:
                    raise TypeError("Using a decoupled system wihtout defining the upstrem pressure. ")

        self.components = components

        # initialize the steady state solver
        self.quasi_steady_solver.initialize(self.components) 
        self.quasi_steady_solver.Output.toggle_active()

        self.objects = self.quasi_steady_solver.objects
        self.inlet_BC_type = self.quasi_steady_solver.inlet_BC
        self.outlet_BC_type = self.quasi_steady_solver.outlet_BC

        self.Output.initialize(self.objects)
        self.quasi_steady_solver.Output.residual_queue = self.Output.residual_queue

    def time_marching(self):
        for component in self.components:
            if callable(getattr(component, "transient")):
                if component.interface_in and component.interface_out:
                    component.transient(self.dt, component.interface_in.state, component.interface_out.state)
                elif component.interface_out: 
                    component.transient(self.dt, None, component.interface_out.state)
                elif component.interface_in:
                    component.transient(self.dt, component.interface_in.state, None)


    def solve(self, simulation_time: float, dt: float = 0.1):
        #solve system 
        self.dt = UnitValue.create_unit("s", dt)
        self.simulation_time = simulation_time
        t = 0
        while t <= self.simulation_time:
            # initialize the steady state solver
            self.quasi_steady_solver.solve() # False 
            self.Output._run(dt)
            self.time_marching()
            t += dt

        self.Output._finish()
        # push datafranmes to csv
           