
from FCOFFS.utilities.units import *
#from FCOFFS.utilities.units import * # .. \
from FCOFFS.components import * 
from FCOFFS.interfaces.interface import *
from FCOFFS.systems.steady import *


BendSystem = SteadySolver(ref_p=UnitValue("IMPERIAL", "PRESSURE", "psi", 500)) 

#can be dynamically initialized now
interface1 = Interface("INTER1")
interface2 = Interface("INTER2")
interface3 = Interface("INTER3")
interface4 = Interface("INTER4")
interface5 = Interface("INTER5")

fluid = "N2"

inlet = pressure_inlet.PressureInlet(BendSystem, UnitValue.create_unit("in", 0.25), fluid, UnitValue.create_unit("psi", 588), UnitValue.create_unit("c",25), UnitValue.create_unit("m/s", 1), "pressure_inlet")
p1 = pipe.Pipe(BendSystem, UnitValue.create_unit("in", 0.25), fluid, UnitValue.create_unit("in",12))
bend = smooth_bend.SmoothBend(BendSystem, UnitValue.create_unit("in", 0.25), radius_of_curvature=UnitValue.create_unit("in", 2), fluid=fluid)
p2 = pipe.Pipe(BendSystem, UnitValue.create_unit("in", 0.25), fluid, UnitValue.create_unit("in", 6))
# bend = smooth_bend.SmoothBend(BendSystem, UnitValue.create_unit("in", 0.25), radius_of_curvature=UnitValue.create_unit("in", 2.5), fluid=fluid)
# orifice = critical_orifice.CriticalOrifice(BendSystem, UnitValue.create_unit("in",0.25), UnitValue.create_unit("in", 0.125), UnitValue.create_unit("in", 0.125), fluid, Cd=0.86)
# p2 = pipe.Pipe(PS, UnitValue.create_unit("in", 0.25), fluid, UnitValue.create_unit("m", 0.5))
outlet = mass_flow_outlet.MassFlowOutlet(BendSystem, UnitValue.create_unit("in", 0.25), fluid, UnitValue.create_unit("kg/s", 0.05))
# outlet = pressure_outlet.PressureOutlet(BendSystem, UnitValue.create_unit("in",0.125) , fluid, UnitValue.create_unit("psi",15), "pressure_outlet")

inlet.set_connection(downstream=interface1)
p1.set_connection(interface1, interface2)
bend.set_connection(interface2, interface3)
p2.set_connection(interface3, interface4)
# orifice.set_connection(interface4, interface5)
#tube.set_connection(interface2, interface3)
outlet.set_connection(upstream=interface4)

'''
 inter_face
'''

BendSystem.initialize([inlet,p1,bend,p2,outlet])

#BendSystem.Output.show_tree()
#BendSystem.Output.toggle_steady_state_output()
BendSystem.Output.set_ouput_unit("psi")
#BendSystem.Output.toggle_convergence_output()
BendSystem.solve()
#interface4.state.mdot.to("SCFM", temperature=interface4.state.T,pressure=interface4.state.p )

