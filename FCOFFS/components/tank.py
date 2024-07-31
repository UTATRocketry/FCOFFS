'''
Description
'''

from ..components.componentClass import ComponentClass
from ..pressureSystem import PressureSystem
from ..fluids.fluid import Fluid
from ..utilities.units import *

class Tank(ComponentClass):
    def __init__(self, parent_system: PressureSystem, diameter: UnitValue, fluid: str, volume: UnitValue, name: str="Tank"):
      
        super().__init__(parent_system, diameter, fluid, name)
        self.volume = volume
        self.volume.convert_base_metric() 
        self.fluid_level = 0  
        self.pressure = None  
        self.temperature = None  

    def __str__(self):
        
        return f"{self.name}: Volume={self.volume} m^3, Fluid Level={self.fluid_level} m^3"

    def add_fluid(self, volume):
        
        self.fluid_level += volume
        if self.fluid_level > self.volume.value: # why not just stop users from adding over instead of doing it and throwing error?
            raise ValueError("Fluid level exceeds tank capacity")

    def remove_fluid(self, volume):

        self.fluid_level -= volume 
        if self.fluid_level < 0: #  same here why not just stop users from removing more instead of doing it and throwing error?
            raise ValueError("Cannot remove more fluid than the current level")

    def update_properties(self):
        # Update tank properties based on current state
        pass

    def initialize(self):
        # Initialize tank properties
        super().initialize() 
        # Additional initialization specific to the tank
        self.update_properties()

    def update(self):
        # Update method to adjust tank state and potentially connected nodes
        super().update()
        self.update_properties()
        return []


