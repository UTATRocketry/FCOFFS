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
    
    def output(self, verbose: bool = True):
        header = f"{'Name':<12} {'Rho':<20} {'Velocity':<20} {'Pressure':<20} {'Temp':<15} {'Mdot':<20} {'Area':<20} {'Fluid':<10}"
        
        output_string = header + "\n" + "-" * len(header) + "\n"
        
        for obj in self.objects:
            if obj.type == 'interface':
                state = obj.state
                
                output_string += f"{obj.name:<12} {str(round(getattr(state, 'rho', 'N/A'), 4)):<20} {str(round(getattr(state, 'u', 'N/A'), 2)):<20} {str(round(getattr(state, 'p', 'N/A'), 4)):<20} {str(round(getattr(state, 'T', 'N/A'), 4)):<15} {str(round(getattr(state, 'mdot', 'N/A'), 4)):<20} {str(round(getattr(state, 'area', 'N/A'), 4)):<20} {getattr(state, 'fluid', 'N/A'):<10}\n"
            else:
                output_string += f"{obj.name:<12}\n"

        # Print the output if verbose is True
        if verbose:
            print("\n" + output_string + "\n")
        
        return output_string

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