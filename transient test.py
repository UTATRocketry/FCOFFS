from FCOFFS.utilities.units import *

from FCOFFS.components import *
from FCOFFS.interfaces.interface import *
from FCOFFS.systems.transient import *

TS = TransientSolver(ref_p=UnitValue("IMPERIAL", "PRESSURE", "psi", 15)) 

#can be dynamically initialized now
interface1 = Interface("INTER1")
interface2 = Interface("INTER2")
interface3 = Interface("INTER3")
interface4 = Interface("INTER4")

pressure_tank.PressurantTank(TS.quasi_steady_solver, UnitValue("IMPERIAL", "DISTANCE", "in", 0.8), 'N2', UnitValue("IMPERIAL", "PRESSURE", "psi", 1000), UnitValue("METRIC", "TEMPERATURE", "K", 280), UnitValue("METRIC", "VOLUME", "m^3", 0.5))
critical_orifice.CriticalOrifice(TS.quasi_steady_solver, UnitValue("IMPERIAL", "DISTANCE", "in", 0.8), UnitValue("IMPERIAL", "DISTANCE", "in", 0.8), UnitValue("IMPERIAL", "DISTANCE", "in", 0.2), "N2")
