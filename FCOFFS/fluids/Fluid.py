'''
Description
'''

from CoolProp.CoolProp import PropsSI

class Fluid:
    supported_fluids = {"N2","N2O","C2H6O"}

    # density [kg/m3]
    # dynamic_viscosity [Pa-s]
    def density(fluid,T,p):
        return PropsSI('D', 'T', T, 'P', p, fluid)

    def T(fluid,rho,p):
        return PropsSI('T', 'D',rho, 'P',p, fluid)

    def p(fluid,rho,T):
        return PropsSI('P', 'D',rho, 'T',T, fluid)

    def dynamic_viscosity(fluid,rho=None,T=None,p=None):
        if fluid=="N2O":
            return 0.0000552
        elif fluid=="C2H6O":
            return 0.001198
        else:
            raise Exception("Fluid "+fluid+" not supported")

    def kinematic_viscosity(fluid,rho=None,T=None,p=None):
        if rho == None:
            rho = Fluid.density(fluid,T,p)
        return Fluid.dynamic_viscosity(fluid,rho,T,p) / rho