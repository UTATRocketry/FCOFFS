
from FCOFFS.utilities.units import *
#from FCOFFS.utilities.units import * # .. \
from FCOFFS.components import * 
from FCOFFS.interfaces.interface import *
from FCOFFS.systems.steady import *


BendSystem = SteadySolver(ref_p=UnitValue("IMPERIAL", "PRESSURE", "psi", 15)) 

#can be dynamically initialized now
interface1 = Interface("INTER1")
interface2 = Interface("INTER2")
interface3 = Interface("INTER3")
# interface4 = Interface("INTER4")

fluid = "N2O"

inlet = pressure_inlet.PressureInlet(BendSystem, UnitValue.create_unit("in", 0.25), fluid, UnitValue.create_unit("psi", 800), UnitValue.create_unit("c",25), UnitValue.create_unit("m/s", 0.05), "pressure_inlet")
bend = smooth_bend.SmoothBend(BendSystem, UnitValue.create_unit("in", 0.25), radius_of_curvature=UnitValue.create_unit("in", 10), fluid=fluid)
#p1 = pipe.Pipe(PS, UnitValue.create_unit("in", 0.25), fluid, UnitValue.create_unit("ft", 2))
# venturi = cavitating_venturi.CavitatingVenturi(PS, UnitValue.create_unit("in", 0.25), UnitValue.create_unit("in", 0.25), UnitValue.create_unit("in", 0.01), fluid, 0.95)
# p2 = pipe.Pipe(PS, UnitValue.create_unit("in", 0.25), fluid, UnitValue.create_unit("m", 0.5))
outlet = mass_flow_outlet.MassFlowOutlet(BendSystem, UnitValue.create_unit("in", 0.25), fluid, UnitValue.create_unit("kg/s", 0.012), )
# outlet = pressure_outlet.PressureOutlet(BendSystem, UnitValue.create_unit("in",0.25) , fluid, UnitValue.create_unit("psi", ), "pressure_outlet")

inlet.set_connection(downstream=interface1)
bend.set_connection(interface1, interface2)
# venturi.set_connection(interface2, interface3)
# p2.set_connection(interface3, interface4)
#tube.set_connection(interface2, interface3)
outlet.set_connection(upstream=interface2)

'''
 inter_face
'''

BendSystem.initialize([inlet, bend, outlet])

#BendSystem.Output.show_tree()
BendSystem.Output.toggle_steady_state_output()
BendSystem.Output.set_ouput_unit("Pa")
#BendSystem.Output.toggle_convergence_output()
BendSystem.solve()

