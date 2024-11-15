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

Nitorgen_Tank = pressure_tank_inlet.PressurantTank(TS.quasi_steady_solver, UnitValue.create_unit("inch", 0.25), "N2", UnitValue.create_unit("psi", 3000), UnitValue.create_unit("C", 20), UnitValue.create_unit("L", 1.5), UnitValue.create_unit("m/s", 5))
regulator = pressure_regulator.PressureRegulator(TS.quasi_steady_solver, UnitValue.create_unit("inch", 0.25), "N2", os.path.join(os.getcwd(), "DOCS", "Components", "Pressure Regulator", "Regulator Curves", "KPF.csv"), UnitValue.create_unit("psi", 800))
orifice = critical_orifice.CriticalOrifice(TS.quasi_steady_solver, UnitValue.create_unit("in",0.25), UnitValue.create_unit("in",0.25), UnitValue.create_unit("in",0.01), "N2", Cd=0.86)
outlet = pressure_outlet.PressureOutlet(TS.quasi_steady_solver, UnitValue.create_unit("in", 0.25), "N2", UnitValue.create_unit("psig", 0))

Nitorgen_Tank.set_connection(downstream=interface1)
regulator.set_connection(interface1, interface2)
orifice.set_connection(interface2, interface3)
outlet.set_connection(upstream=interface3)


TS.initialize([Nitorgen_Tank, regulator, orifice, outlet]) 
TS.Output.add_probes([(Nitorgen_Tank, "mass"), (Nitorgen_Tank, "p"), (Nitorgen_Tank, "rho"), (Nitorgen_Tank, "T")]) 
#TS.Output.mute_steady_state()
TS.solve(1, 0.1)        