'''
Description
'''

from scipy.optimize import root

from .system import System
from ..utilities.utilities import rms
from ..utilities.units import UnitValue

# Nomenclature:

class SteadySolver(System):

    def __init__(self, name: str="Steady State System", ref_T: UnitValue=UnitValue("METRIC", "TEMPERATURE", "K", 293.15), ref_p: UnitValue=UnitValue("METRIC", "PRESSURE", "Pa", 1.01e5)):
        super().__init__(name, ref_T, ref_p)

    def __repr__(self):
        return str(self.objects)

    def output(self, verbose: bool=True):
        output_string = ""
        items = ["name", "rho", "u", "p", "T", "mdot", "area", "fluid"]
        for item in items:
            output_string += item[:15] + " "*max(16-len(item), 23)
        output_string += "\n"
        for obj in self.objects:
            output_string += str(obj) + " "*2
            for item in items:
                try:
                    val = getattr(obj.state, item)
                except:
                    val = None
                if val == None:
                    val_string = " "
                elif type(val) == str:
                    val_string = val
                else:
                    val_string = str(val)
                output_string += val_string + " "*max(16-len(val_string), 2)
            output_string += "\n"
        if verbose: print("\n\n", output_string, "\n\n", sep='')
        return output_string

    def show_tree(self):
        for i in range(len(self.objects)-1):
            print(self.objects[i].name)
            print(' | ')
        print(self.objects[-1].name)
        print()

    def initialize(self, components: list):
        # Sytem Vlaidation Checks
        if len(components) < 1:
            raise IndexError('No component found. ')
        if components[0].BC_type != "PRESSURE":
            for component in components:
                if component.decoupler == True:
                    raise TypeError("Using a decoupled system wihtout defining the upstrem pressure. ")

        self.components = components
        self.objects = []
        for component in components[:-1]:
                self.objects += [component, component.interface_out]
        self.objects.append(components[-1])
        self.inlet_BC = components[0].BC_type
        self.outlet_BC = components[-1].BC_type
        for component in components:
            component.initialize()

    def update_w(self):
        self.w = []
        for obj in self.objects:
            if obj.type == 'interface':
                self.w += [obj.state.rho.value, obj.state.u.value, obj.state.p.value]
        return self.w

    def set_w(self, new_w):
        i = 0
        for obj in self.objects:
            if obj.type == 'interface':
                obj.state.set(rho=UnitValue("METRIC", "DENSITY", "kg/m^3", new_w[i]), u=UnitValue("METRIC", "VELOCITY", "m/s", new_w[i+1]), p=UnitValue("METRIC", "PRESSURE", "kg/ms^2", new_w[i+2]))
                obj.update()
                i += 3
        self.update_w()


    def solve(self, verbose: bool=True, queue=None):
        self.update_w()
        def func(x):
            self.set_w(x)
            res = []
            for component in self.components:
                component.update()
                res += component.eval()
            if verbose is True:
                print("Residual = "+str(rms(res)))
            if queue is not None:
                queue.put(rms(res))
            return res

        sol = root(func, self.w).x
        if verbose is True:
            print(sol)
        