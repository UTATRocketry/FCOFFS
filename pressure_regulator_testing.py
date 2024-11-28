import os

from FCOFFS.utilities.units import *
from FCOFFS.components import *
from FCOFFS.interfaces.interface import *
from FCOFFS.systems.steady import *
from FCOFFS.systems.transient import *


PS = SteadySolver(ref_p=UnitValue("IMPERIAL", "PRESSURE", "psi", 15))
TS = TransientSolver(ref_p=UnitValue("IMPERIAL", "PRESSURE", "psi", 15)) 

#can be dynamically initialized now
interface1 = Interface("INTER1")
interface2 = Interface("INTER2")
interface3 = Interface("INTER3")
interface4 = Interface("INTER4")
interface5 = Interface("INTER5")
interface6 = Interface("INTER6")
interface7 = Interface("INTER7")

inlet = pressure_tank_inlet.PressurantTank(TS.quasi_steady_solver, UnitValue.create_unit("inch", 0.25), "N2", UnitValue.create_unit("psi", 4000), UnitValue.create_unit("C", 20), UnitValue.create_unit("L", 1.5), UnitValue.create_unit("m/s", 5))
p = pipe.Pipe(TS.quasi_steady_solver, UnitValue.create_unit("in", 0.25), "N2", UnitValue.create_unit("m", 0.3), name="Pipe 1") #3657
regulator = pressure_regulator.PressureRegulator(TS.quasi_steady_solver,  UnitValue.create_unit("in",0.25), "N2", os.path.join(os.getcwd(), "DOCS", "Components", "Pressure Regulator", "Regulator Curves", "KPF.csv"), UnitValue.create_unit("psi", 1000))
p2 = pipe.Pipe(TS.quasi_steady_solver, UnitValue.create_unit("in", 0.25), "N2", UnitValue.create_unit("m", 0.35), name="Pipe 2")
chamb = chamber.Chamber(TS.quasi_steady_solver, UnitValue.create_unit("in",0.25), "N2", UnitValue.create_unit("psi", 830), UnitValue.create_unit("K", 150), UnitValue.create_unit("L", 2))
p3 = pipe.Pipe(TS.quasi_steady_solver, UnitValue.create_unit("in", 0.25), "N2", UnitValue.create_unit("m", 0.15), name="Pipe 3")
orrifice = critical_orifice.CriticalOrifice(TS.quasi_steady_solver, UnitValue.create_unit("in",0.25), UnitValue.create_unit("in",0.25), UnitValue.create_unit("in", 0.01), "N2", Cd=0.86)
outlet = pressure_outlet.PressureOutlet(TS.quasi_steady_solver, UnitValue.create_unit("in",0.25), "N2", UnitValue.create_unit("psi", 10), "pressure_outlet")

inlet.set_connection(downstream=interface1)
p.set_connection(interface1, interface2)
regulator.set_connection(interface2, interface3)
p2.set_connection(interface3, interface4)
chamb.set_connection(interface4, interface5)
p3.set_connection(interface5, interface6)
orrifice.set_connection(interface6, interface7)
outlet.set_connection(upstream=interface7)

TS.initialize([inlet, p, regulator, p2, chamb, p3, orrifice, outlet])

TS.Output.toggle_steady_state_output()
TS.Output.toggle_convergence_output()
TS.Output.add_probes(((interface4, "mdot"), (interface5, "mdot")))
TS.Output.set_ouput_unit("psi")
#TS.Output.show_tree()
TS.Output.toggle_transient_ouput()

TS.solve(15, 0.01)