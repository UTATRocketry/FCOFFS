'''
Description
'''

from CoolProp.CoolProp import PropsSI
#from ..utilities.units import UnitValue
from FCOFFS.utilities.units import UnitValue
from scipy.constants import R

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
    
    def Cp(fluid: str, T: UnitValue, p: UnitValue) -> UnitValue:
        cp = PropsSI('C', 'T', T.value, 'P', p.value, fluid)
        return UnitValue("METRIC", "GAS CONSTANTS", "m^2/s^2K", cp)
    
    def Cv(fluid: str, T: UnitValue, p: UnitValue) -> UnitValue:
        cv = PropsSI('O', 'T', T.value, 'P', p.value, fluid)
        return UnitValue("METRIC", "GAS CONSTANTS", "m^2/s^2K", cv)
    
    def local_speed_sound(fluid: str, T: UnitValue, rho: UnitValue) -> UnitValue:
        '''For pure and pseudo-pure fluids, two state variables are required to fix the state. The equations of state are based on T
            and ρ as state variables, so T,ρ will always be the fastest inputs. P,T will be a bit slower (3-10 times), WHATTTTTTTTTTTTT'''
        c_s = PropsSI("A", 'T', T.value , 'D', rho.value, fluid)
        return UnitValue("METRIC", "VELOCITY", "m/s", c_s)

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
    
    def get_gas_constant(fluid: str) -> UnitValue:
        # Gas Constant = Universal Gas Constant / Molecular Weight of Gas
        GasConstant = {"C2H6O": R/50.0 , "N20" : R/44.013 , "N2" : R/28.02 , "H20" : R/18.015}
        return UnitValue.create_unit("m^2/s^2K", GasConstant[fluid])
        
        
    
if __name__ == "__main__":
    UnitValue.create_unit("K", 293.15)
    UnitValue.create_unit("")

