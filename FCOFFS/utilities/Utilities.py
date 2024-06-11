'''
Description
'''

from CoolProp.CoolProp import PropsSI
import numpy as np
from enum import Enum


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
    


class UnitPressure(Enum):
    Pa = 1
    psi = 6894.76


class UnitLength(Enum):
    m = 1
    inch = 0.0254


def convert_to_si(quantity):
    # Quantity: value or (value, unit)
    # Returns value in SI units

    if not isinstance(quantity, tuple):
        return quantity
    return quantity[0] * quantity[1].value


def convert_from_si(quantity):
    if not isinstance(quantity, tuple):
        return quantity
    return quantity[0] / quantity[1].value
    

def rms(arr):
    sum = 0
    for num in arr:
        sum += num**2
    sum /= len(arr)
    return np.sqrt(sum)