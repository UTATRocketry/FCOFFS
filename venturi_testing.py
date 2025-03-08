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
interface4 = Interface("INTER4")


inlet = pressure_inlet.PressureInlet(PS, UnitValue.create_unit("in", 0.25), "C2H6O", UnitValue.create_unit("psi", 400), UnitValue.create_unit("c",25), UnitValue.create_unit("m/s", 5), "pressure_inlet")
p = pipe.Pipe(PS, UnitValue.create_unit("in", 0.25), "N2", UnitValue.create_unit("m", 1))
venturi = cavitating_venturi.CavitatingVenturi(PS, UnitValue.create_unit("in", 0.25), UnitValue.create_unit("in", 0.25), UnitValue.create_unit("in", 0.01), "C2H6O", 0.95)
#tube = pipe.Pipe(PS, UnitValue.create_unit("in", 0.25), "C2H6O", UnitValue.create_unit("in", 10))
#injector_manifold = injector.Injector(PS,)
#p2 = pipe.Pipe(PS, UnitValue.create_unit("in", 0.25), "N2", UnitValue.create_unit("m", 0.5))
outlet = pressure_outlet.PressureOutlet(PS, UnitValue.create_unit("in",0.25) , "C2H6O", UnitValue.create_unit("psi", 350), "pressure_outlet")

inlet.set_connection(downstream=interface1)
p.set_connection(interface1, interface2)
venturi.set_connection(interface2, interface3)
#p2.set_connection(interface2, interface3)
#tube.set_connection(interface2, interface3)
outlet.set_connection(upstream=interface3)

'''
 inter_face
'''

PS.initialize([inlet, p, venturi, outlet])

#PS.Output.show_tree()
PS.Output.toggle_steady_state_output()
PS.Output.set_ouput_unit("psi")
#PS.Output.toggle_convergence_output()
PS.solve()

