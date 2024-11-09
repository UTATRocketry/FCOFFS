from FCOFFS.utilities.units import *
#from FCOFFS.utilities.units import * # .. \
from FCOFFS.components import * 
from FCOFFS.interfaces.interface import *
from FCOFFS.systems.steady import *


PS = SteadySolver(ref_p=UnitValue("IMPERIAL", "PRESSURE", "psi", 15)) 

#can be dynamically initialized now
interface1 = Interface("INTER1")
interface2 = Interface("INTER2")
interface3 = Interface("INTER3")


inlet = pressure_inlet.PressureInlet(PS, UnitValue.create_unit("in", 0.25), "C2H6O", UnitValue.create_unit("psi", 600), UnitValue.create_unit("c",25), "pressure_inlet")
venturi = cavitating_venturi.CavitatingVenturi(PS, UnitValue.create_unit("in", 0.25), UnitValue.create_unit("in", 0.25), UnitValue.create_unit("in", 0.096), 0.95, "C2H6O")
tube = pipe.Pipe(PS, UnitValue.create_unit("in", 0.25), "C2H6O","tube", UnitValue.create_unit("in", 10))
#injector_manifold = injector.Injector(PS,)
outlet = pressure_outlet.PressureOutlet(PS, UnitValue.create_unit("in",0.25) , "C2H6O", UnitValue.create_unit("psi", 400), "pressure_outlet")

inlet.set_connection(downstream=interface1)
venturi.set_connection(interface1, interface2)
tube.set_connection(interface2, interface3)
outlet.set_connection(upstream=interface3)

'''
 inter_face
'''

PS.initialize([inlet,venturi,tube,outlet])
PS.show_tree()
PS.output()
PS.solve()
PS.output()
