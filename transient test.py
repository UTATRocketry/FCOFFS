from FCOFFS.utilities.units import *

from FCOFFS.components import *
from FCOFFS.interfaces.interface import *
from FCOFFS.systems.transient import *

TS = TransientSolver(ref_p=UnitValue("IMPERIAL", "PRESSURE", "psi", 15)) 

interface1 = Interface("INTER1")
interface2 = Interface("INTER2")
interface3 = Interface("INTER3")
interface4 = Interface("INTER4")


#inlet = mass_flow_inlet.MassFlowInlet(TS.quasi_steady_solver, UnitValue.create_unit("inch", 0.25), "N2", UnitValue.create_unit("kg/s", 0.1), UnitValue.create_unit("C", 20))
#inlet = pressure_tank_inlet.PressurantTank(TS.quasi_steady_solver, UnitValue.create_unit("inch", 0.25), "N2", UnitValue.create_unit("psi", 500), UnitValue.create_unit("C", 20), UnitValue.create_unit("m^3", 0.1), UnitValue.create_unit("m/s", 100))
inlet = pressure_inlet.PressureInlet(TS.quasi_steady_solver, UnitValue.create_unit("inch", 0.25), "N2", UnitValue.create_unit("psi", 350), UnitValue.create_unit("C", 20),  UnitValue.create_unit("m/s", 10))
p = pipe.Pipe(TS.quasi_steady_solver, UnitValue.create_unit("in", 0.25), "N2", UnitValue.create_unit("m", 0.75)) 
chamb = chamber.Chamber(TS.quasi_steady_solver, UnitValue.create_unit("inch", 0.25), "N2", UnitValue.create_unit("psi", 300), UnitValue.create_unit("C", 20), UnitValue.create_unit("m^3", 0.1))
p2 = pipe.Pipe(TS.quasi_steady_solver, UnitValue.create_unit("in", 0.25), "N2", UnitValue.create_unit("m", 1.2)) 
#out = pressure_outlet.PressureOutlet(TS.quasi_steady_solver, UnitValue.create_unit("in", 0.25), "N2", UnitValue.create_unit("psig", 0))
#out = mass_flow_outlet.MassFlowOutlet(TS.quasi_steady_solver, UnitValue.create_unit("inch", 0.25), "N2", UnitValue.create_unit("kg/s", 0.2))
out = pressure_outlet.PressureOutlet(TS.quasi_steady_solver, UnitValue.create_unit("in", 0.25), "N2", UnitValue.create_unit("psi", 100))

# tank = pressure_tank_inlet.PressurantTank(TS.quasi_steady_solver, UnitValue("IMPERIAL", "DISTANCE", "in", 0.8), 'N2', UnitValue("IMPERIAL", "PRESSURE", "psi", 20), UnitValue("METRIC", "TEMPERATURE", "K", 280), UnitValue("METRIC", "VOLUME", "m^3", 0.6))
# p = pipe.Pipe(TS.quasi_steady_solver, UnitValue("IMPERIAL", "DISTANCE", "in", 0.8), "N2", UnitValue("IMPERIAL", "DISTANCE", "in", 5), name="Pipe 1")
# #orifice = critical_orifice.CriticalOrifice(TS.quasi_steady_solver, UnitValue("IMPERIAL", "DISTANCE", "in", 0.8), UnitValue("IMPERIAL", "DISTANCE", "in", 0.8), "N2")
# out = pressure_outlet.PressureOutlet(TS.quasi_steady_solver, UnitValue("IMPERIAL", "DISTANCE", "in", 0.8), "N2", UnitValue("IMPERIAL", "PRESSURE", "psi", 16))
inlet.set_connection(downstream=interface1)
p.set_connection(interface1, interface2)
chamb.set_connection(interface2, interface3)
p2.set_connection(interface3, interface4)
out.set_connection(upstream=interface4)

TS.initialize([inlet, p, chamb, p2, out], 2)
TS.solve()


