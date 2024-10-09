from FCOFFS.utilities.units import *
#from FCOFFS.utilities.units import *
from FCOFFS.components import *
from FCOFFS.interfaces.interface import *
from FCOFFS.systems.steady import *



PS = SteadySolver(ref_p=UnitValue("IMPERIAL", "PRESSURE", "psi", 15)) 

#can be dynamically initialized now
interface1 = Interface("INTER1")
interface2 = Interface("INTER2")

inlet = pressure_inlet.PressureInlet(PS, UnitValue.create_unit("in", 0.8), "CO2", UnitValue.create_unit("psi", 314.7), UnitValue.create_unit("K", 236.7), "pressure_inlet")
orifice = critical_orifice.CriticalOrifice(PS, UnitValue.create_unit("in",0.8), UnitValue.create_unit("in",0.8), "CO2", Cd=0.86)
outlet = pressure_outlet.PressureOutlet(PS, UnitValue.create_unit("in",0.8), "CO2", UnitValue.create_unit("psi", 14.7), "pressure_outlet")

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