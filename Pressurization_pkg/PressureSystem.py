from Pressurization_pkg.Node import *
from Pressurization_pkg.componentClass import *
from Pressurization_pkg.Utilities import *
from scipy.optimize import newton,fsolve


# Nomenclature:

class PressureSystem:

    def __init__(self,ref_T=293.15,ref_p=1.01e5):
        self.w = []            # list of primitives on the nodes
        self.ref_T = ref_T
        self.ref_p = ref_p

    def __repr__(self):
        return str(self.objects)

    def output(self):
        print("Name\trho\tu\tp\tmdot")
        for obj in self.objects:
            if obj.type=='node':
                print(obj.name + "\t" + str(obj.state.rho) + "\t" + str(obj.state.u) + "\t" + str(obj.state.p) + "\t" + str(obj.state.mdot))
            else:
                print(obj.name)
        print()

    def show_tree(self):
        for i in range(len(self.objects)-1):
            print(self.objects[i].name)
            print(' | ')
        print(self.objects[-1].name)
        print()

    def initialize(self,components,inlet_BC,outlet_BC):
        if len(components) < 1:
            raise IndexError('No component found. ')
        self.components = components
        self.objects = [components[0].node_in]
        for component in components:
            self.objects += [component,component.node_out]
        self.inlet_BC = inlet_BC
        self.outlet_BC = outlet_BC
        if self.objects[0].BC_type != inlet_BC or self.objects[-1].BC_type != outlet_BC:
            raise Exception("Boundary Condition setting mismatch")
        for component in components:
            component.initialize()

    def update_w(self):
        self.w = []
        for obj in self.objects:
            if obj.type == 'node':
                self.w += [obj.state.rho, obj.state.u, obj.state.p]
        return self.w

    def set_w(self,new_w):
        i = 0
        for obj in self.objects:
            if obj.type == 'node':
                obj.state.set(rho=new_w[i], u=new_w[i+1], p=new_w[i+2])
                obj.update()
                i += 3


    def solve(self):
        if self.inlet_BC=="PressureInlet" and self.outlet_BC=="MassOutlet":
            target_pressure_in = self.objects[0].state.p
            target_temperature_in = self.objects[0].state.T
            target_mass_out = self.objects[-1].state.mdot
            self.update_w()
            def func(x):
                self.set_w(x)
                res = [(self.objects[0].state.p-target_pressure_in)/target_pressure_in,(self.objects[0].state.T-target_temperature_in)/target_temperature_in]
                for component in self.components:
                    res += component.update()
                res += [(self.objects[-1].state.mdot-target_mass_out)/target_mass_out]
                print("Residual = "+str(rms(res)))
                #self.output()
                return res
        # elif self.inlet_BC=="PressureInlet" and self.outlet_BC=="PressureOutlet":
        #     # guess variable is inlet velocity; need to match outlet p
        #     if self.objects[0].state.u != None or self.objects[0].state.u != 0:
        #         x0 = self.objects[0].state.u
        #     else:
        #         x0 = 1
        #     target = self.objects[-1].state.p
        #     print("x0="+str(x0)+"\ntarget="+str(target))
        #     def func(x):
        #         self.objects[0].state.set(u=x)
        #         for component in self.components:
        #             component.update()
        #         print("Residual = "+str(abs(self.objects[-1].state.p - target)/target))
        #         return self.objects[-1].state.p - target
        fsolve(func,self.w)

    #
    # def show(self,pressure_unit='metric'):
    #     print(' O ',self.source.name)
    #     if pressure_unit == 'metric':
    #         print(self.source.outlet.p_upstream,'Pa')
    #     else:
    #         print(pa2psi(self.source.outlet.p_upstream),'PSI')
    #     for component in self.components:
    #         print(' | ',component.name)
    #         if pressure_unit == 'metric':
    #             print(component.outlet.p_upstream,'Pa')
    #         else:
    #             print(pa2psi(component.outlet.p_upstream),'PSI')