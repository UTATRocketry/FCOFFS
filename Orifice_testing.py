from FCOFFS.utilities.units import *
#from FCOFFS.utilities.units import *
from FCOFFS.components import *
from FCOFFS.interfaces.interface import *
from FCOFFS.systems.steady import *



PS = SteadySolver(ref_p=UnitValue("IMPERIAL", "PRESSURE", "psi", 15)) 

#can be dynamically initialized now
interface1 = Interface("INTER1")
interface2 = Interface("INTER2")

inlet = pressure_inlet.PressureInlet(PS, UnitValue.create_unit("in", 0.8), "N2", UnitValue.create_unit("psi", 1000), UnitValue.create_unit("K", 290.7), "pressure_inlet")
orifice = critical_orifice.CriticalOrifice(PS, UnitValue.create_unit("in",0.8), UnitValue.create_unit("in",0.8), UnitValue.create_unit("in",0.2), "N2", Cd=0.86)
outlet = pressure_outlet.PressureOutlet(PS, UnitValue.create_unit("in",0.8), "N2", UnitValue.create_unit("psi", 15.7), "pressure_outlet")

inlet.set_connection(downstream=interface1)
orifice.set_connection(interface1, interface2)
outlet.set_connection(upstream=interface2)

'''
 inter_face
'''

PS.initialize([inlet,orifice,outlet])
PS.show_tree()
PS.output()
PS.solve()
PS.output()