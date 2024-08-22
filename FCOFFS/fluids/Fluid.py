'''
Description
'''

from CoolProp.CoolProp import PropsSI
from ..utilities.units import UnitValue

class Fluid:
    supported_fluids = {"N2", "N2O", "C2H6O"} # why is this here

    # density [kg/m3]
    # dynamic_viscosity [Pa-s]
    def density(fluid: str, T: UnitValue, p: UnitValue) -> UnitValue:
        dens = PropsSI('D', 'T', T.value, 'P', p.value, fluid)
        return UnitValue("METRIC", "DENSITY", "kg/m^3", dens)

    def temp(fluid: str, rho: UnitValue, p: UnitValue) -> UnitValue:
        t = PropsSI('T', 'D', rho.value, 'P', p.value, fluid)
        return UnitValue("METRIC", "TEMPERATURE", "K", t)

    def pressure(fluid: str, rho: UnitValue, T: UnitValue) -> UnitValue:
        p = PropsSI('P', 'D', rho.value, 'T', T.value, fluid)
        return UnitValue("METRIC", "PRESSURE", "kg/ms^2", p)

    def dynamic_viscosity(fluid: str, rho: UnitValue=None, T: UnitValue=None, p: UnitValue=None) -> UnitValue: # Eventuatly we want to calculate this 
        if fluid=="N2O":
            return UnitValue("METRIC", "DYNAMIC VISCOCITY", "kg/ms", 0.0000552)
        elif fluid=="C2H6O":
            return UnitValue("METRIC", "DYNAMIC VISCOCITY", "kg/ms", 0.001198)
        else:
            raise Exception("Fluid " + fluid + " not supported")

    def kinematic_viscosity(fluid: str, rho: UnitValue|None=None, T: UnitValue=None, p: UnitValue=None) -> UnitValue:
        if rho == None:
            rho = Fluid.density(fluid, T, p)
        return Fluid.dynamic_viscosity(fluid, rho, T, p) / rho