'''
Description
'''

from ..utilities.units import UnitValue
from .system import System
from .steady import SteadySolver

class TransientSolver(System):
    def __init__(self, name: str = "Transient State Solver", ref_T: UnitValue = UnitValue("METRIC", "TEMPERATURE", "K", 293.15), ref_p: UnitValue = UnitValue("METRIC", "PRESSURE", "Pa", 1.01e5)):
        super().__init__(name, ref_T, ref_p)
        self.quasi_steady_state = SteadySolver("Transient Qausi Intemediate", ref_T, ref_p)
        # Stuff I think we will need
        self.partials = None
        self.time_range = None
        self.time_step = None




    def solve(self):
        #solve system 
        pass