'''
Description
'''

from ..utilities.units import UnitValue

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
            

    def __repr__(self):
        return str(self.objects)

    def show_tree(self):
        for i in range(len(self.objects)-1):
            print(self.objects[i].name)
            print(' | ')
        print(self.objects[-1].name)
        print()

    def solve(self):
        print("")
        #pretty self explanatory, should be overitten
        pass 