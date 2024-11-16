import os

from FCOFFS.utilities.units import *
from FCOFFS.components import *
from FCOFFS.interfaces.interface import *
from FCOFFS.systems.steady import *


PS = SteadySolver(ref_p=UnitValue("IMPERIAL", "PRESSURE", "psi", 15)) 

#can be dynamically initialized now
interface1 = Interface("INTER1")
interface2 = Interface("INTER2")

# note initial velocity guess really matters for pressure regulator convergence!!!!!
inlet = pressure_inlet.PressureInlet(PS, UnitValue.create_unit("in", 0.25), "N2", UnitValue.create_unit("psi", 1000), UnitValue.create_unit("K", 295.7), UnitValue.create_unit("m/s", 5), "pressure_inlet")
regulator = pressure_regulator.PressureRegulator(PS,  UnitValue.create_unit("in",0.25), "N2", os.path.join(os.getcwd(), "DOCS", "Components", "Pressure Regulator", "Regulator Curves", "KPF.csv"), UnitValue.create_unit("psi", 600))
outlet = pressure_outlet.PressureOutlet(PS, UnitValue.create_unit("in",0.25), "N2", UnitValue.create_unit("psi", 550), "pressure_outlet")

inlet.set_connection(downstream=interface1)
regulator.set_connection(interface1, interface2)
outlet.set_connection(upstream=interface2)

'''
 inter_face
'''

PS.initialize([inlet,regulator,outlet])

PS.Output

PS.solve()