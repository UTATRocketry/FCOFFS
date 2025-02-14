from FCOFFS.utilities.units import *
from FCOFFS.components import * 
from FCOFFS.interfaces.interface import *
from FCOFFS.systems.steady import *

interface1 = Interface("INTER1")
interface2 = Interface("INTER2")
interface3 = Interface("INTER3")
interface4 = Interface("INTER4")

SS = SteadySolver(ref_p=UnitValue.create_unit("psi", 700), ref_T=UnitValue.create_unit("C", 20))

pipe_diameter = 0.16
orifice_diameter = 0.03

inlet = pressure_inlet.PressureInlet(SS, UnitValue.create_unit("in", pipe_diameter), "N2", UnitValue.create_unit("psi", 400), UnitValue.create_unit("C", 20), UnitValue.create_unit("m/s", 20))
p = pipe.Pipe(SS, UnitValue.create_unit("in", pipe_diameter), "N2", UnitValue.create_unit("in", 10), roughness=0.015)
orifice = critical_orifice.CriticalOrifice(SS, UnitValue.create_unit("in", pipe_diameter), UnitValue.create_unit("in", pipe_diameter), UnitValue.create_unit("in", orifice_diameter), "N2")
#p2 = pipe.Pipe(SS, UnitValue.create_unit("in", pipe_diameter), "N2", UnitValue.create_unit("in", 10), roughness=0.015)
outlet = pressure_outlet.PressureOutlet(SS, UnitValue.create_unit("in", pipe_diameter), "N2", UnitValue.create_unit("psig", 0))
#outlet = flowrate_outlet.FlowRateOutlet(SS, UnitValue.create_unit("in", 0.18), "N2", UnitValue.create_unit("SCFM", 106.5))

inlet.set_connection(downstream=interface1)
p.set_connection(interface1, interface2)
orifice.set_connection(interface2, interface3)
# p2.set_connection(interface3, interface4)
outlet.set_connection(upstream=interface3)

SS.initialize([inlet, p, orifice, outlet])
SS.Output.set_ouput_unit("psi")
SS.Output.toggle_steady_state_output()
SS.solve()

Re = outlet.interface_in.state.rho*outlet.interface_in.state.u*outlet.diameter/Fluid.dynamic_viscosity("N2", outlet.interface_in.state.rho, outlet.interface_in.state.T, outlet.interface_in.state.p)
flow = outlet.interface_in.state.mdot/outlet.interface_in.state.rho
print("Reynolds Number:", Re)
# print("Outlet Flow Rate:", flow.to("SCFM", temperature=outlet.interface_in.state.T, pressure=outlet.interface_in.state.p))