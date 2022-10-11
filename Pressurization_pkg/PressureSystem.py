from Pressurization_pkg.Node import Node
from Pressurization_pkg.componentClass import *
from Pressurization_pkg.Utilities import *

fluid_N2O = Fluid(784.94,0.05598)
fluid_C2H6O = Fluid(784.94,0.05598)

# Nomenclature:
# p_t        total pressure [Pa]
# P          static pressure [Pa]
# q          dynamic pressure [Pa]
class PressureSystem:

    def __init__(self, source, components, fluid):
        self.source = source
        self.components = components
        if len(components) < 1:
            raise IndexError('No component found. ')
        if fluid == 'N2O':
            self.fluid = fluid_N2O
        elif fluid == 'C2H6O':
            self.fluid = fluid_C2H6O
        else:
            self.fluid = fluid
        self._connect()._update()

    def _connect(self):
        comp_number = 1
        if self.components[0].name == None:
            self.components[0].name = 'COMP ' + str(comp_number)
            comp_number += 1
        self.components[0]._connect(self.source)
        for indx in range(1,len(self.components)):
            if self.components[indx].name == None:
                self.components[indx].name = 'COMP ' + str(comp_number)
                comp_number += 1
            self.components[indx]._connect(self.components[indx-1])
        return self

    def _update(self):
        self.source._update_fluid(self.fluid)
        self.source._update()
        for component in self.components:
            component._update_fluid(self.fluid)
            component._update()
        return self

    def show(self,pressure_unit='metric'):
        print(' O ',self.source.name)
        if pressure_unit == 'metric':
            print(self.source.outlet.p_upstream,'Pa')
        else:
            print(pa2psi(self.source.outlet.p_upstream),'PSI')
        for component in self.components:
            print(' | ',component.name)
            if pressure_unit == 'metric':
                print(component.outlet.p_upstream,'Pa')
            else:
                print(pa2psi(component.outlet.p_upstream),'PSI')