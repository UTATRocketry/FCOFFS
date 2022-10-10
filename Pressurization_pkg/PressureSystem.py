from Pressurization_pkg.Node import Node
from Pressurization_pkg.componentClass import *

class PressureSystem:

    def __init__(self, source, components):
        self.source = source
        self.components = components
        if len(components) < 1:
            raise IndexError('No component found. ')
        self._connect()
        self._update()

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

    def _update(self):
        for component in self.components:
            component._compute()
            component._update()

        self.outlet_P = self.components[-1].outlet.P
        self.total_dP = self.source.outlet.P - self.outlet_P

    def show(self):
        print(self.source.outlet.P)
        for component in self.components:
            print(' | ',component.name)
            print(component.outlet.P)