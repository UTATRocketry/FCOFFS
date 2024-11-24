from FCOFFS.utilities.units import * 

from FCOFFS.components import *
from FCOFFS.interfaces.interface import *
from FCOFFS.systems.transient import *

SS = SteadySolver(ref_p=UnitValue("IMPERIAL", "PRESSURE", "psig", 600)) 

interface1 = Interface("INTER1")
interface2 = Interface("INTER2")

inlet = mass_flow_inlet.MassFlowInlet(SS, UnitValue.create_unit("in", 0.25), "N2", UnitValue.create_unit("kg/s", 0.01148935361), UnitValue.create_unit("C", 20), UnitValue.create_unit("m/s", 50))
p = pipe.Pipe(SS, UnitValue.create_unit("in", 0.25), "N2", UnitValue.create_unit("ft", 20))
#outlet = mass_flow_outlet.MassFlowOutlet(SS, UnitValue.create_unit("in", 0.25), "N2", UnitValue.create_unit("kg/s", 0.01148935361))
outlet = pressure_outlet.PressureOutlet(SS, UnitValue.create_unit("in", 0.25), "N2", UnitValue.create_unit("psig", 500))


inlet.set_connection(downstream=interface1)
p.set_connection(interface1, interface2)
outlet.set_connection(upstream=interface2)

SS.initialize([inlet, p, outlet])
SS.Output.toggle_steady_state_output()
#TS.Output.show_config()

SS.Output.set_ouput_unit("psi")
SS.Output.add_probes(((interface1, "p"), (interface2, "p")))

SS.solve()                       