from FCOFFS.utilities.units import *
from FCOFFS.components import * 
from FCOFFS.interfaces.interface import *
from FCOFFS.systems.steady import *

interface1 = Interface("INTER1")
interface2 = Interface("INTER2")

SS = SteadySolver(ref_p=UnitValue.create_unit("psi", 700), ref_T=UnitValue.create_unit("C", 20))

inlet = pressure_inlet.PressureInlet(SS, UnitValue.create_unit("in", 0.25), "N2", UnitValue.create_unit("psi", 800), UnitValue.create_unit("C", 20), UnitValue.create_unit("m/s", 20))
p = pipe.Pipe(SS, UnitValue.create_unit("in", 0.25), "N2", UnitValue.create_unit("m", 0.25,))
outlet = flowrate_outlet.FlowRateOutlet(SS, UnitValue.create_unit("in", 0.25), "N2", UnitValue.create_unit("SCFM", 70))

inlet.set_connection(downstream=interface1)
p.set_connection(interface1, interface2)
outlet.set_connection(upstream=interface2)

SS.initialize([inlet, p, outlet])
SS.Output.set_ouput_unit("psi")
SS.Output.toggle_steady_state_output()
SS.solve()
flow = outlet.interface_in.state.mdot/outlet.interface_in.state.rho
print("Outlet Flow Rate:", flow.to("SCFM", temperature=outlet.interface_in.state.T, pressure=outlet.interface_in.state.p))