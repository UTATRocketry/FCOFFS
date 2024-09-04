from FCOFFS.utilities.units import *
#from FCOFFS.utilities.units import *
from FCOFFS.components import *
from FCOFFS.interfaces.interface import *
from FCOFFS.pressureSystem.PressureSystem import *

import os



PS = PressureSystem(ref_p=UnitValue("IMPERIAL", "PRESSURE", "psi", 15)) 

#can be dynamically initialized now
interface1 = Interface("INTER1")
interface2 = Interface("INTER2")

inlet = pressure_inlet.PressureInlet(PS, UnitValue.create_unit("in", 0.25), "N2", UnitValue.create_unit("psi", 1000), UnitValue.create_unit("K", 295.7), "pressure_inlet")
regulator = pressure_regulator.PressureRegulator(PS,  UnitValue.create_unit("in",0.25), "N2", os.path.join(os.getcwd(), "FCOFFS", "utilities", "test.csv"), UnitValue.create_unit("psi", 20))
outlet = pressure_outlet.PressureOutlet(PS, UnitValue.create_unit("in",0.25), "N2", UnitValue.create_unit("psi", 17), "pressure_outlet")

inlet.set_connection(downstream=interface1)
regulator.set_connection(interface1, interface2)
outlet.set_connection(upstream=interface2)

'''
 inter_face
'''

PS.initialize([inlet,regulator,outlet])
PS.show_tree()
PS.output()
PS.solve()
PS.output()