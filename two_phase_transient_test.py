
import os

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

inlet = pressure_tank_inlet.PressurantTank(TS.quasi_steady_solver, UnitValue.create_unit("inch", 0.25), "N2", UnitValue.create_unit("psi", 950), UnitValue.create_unit("C", 20), UnitValue.create_unit("m^3", 0.002408554367752175), UnitValue.create_unit("m/s", 10))
# p = pipe.Pipe(TS.quasi_steady_solver, UnitValue.create_unit("in", 0.25), "N2", UnitValue.create_unit("m", 1.5)) 
tp_tank = two_phase_tank.TwoPhaseTank(TS.quasi_steady_solver, UnitValue.create_unit("inch", 0.25), UnitValue.create_unit("inch", 0.25), "N2", "C2H6O", UnitValue.create_unit("kg", 1.8), UnitValue.create_unit("C", 20), UnitValue.create_unit("m", 0.05), UnitValue.create_unit("m", 0.24))
p2 = pipe.Pipe(TS.quasi_steady_solver, UnitValue.create_unit("in", 0.25), "C2H6O", UnitValue.create_unit("m", 0.4))
venturri = cavitating_venturi.CavitatingVenturi(TS.quasi_steady_solver,  UnitValue.create_unit("in", 0.25), UnitValue.create_unit("in", 0.25), UnitValue.create_unit("in", 0.096), "C2H6O", 0.95)
p3 = pipe.Pipe(TS.quasi_steady_solver, UnitValue.create_unit("in", 0.25), "C2H6O", UnitValue.create_unit("m", 0.4))
out = pressure_outlet.PressureOutlet(TS.quasi_steady_solver, UnitValue.create_unit("in", 0.25), "C2H6O", UnitValue.create_unit("psi", 500))

reg = pressure_regulator.PressureRegulator(TS.quasi_steady_solver, UnitValue.create_unit("in", 0.25), "N2", os.path.join(os.getcwd(), "DOCS", "Components", "Pressure Regulator", "Regulator Curves", "KPF.csv"), UnitValue.create_unit("psi", 800))


inlet.set_connection(downstream=interface1)
# p.set_connection(interface1, interface2)
tp_tank.set_connection(interface1, interface2)
p2.set_connection(interface2, interface3)
venturri.set_connection(interface3, interface4)
p3.set_connection(interface4, interface5)
out.set_connection(upstream=interface5)

TS.initialize([inlet, tp_tank, p2, venturri ,p3, out])

#SS.Output.show_tree()
TS.Output.add_probes([(inlet, "p"), (tp_tank, "liquid_height"), (interface2, "mdot"), (tp_tank, "liquid_mass")])
TS.Output.toggle_steady_state_output()
TS.Output.toggle_convergence_output()
TS.Output.set_ouput_unit("psi")
#TS.Output.show_config()
TS.solve(5.85, 0.05)                                                                                                               

