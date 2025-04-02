from FCOFFS.utilities.units import *
from FCOFFS.components import *
from FCOFFS.interfaces.interface import *
from FCOFFS.systems.transient import *

SS = SteadySolver(ref_p=UnitValue.create_unit("psig", 0), ref_T=UnitValue.create_unit("C", 0))

interface1 = Interface("INTER1")
interface2 = Interface("INTER2")
interface3 = Interface("INTER3")
interface4 = Interface("INTER4")


inlet = pressure_inlet.PressureInlet(SS, UnitValue.create_unit("in", 0.25), "N2", UnitValue.create_unit("psi", 500), UnitValue.create_unit("K", 295), UnitValue.create_unit("m/s", 50))
p1 = pipe.Pipe(SS, UnitValue.create_unit("in", 0.25), "N2", UnitValue.create_unit("m", 0.25))
#b1 = bend.Bend(SS, UnitValue.create_unit("in", 0.25), UnitValue.create_unit("in", 5), "C2H6O", UnitValue.create_unit("in", 12))
#p2 = pipe.Pipe(SS, UnitValue.create_unit("in", 0.25), "C2H6O", UnitValue.create_unit("in", 15))
outlet = pressure_outlet.PressureOutlet(SS, UnitValue.create_unit("in", 0.25), "N2", UnitValue.create_unit("kg/ms^2", 1564298.8749036463))
# outlet = mass_flow_outlet.MassFlowOutlet(SS, UnitValue.create_unit("in", 0.25), "N2", UnitValue.create_unit("kg/s", 0.25))

#unit = UnitValue.create_unit("kg/ms^2", 1564298.8749036463)

inlet.set_connection(downstream=interface1)
p1.set_connection(interface1, interface2)
#b1.set_connection(interface1, interface2)
# p2.set_connection(interface3, interface4)
outlet.set_connection(upstream=interface2)


SS.Output.toggle_steady_state_output()
SS.initialize([inlet, p1, outlet])
#SS.Output.set_ouput_unit("psi")



SS.solve()

















