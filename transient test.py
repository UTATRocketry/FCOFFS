from FCOFFS.utilities.units import *

from FCOFFS.components import *
from FCOFFS.interfaces.interface import *
from FCOFFS.systems.transient import *

TS = TransientSolver(ref_p=UnitValue("IMPERIAL", "PRESSURE", "psi", 15)) 


interface1 = Interface("INTER1")
interface2 = Interface("INTER2")

tank = pressure_tank.PressurantTank(TS.quasi_steady_solver, UnitValue("IMPERIAL", "DISTANCE", "in", 0.8), 'N2', UnitValue("IMPERIAL", "PRESSURE", "psi", 20), UnitValue("METRIC", "TEMPERATURE", "K", 280), UnitValue("METRIC", "VOLUME", "m^3", 0.6))
p = pipe.Pipe(TS.quasi_steady_solver, UnitValue("IMPERIAL", "DISTANCE", "in", 0.8), "N2", UnitValue("IMPERIAL", "DISTANCE", "in", 5), name="Pipe 1")
#orifice = critical_orifice.CriticalOrifice(TS.quasi_steady_solver, UnitValue("IMPERIAL", "DISTANCE", "in", 0.8), UnitValue("IMPERIAL", "DISTANCE", "in", 0.8), "N2")
out = pressure_outlet.PressureOutlet(TS.quasi_steady_solver, UnitValue("IMPERIAL", "DISTANCE", "in", 0.8), "N2", UnitValue("IMPERIAL", "PRESSURE", "psi", 16))

tank.set_connection(downstream=interface1)
p.set_connection(interface1, interface2)
#orifice.set_connection(interface1, interface2)
out.set_connection(upstream=interface2)

TS.initialize([tank, p, out], 10)
TS.solve()


