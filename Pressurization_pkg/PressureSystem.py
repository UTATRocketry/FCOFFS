from Pressurization_pkg.Node import *
from Pressurization_pkg.componentClass import *
from Pressurization_pkg.Utilities import *
from scipy.optimize import newton

# Nomenclature:

class PressureSystem:

    def __init__(self,ref_T=293.15,ref_p=1.01e5):
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
        for component in components:
            component.initialize()

    def solve(self):
        if self.inlet_BC=="PressureInlet" and self.outlet_BC=="MassOutlet":
            # guess variable is inlet velocity; need to match outlet mdot
            x0 = self.objects[-1].state.u
            target = self.objects[-1].state.mdot
            print("x0="+str(x0)+"\ntarget="+str(target))
            def func(x):
                self.objects[0].state.set(u=x)
                for component in self.components:
                    component.update()
                print("Residual = "+str(abs(self.objects[-1].state.mdot - target)/target))
                return self.objects[-1].state.mdot - target
            newton(func,x0,full_output=True)


    # def _connect(self):
    #     if self.components[0].name == None:
    #         self.components[0].name = 'COMP0'
    #     for indx in range(1,len(self.components)):
    #         if self.components[indx].name == None:
    #             self.components[indx].name = 'COMP' + str(indx)
    #         if self.components[indx-1].type == 'node':
    #             self.nodes.append(self.components[indx-1])
    #             self.components[indx-1]._connect_downstream(self.components[indx])
    #             self.components[indx]._connect_upstream(self.components[indx-1])
    #         elif self.components[indx].type == 'node':
    #             self.nodes.append(self.components[indx])
    #             self.components[indx-1]._connect_downstream(self.components[indx])
    #             self.components[indx]._connect_upstream(self.components[indx-1])
    #         else:
    #             node = Node(self.components[indx-1],self.components[indx],name='NODE' + str(indx))
    #             self.nodes.append(node)
    #             self.components[indx-1]._connect_downstream(node)
    #             self.components[indx]._connect_upstream(node)
    #
    #     head = self.components[0]
    #     self.components = [head]
    #     while head.downstream != None:
    #         head = head.downstream
    #         self.components.append(head)
    #
    #     for item in self.components:
    #         item.parent_system = self
    #         item.initialize()
    #
    #     return self
    #
    # def _time_march(self):
    #     pass
    #
    #
    # def execute(self,t_max,dt):
    #     self.t = 0
    #     self.t_max = time
    #     self.dt = dt
    #
    #
    # def _update(self):
    #     self.source._update_fluid(self.fluid)
    #     self.source._update()
    #     for component in self.components:
    #         component._update_fluid(self.fluid)
    #         component._update()
    #     return self
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