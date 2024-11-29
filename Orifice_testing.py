from FCOFFS.utilities.units import *
#from FCOFFS.utilities.units import *
from FCOFFS.components import *
from FCOFFS.interfaces.interface import *
from FCOFFS.systems.steady import *
from FCOFFS.systems.transient import *



TS = TransientSolver(ref_p=UnitValue("IMPERIAL", "PRESSURE", "psig", 0)) 

#can be dynamically initialized now
interface1 = Interface("INTER1")
interface2 = Interface("INTER2")
interface3 = Interface("INTER3")
interface4 = Interface("INTER4")


inlet = pressure_tank_inlet.PressurantTank(TS.quasi_steady_solver, UnitValue.create_unit("in", 0.152), "N2", UnitValue.create_unit("psi", 5), UnitValue.create_unit("C", 15), UnitValue.create_unit("m^3", 0.1), UnitValue.create_unit("m/s", 20))
#inlet = pressure_inlet.PressureInlet(PS, UnitValue.create_unit("in", 0.25), "N2", UnitValue.create_unit("psi", 800), UnitValue.create_unit("C", 5), UnitValue.create_unit("m/s", 10), "pressure_inlet")
p = pipe.Pipe(TS.quasi_steady_solver, UnitValue.create_unit('in', 0.152), UnitValue.create_unit('in', 0.152), "N2", UnitValue.create_unit('ft', 2))
orifice = critical_orifice.CriticalOrifice(TS.quasi_steady_solver, UnitValue.create_unit("in",0.152), UnitValue.create_unit("in", 0.152), UnitValue.create_unit("in", 0.01), "N2", Cd=0.86)
p2 = pipe.Pipe(TS.quasi_steady_solver, UnitValue.create_unit('in', 0.152), UnitValue.create_unit('in', 0.152), "N2", UnitValue.create_unit('ft', 2), name = "pipe 2")
outlet = pressure_outlet.PressureOutlet(TS.quasi_steady_solver, UnitValue.create_unit("in",0.25), "N2", UnitValue.create_unit("psig", 0))

inlet.set_connection(downstream=interface1)
p.set_connection(interface1, interface2)
orifice.set_connection(interface2, interface3)
p2.set_connection(interface3, interface4)
outlet.set_connection(upstream=interface4)

'''
 inter_face
'''

TS.initialize([inlet, p, orifice, p2, outlet])
#TS.Output.toggle_steady_state_output()

TS.solve(1, 0.05)
