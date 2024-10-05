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


    def initialize(self, components: list, simulation_time: float, Inlet_BC: list[tuple], Outlet_BC: list[tuple]):
        if len(components) < 1:
            raise IndexError('No component found. ')
        if components[0].BC_type != "PRESSURE":
            for component in components:
                if component.decoupler == True:
                    raise TypeError("Using a decoupled system wihtout defining the upstrem pressure. ")
        if len(Inlet_BC) == 0 and len(Outlet_BC) == 0:
            raise IndexError("Insufficinet Boundary Conditions Provided")

        self.end_time = simulation_time
        self.Conv_dataframe = pandas.DataFrame()  # provide column labels [time_step, component, rho, p, u, mdot]
        self.Init_dataframe = pandas.DataFrame() #pandas dataframe
        self.inlet_BC = Inlet_BC
        self.outlet_BC = Outlet_BC

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
        
    def state_time_marching(self, time):
        for ind, bc in enumerate(self.inlet_BC): # inlet bc maybe not needed??
            if time == bc[0]:
                in_BC = bc[1]
            elif time > bc[0]:
                in_BC = (time - self.inlet_BC[ind-1][0])*((bc[1] - self.inlet_BC[ind-1][1])/(bc[0] - self.inlet_BC[ind-1][0])) + self.inlet_BC[ind-1][1]
        for ind, bc in enumerate(self.outlet_BC):
            if time == bc[0]:
                out_BC = bc[1]
            elif time > bc[0]:
                out_BC = (time - self.inlet_BC[ind-1][0])*((bc[1] - self.inlet_BC[ind-1][1])/(bc[0] - self.inlet_BC[ind-1][0])) + self.inlet_BC[ind-1][1]
        
        for component in self.components[1:-1]:
            #use array of bcs at inlet (2) and outlet (1), inteprolate if needed for dt 
            #inlet and outlet don't have interface on both sides need BCs
            dp = component.interface_in.state.p - component.interface_out.state.p
            u_next = component.interface_in.state.u - self.dt * (dp/component.interface_in.state.rho)
            T_next = component.interface_in.state.T + (component.interface_in.state.u**2-u_next**2)/(2*Fluid.Cp(component.interface_in.state.fluid, component.interface_in.state.T, component.interface_in.state.p)) 
            P_next = Fluid.pressure(component.interface_in.state.fluid, component.interface_in.state.rho, T_next)
            component.interface_in.state.u = u_next
            component.interface_in.state.T = T_next
            component.interface_in.state.p = P_next
        #deal with inlet and outlet 
        dp = self.components[-1].interface_in.state.p - out_BC
        u_next = self.components[-1].interface_in.state.u - self.dt * (dp/self.components[-1].interface_in.state.rho)
        T_next = self.components[-1].interface_in.state.T + (self.components[-1].interface_in.state.u**2-u_next**2)/(2*Fluid.Cp(self.components[-1].interface_in.state.fluid, self.components[-1].interface_in.state.T, self.components[-1].interface_in.state.p)) 
        P_next = Fluid.pressure(self.components[-1].interface_in.state.fluid, self.components[-1].interface_in.state.rho, T_next)
        self.components[-1].interface_in.state.u = u_next
        self.components[-1].interface_in.state.T = T_next
        self.components[-1].interface_in.state.p = P_next

    def store_converged_state(self, state_type: str):
        # save state into file 1 or 2 depending on if it is converged or intialized state
        # add state to appropriate dataframe
        
        for component in self.components:
            # add to dataframe 
            pass
        pass

    def solve(self):
        #solve system 
        start_time = 0
        N = self.end_time / self.dt
        time = np.linspace(0, self.end_time, N)
        for t in time:
            # initialize the steady state solver
            self.quasi_steady_solver.solve(False)
            self.output() # prints what quasi steady solver converged to
            #self.store_converged_state("Conv")

            self.state_time_marching(t)
            self.output()
            #self.store_converged_state("Init")
        
        # push datafranmes to csv
           