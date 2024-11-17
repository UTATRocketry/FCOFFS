from FCOFFS.utilities.units import *
#from FCOFFS.utilities.units import *
from FCOFFS.components import *
from FCOFFS.interfaces.interface import *
from FCOFFS.systems.steady import *



PS = SteadySolver(ref_p=UnitValue("IMPERIAL", "PRESSURE", "psig", 0)) 

#can be dynamically initialized now
interface1 = Interface("INTER1")
interface2 = Interface("INTER2")

inlet = pressure_inlet.PressureInlet(PS, UnitValue.create_unit("in", 0.25), "N2", UnitValue.create_unit("psig", 850), UnitValue.create_unit("K", 250), UnitValue.create_unit("m/s", 4), "pressure_inlet")
#p = pipe.Pipe(PS, UnitValue.create_unit('in', 0.25), "N2", UnitValue.create_unit('in', 25))
orifice = critical_orifice.CriticalOrifice(PS, UnitValue.create_unit("in",0.25), UnitValue.create_unit("in", 0.25), UnitValue.create_unit("mm", 0.2312), "N2", Cd=0.86)
outlet = pressure_outlet.PressureOutlet(PS, UnitValue.create_unit("in",0.25), "N2", UnitValue.create_unit("psig", 0), "pressure_outlet")

inlet.set_connection(downstream=interface1)
#p.set_connection(interface1, interface2)
orifice.set_connection(interface1, interface2)
outlet.set_connection(upstream=interface2)

'''
 inter_face
'''

PS.initialize([inlet,orifice,outlet])

PS.solve()
