from FCOFFS.utilities.units import *

from FCOFFS.components import *
from FCOFFS.interfaces.interface import *
from FCOFFS.systems.transient import *

TS = TransientSolver(ref_p=UnitValue("IMPERIAL", "PRESSURE", "psi", 15)) 

interface1 = Interface("INTER1")
interface2 = Interface("INTER2")
interface3 = Interface("INTER3")
interface4 = Interface("INTER4")
interface5 = Interface("INTER5")


inlet = pressure_tank_inlet.PressurantTank(TS.quasi_steady_solver, UnitValue.create_unit("inch", 0.25), "N2", UnitValue.create_unit("psi", 200), UnitValue.create_unit("C", 20), UnitValue.create_unit("m^3", 0.05), UnitValue.create_unit("m/s", 100))
p = pipe.Pipe(TS.quasi_steady_solver, UnitValue.create_unit("in", 0.25), "N2", UnitValue.create_unit("m", 1.5)) 
chamb = chamber.Chamber(TS.quasi_steady_solver, UnitValue.create_unit("inch", 0.25), "N2", UnitValue.create_unit("psi", 150), UnitValue.create_unit("C", 20), UnitValue.create_unit("m^3", 0.05))
p2 = pipe.Pipe(TS.quasi_steady_solver, UnitValue.create_unit("in", 0.25), "N2", UnitValue.create_unit("m", 0.9))
out = pressure_outlet.PressureOutlet(TS.quasi_steady_solver, UnitValue.create_unit("in", 0.25), "N2", UnitValue.create_unit("psi", 100))

orifice = critical_orifice.CriticalOrifice(TS.quasi_steady_solver, UnitValue.create_unit("inch", 0.25), UnitValue.create_unit("inch", 0.25), UnitValue.create_unit("inch", 0.2), "N2")

inlet.set_connection(downstream=interface1)
p.set_connection(interface1, interface2)
chamb.set_connection(interface2, interface3)
p2.set_connection(interface3, interface4)
orifice.set_connection(interface4, interface5)
out.set_connection(upstream=interface5)

TS.initialize([inlet, p, chamb, p2, orifice, out])

TS.Output.show_tree()
TS.Output.add_probes([(inlet, "p"), (interface2, "mdot"), (interface3, "mdot"), (inlet, "mass"), (chamb, "p"), (chamb, "mass")]) #
TS.Output.toggle_steady_state_output()
TS.Output.toggle_convergence_output()
TS.Output.set_ouput_unit("psi")
TS.Output.show_config()
TS.solve(10, 0.5)                                                                                                               



