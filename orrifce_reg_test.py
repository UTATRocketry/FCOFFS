from FCOFFS.utilities.units import *
#from FCOFFS.utilities.units import *
from FCOFFS.components import *
from FCOFFS.interfaces.interface import *
from FCOFFS.systems.steady import *
from FCOFFS.systems.transient import *

SS = SteadySolver(ref_p=UnitValue("IMPERIAL", "PRESSURE", "psig", 0))

interface1 = Interface("INTER1")
interface2 = Interface("INTER2")

inlet = pressure_inlet.PressureInlet(SS, UnitValue.create_unit("in",0.152), "N2", UnitValue.create_unit("psi", 800), UnitValue.create_unit("C", -5), UnitValue.create_unit("m/s", 20))
orifice = critical_orifice.CriticalOrifice(SS, UnitValue.create_unit("in",0.152), UnitValue.create_unit("in", 0.152), UnitValue.create_unit("in", 0.062), "N2", Cd=0.86)
outlet = pressure_outlet.PressureOutlet(SS, UnitValue.create_unit("in", 0.152), "N2", UnitValue.create_unit("psi", 14.6))
#outlet = mass_flow_outlet.MassFlowOutlet(SS, UnitValue.create_unit("in", 0.152), "N2", UnitValue.create_unit("kg/s", 0.068326221))

inlet.set_connection(downstream=interface1)
#p.set_connection(interface1, interface2)
orifice.set_connection(interface1, interface2)
#p2.set_connection(interface3, interface4)
outlet.set_connection(upstream=interface2)

SS.initialize([inlet, orifice, outlet])
SS.Output.toggle_steady_state_output()
SS.solve()
flow = interface1.state.mdot/interface1.state.rho
slpm = flow.SLPM(interface1.state.T, interface1.state.p)
print(flow, slpm, slpm.value/28.31, "SCFM")