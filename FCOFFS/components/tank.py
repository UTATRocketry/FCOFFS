'''
Description
'''
from numpy import pi

from ..components.componentClass import ComponentClass
from ..pressureSystem import PressureSystem
from ..fluids.Fluid import Fluid
from ..utilities.units import *
from ..state.State import *


class TwoPhaseTank(ComponentClass):
    def __init__(self, parent_system: PressureSystem, diameter_in: UnitValue, diameter_out: UnitValue, cross_sectional_diameter: UnitValue, forward_dome_height: UnitValue, aft_dome_height: UnitValue, mid_section_height: UnitValue, liquid_density: UnitValue, fluid: str, mass_of_liquid: UnitValue, name: str="Tank"):

        super().__init__(parent_system, cross_sectional_diameter, fluid, name)
        self.diameter_in = diameter_in
        self.diameter_out = diameter_out
        self.mass_of_liquid = mass_of_liquid
        self.liquid_density = liquid_density
        self.cross_sectional_area =  pi/4 * cross_sectional_diameter**2 

        self.forward_dome_volume = 2/3 * pi * (forward_dome_height)**3 
        self.aft_dome_volume = 2/3 * pi * (aft_dome_height)**3
        self.mid_section_volume = pi * (cross_sectional_diameter/2)**2 * mid_section_height 
        self.volume_of_tank = self.forward_dome_volume + self.aft_dome_volume + self.mid_section_volume
        self.height_of_tank = forward_dome_height + mid_section_height + aft_dome_height
        
        self.volume_liquid = mass_of_liquid / liquid_density 
        
        #calculating remaining fluid height by reverse engineering the remaining fluid volume obtained, in which sectors of the tank
        if self.volume_liquid > (self.mid_section_volume + self.aft_dome_volume):
            self.fluid_height = self.height_of_tank - ( (self.volume_of_tank - self.volume_liquid) / (2/3 * pi) )**(1/3)
            #forward dome contains some fluid 
        
        elif self.volume_liquid > self.aft_dome_volume:
            self.fluid_height = aft_dome_height + (4*(self.volume_liquid - self.aft_dome_volume))/(pi * (cross_sectional_diameter)**2)
            #mid section contains some fluid
        
        elif self.volume_liquid <= self.aft_dome_volume and self.volume_liquid > 0:
            self.fluid_height = (self.volume_liquid/(2/3 * pi))**(1/3)
            #fluid remaining only exists in aft dome section 
        
        elif self.volume_liquid > self.volume_of_tank:
            raise ValueError("Invalid calcultation of remaining fluid volume in tank, revise remaining mass data")
        
        elif self.volume_liquid == self.volume_of_tank:
            self.fluid_height = self.height_of_tank
            
        else:
            raise ValueError("Invalid calcultation of remaining fluid volume in tank, revise remaining mass data")

        
        self.pressure = None  
        self.temperature = None  

    def initialize(self):
        self.interface_in.initialize(parent_system=self.parent_system, area=pi*self.diameter_in**2/4, fluid=self.fluid)
        self.interface_out.initialize(parent_system=self.parent_system, area=pi*self.diameter_out**2/4, fluid=self.fluid, rho=self.interface_in.state.rho, u=self.interface_in.state.u, p=self.interface_in.state.p)

    def eval(self, new_states: tuple[State, State]|None=None) -> list:
        if new_states is None:
            state_in = self.interface_in.state
            state_out = self.interface_out.state
        else:
            state_in = new_states[0]
            state_out = new_states[1]

        res1 = (state_in.mdot / state_in.rho - state_out.mdot / state_out.rho) / 1/2(state_in.mdot / state_in.rho + state_out.mdot / state_out.rho)
        res2 = None
        res3 = None

        return [res1, res2, res3]


    # def __str__(self):

    #     return f"{self.name}: Volume={self.volume} m^3, Fluid Level={self.fluid_level} m^3"

    # def add_fluid(self, volume):

    #     self.fluid_level += volume
    #     if self.fluid_level > self.volume.value: # why not just stop users from adding over instead of doing it and throwing error?
    #         raise ValueError("Fluid level exceeds tank capacity")

    # def remove_fluid(self, volume):

    #     self.fluid_level -= volume 
    #     if self.fluid_level < 0: #  same here why not just stop users from removing more instead of doing it and throwing error?
    #         raise ValueError("Cannot remove more fluid than the current level")

    # def update_properties(self):
    #     # Update tank properties based on current state
    #     pass