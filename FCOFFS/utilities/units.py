'''
Description
'''

from enum import Enum


class UnitPressure(Enum):
    Pa = 1
    psi = 6894.76


class UnitLength(Enum):
    m = 1
    inch = 0.0254


def convert_to_si(quantity):
    if not isinstance(quantity, tuple):
        return quantity
    return quantity[0] * quantity[1].value


def convert_from_si(quantity):
    if not isinstance(quantity, tuple):
        return quantity
    return quantity[0] / quantity[1].value