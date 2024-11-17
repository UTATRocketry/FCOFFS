'''
Description
'''

from CoolProp.CoolProp import PropsSI, PhaseSI
#from ..utilities.units import UnitValue
from FCOFFS.utilities.units import UnitValue
from scipy.constants import R


class Fluid:
    supported_fluids = {"N2", "N2O", "C2H6O"} 

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
    
    def phase(fluid: str, T: UnitValue|None = None, p: UnitValue|None = None, rho: UnitValue|None = None) -> str:
        #indexes = {0.0: "liquid", 2.0: "supercritical gas", 5.0: 'gas', 6.0: "mixed (liquid + vapour)", 1.0: "supercritical", 3.0: "supercritical liquid", 4.0: "critical point", 7.0: "unkown phase", 8.0: "not imposed"}
        if T != None and p != None: 
            phase = PhaseSI("P", p.value, "T", T.value, fluid)
        elif T != None and rho != None: 
            phase = PhaseSI("D", rho.value, "T", T.value, fluid)
        elif rho != None and p != None: 
            phase = PhaseSI("P", p.value, "D", rho.value, fluid)
        
        return phase

    def dynamic_viscosity(fluid: str, rho: UnitValue=None, T: UnitValue=None, p: UnitValue=None) -> UnitValue: # Eventuatly we want to calculate this 
        if fluid=="N2O": # get better values
            return UnitValue("METRIC", "DYNAMIC VISCOCITY", "kg/ms", 0.0000552)
        elif fluid=="C2H6O":
            return UnitValue("METRIC", "DYNAMIC VISCOCITY", "kg/ms", 0.001198)
        elif fluid=="N2": 
            return UnitValue("METRIC", "DYNAMIC VISCOCITY", "kg/ms", 0.00001789)
        else:
            raise Exception("Fluid " + fluid + " not supported")

    def kinematic_viscosity(fluid: str, rho: UnitValue|None=None, T: UnitValue=None, p: UnitValue=None) -> UnitValue:
        if rho == None:
            rho = Fluid.density(fluid, T, p)
        return Fluid.dynamic_viscosity(fluid, rho, T, p) / rho
    
    def get_gas_constant(fluid: str) -> UnitValue:
        # Gas Constant = Universal Gas Constant / Molecular Weight of Gas
        GasConstant = {"C2H6O": R/50.0 , "N2O" : R/44.013 , "N2" : R/28.02 , "H2O" : R/18.015, "CO2": R/44}
        return UnitValue.create_unit("m^2/s^2K", GasConstant[fluid])
    
    def get_molecular_mass(fluid: str) -> UnitValue:

        GasConstant = {"C2H6O": 50.0 , "N2O" : 44.013 , "N2" : 28.02 , "H2O" : 18.015, "CO2": 44}
        return UnitValue.create_unit("kg/Mol", GasConstant[fluid])
       
    
if __name__ == "__main__":
    rho = UnitValue.create_unit("kg/m^3", 500)
    p = UnitValue.create_unit("MPa", 4)
    p.convert_base_metric()

    print(Fluid.phase("N2O", rho=rho, p=p))

