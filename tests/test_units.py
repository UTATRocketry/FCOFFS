from FCOFFS.utilities.units import *

def test_moles():
    mol = UnitValue.create_unit("Mol", 5)
    d = UnitValue.create_unit("m", 1)
    assert (mol*d).get_unit == "Molm"
    assert d*mol*d == 5
    