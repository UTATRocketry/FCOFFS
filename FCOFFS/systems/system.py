'''
Description
'''

from ..utilities.units import UnitValue
from .output import OutputHandler

# made this for functions and things that are comon accross both solving system classes

class System:
    '''base class for software solving methods'''
    def __init__(self, name: str="Solver System", ref_T: UnitValue=UnitValue("METRIC", "TEMPERATURE", "K", 293.15), ref_p: UnitValue=UnitValue("METRIC", "PRESSURE", "Pa", 1.01e5)):
            self.name = name
            self.w = []          # list of primitives on the nodes
            self.components = []
            self.objects = []
            self.ref_T = ref_T
            self.ref_p = ref_p
            self.ref_p.convert_base_metric()
            self.ref_T.convert_base_metric()
            self.Output = OutputHandler(self.name)

    def __repr__(self):
        return str(self.objects)

    def solve(self):
        print("")
        #pretty self explanatory, should be overitten
        pass 