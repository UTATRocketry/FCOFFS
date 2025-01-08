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
interface6 = Interface("INTER6")

inlet = pressure_tank_inlet.PressurantTank(TS.quasi_steady_solver, UnitValue.create_unit("inch", 0.25), "N2", UnitValue.create_unit("psi", 950), UnitValue.create_unit("C", 20), UnitValue.create_unit("m^3", 0.1), UnitValue.create_unit("m/s", 10))
p = pipe.Pipe(TS.quasi_steady_solver, UnitValue.create_unit("in", 0.25), "N2", UnitValue.create_unit("m", 1.5)) 
tp_tank = two_phase_tank.TwoPhaseTank(TS.quasi_steady_solver, UnitValue.create_unit("inch", 0.25), UnitValue.create_unit("inch", 0.25), "N2", "C2H6O", UnitValue.create_unit("kg", 15), UnitValue.create_unit("C", 20), UnitValue.create_unit("m", 0.1), UnitValue.create_unit("m", 0.5))
p2 = pipe.Pipe(TS.quasi_steady_solver, UnitValue.create_unit("in", 0.25), "C2H6O", UnitValue.create_unit("m", 0.4))
venturri = cavitating_venturi.CavitatingVenturi(TS.quasi_steady_solver,  UnitValue.create_unit("in", 0.25), UnitValue.create_unit("in", 0.25), UnitValue.create_unit("in", 0.096), "C2H6O", 0.95)
p3 = pipe.Pipe(TS.quasi_steady_solver, UnitValue.create_unit("in", 0.25), "C2H6O", UnitValue.create_unit("m", 0.4))
out = pressure_outlet.PressureOutlet(TS.quasi_steady_solver, UnitValue.create_unit("in", 0.25), "C2H6O", UnitValue.create_unit("psi", 500))


inlet.set_connection(downstream=interface1)
p.set_connection(interface1, interface2)
tp_tank.set_connection(interface2, interface3)
p2.set_connection(interface3, interface4)
venturri.set_connection(interface4, interface5)
p3.set_connection(interface5, interface6)
out.set_connection(upstream=interface6)

TS.initialize([inlet, p, tp_tank, p2, venturri ,p3, out])

#SS.Output.show_tree()
TS.Output.add_probes([(inlet, "p"), (interface4, "p"), (interface5, "p"), (tp_tank, "liquid_height"), (interface2,"mdot"),(interface3, "mdot")])
TS.Output.toggle_steady_state_output()
TS.Output.toggle_convergence_output()
TS.Output.set_ouput_unit("psi")
#SS.Output.show_config()
TS.solve(0.1, 0.05)                                                                                                               

