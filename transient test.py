from FCOFFS.utilities.units import *

from FCOFFS.components import *
from FCOFFS.interfaces.interface import *
from FCOFFS.systems.transient import *

TS = TransientSolver(ref_p=UnitValue("IMPERIAL", "PRESSURE", "psi", 15)) 


interface1 = Interface("INTER1")
interface2 = Interface("INTER2")

inlet = mass_flow_inlet.MassFlowInlet(TS.quasi_steady_solver, UnitValue.create_unit("inch", 0.25), "N2", UnitValue.create_unit("kg/s", 0.1), UnitValue.create_unit("C", 20))
chamb = chamber.Chamber(TS.quasi_steady_solver, UnitValue.create_unit("inch", 0.25), "N2", UnitValue.create_unit("psi", 10), UnitValue.create_unit("C", 20), UnitValue.create_unit("m^3", 1))
out = mass_flow_outlet.MassFlowOutlet(TS.quasi_steady_solver, UnitValue.create_unit("inch", 0.25), "N2", UnitValue.create_unit("kg/s", 0.1))


# tank = pressure_tank_inlet.PressurantTank(TS.quasi_steady_solver, UnitValue("IMPERIAL", "DISTANCE", "in", 0.8), 'N2', UnitValue("IMPERIAL", "PRESSURE", "psi", 20), UnitValue("METRIC", "TEMPERATURE", "K", 280), UnitValue("METRIC", "VOLUME", "m^3", 0.6))
# p = pipe.Pipe(TS.quasi_steady_solver, UnitValue("IMPERIAL", "DISTANCE", "in", 0.8), "N2", UnitValue("IMPERIAL", "DISTANCE", "in", 5), name="Pipe 1")
# #orifice = critical_orifice.CriticalOrifice(TS.quasi_steady_solver, UnitValue("IMPERIAL", "DISTANCE", "in", 0.8), UnitValue("IMPERIAL", "DISTANCE", "in", 0.8), "N2")
# out = pressure_outlet.PressureOutlet(TS.quasi_steady_solver, UnitValue("IMPERIAL", "DISTANCE", "in", 0.8), "N2", UnitValue("IMPERIAL", "PRESSURE", "psi", 16))
inlet.set_connection(downstream=interface1)
chamb.set_connection(interface1, interface2)
out.set_connection(upstream=interface2)

TS.initialize([inlet, chamb, out], 1)
TS.solve()


