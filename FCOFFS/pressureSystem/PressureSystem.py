'''
Description
'''

from scipy.optimize import root
import warnings

from ..interfaces.interface import *
from ..utilities.Utilities import *
from ..utilities.units import UnitValue


# Nomenclature:

class PressureSystem:

    def __init__(self, name: str="Pressure System", ref_T: UnitValue=UnitValue("METRIC", "TEMPERATURE", "k", 293.15), ref_p: UnitValue=UnitValue("METRIC", "PRESSURE", "Pa", 1.01e5), transient=[0,0,0]):
        self.name = name
        self.w = []            # list of primitives on the nodes
        self.ref_T = ref_T
        self.ref_p = ref_p
        self.ref_p.convert_base_metric()
        self.transient = transient   # [t_i, t_f, dt]
        self.t = transient[0]
        self.components = []


    def __repr__(self):
        return str(self.objects)

    def output(self, verbose: bool=True):
        output_string = ""
        items = ["name", "rho", "u", "p"]
        for item in items:
            output_string += item[:15] + " "*max(16-len(item), 1)
        output_string += "\n"
        for obj in self.objects:
            for item in items:
                try:
                    val = getattr(obj, item)
                except:
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
                output_string += val_string + " "*max(16-len(val_string), 1)
            output_string += "\n"
        if verbose: print("\n\n", output_string, "\n\n", sep='')
        return output_string

    def show_tree(self):
        for i in range(len(self.objects)-1):
            print(self.objects[i].name)
            print(' | ')
        print(self.objects[-1].name)
        print()

    def initialize(self, components: list, inlet_BC: str, outlet_BC: str):
        if len(components) < 1:
            raise IndexError('No component found. ')
        self.components = components
        self.objects = [components[0].interface_in]
        for component in components:
            self.objects += [component, component.interface_out]
        self.inlet_BC = inlet_BC
        self.outlet_BC = outlet_BC
        if self.objects[0].BC_type != inlet_BC or self.objects[-1].BC_type != outlet_BC:
            warnings.warn("Boundary Condition setting mismatch")
        for component in components:
            component.initialize()

    def update_w(self):
        self.w = []
        if self.inlet_BC=="PressureInlet" and self.outlet_BC=="PressureOutlet":
            var1 = self.objects[0].state.u.value
            var2 = self.objects[-1].state.rho.value
            var3 = self.objects[-1].state.u.value
            self.w = [var1]
            for obj in self.objects[1:-1]:
                if obj.type == 'interface':
                    self.w += [obj.state.rho.value, obj.state.u.value, obj.state.p.value]
            self.w += [var2,var3]
        return self.w

    def set_w(self, new_w):
        i = 0
        if self.inlet_BC=="PressureInlet" and self.outlet_BC=="PressureOutlet":
            var1 = new_w[i]
            i += 1
            self.objects[0].state.u =  UnitValue("METRIC", "VELOCITY", "m/s", var1)
            self.objects[0].update()
            for obj in self.objects[1:-1]:
                if obj.type == 'interface':
                    obj.state.set(rho=UnitValue("METRIC", "DENSITY", "kg/m^3", new_w[i]), u=UnitValue("METRIC", "VELOCITY", "m/s", new_w[i+1]), p=UnitValue("METRIC", "PRESSURE", "kg/ms^2", new_w[i+2]))
                    obj.update()
                    i += 3
            var2 = new_w[i]
            var3 = new_w[i+1]
            self.objects[-1].state.rho =  UnitValue("METRIC", "DENSITY", "kg/m^3", var2)
            self.objects[-1].state.u =  UnitValue("METRIC", "VELOCITY", "m/s", var3)
            self.objects[-1].update()
        # if self.inlet_BC=="PressureInlet" and self.outlet_BC=="MassOutlet":
        #     var1 = new_w[i]
        #     i += 1
        #     self.objects[0].state.u =  var1 / self.objects[0].state.rho / self.objects[0].state.area
        #     self.objects[0].update()
        #     for obj in self.objects[1:-1]:
        #         if obj.type == 'node':
        #             obj.state.set(rho=new_w[i], u=new_w[i+1], p=new_w[i+2])
        #             obj.update()
        #             i += 3
        #     var2 = new_w[i]
        #     var3 = new_w[i+1]
        #     self.objects[-1].state.p = var2
        #     self.objects[-1].state.rho =  Fluid.density(self.objects[-1].state.fluid,var3,var2)
        #     self.objects[-1].state.u =  self.objects[-1].state.mdot / self.objects[-1].state.rho / self.objects[-1].state.area
        self.update_w()


    def solve(self):
        while True:
            if self.inlet_BC=="PressureInlet" and self.outlet_BC=="PressureOutlet":
                self.update_w()
                def func(x):
                    #print(x)
                    self.set_w(x)
                    res = []
                    for component in self.components:
                        component.update()
                        res += component.eval()
                    print("Residual = "+str(rms(res)))
                    #print(res)
                    #self.output()
                    return res

            sol = root(func, self.w).x
            print(sol)
            self.t += self.transient[2]
            if self.t > self.transient[1] or self.transient[2] == 0:
                break