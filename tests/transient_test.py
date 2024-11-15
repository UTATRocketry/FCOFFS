from FCOFFS.utilities.units import *

from FCOFFS.components import *
from FCOFFS.interfaces.interface import *
from FCOFFS.systems.transient import *

TS = TransientSolver(ref_p=UnitValue("IMPERIAL", "PRESSURE", "psi", 15)) 

interface1 = Interface("INTER1")
interface2 = Interface("INTER2")
interface3 = Interface("INTER3")
interface4 = Interface("INTER4")
#interface5 = Interface("INTER5")

#length of pipe and your outlet forced condition are important


#inlet = mass_flow_inlet.MassFlowInlet(TS.quasi_steady_solver, UnitValue.create_unit("inch", 0.25), "N2", UnitValue.create_unit("kg/s", 0.1), UnitValue.create_unit("C", 20))
inlet = pressure_tank_inlet.PressurantTank(TS.quasi_steady_solver, UnitValue.create_unit("inch", 0.25), "N2", UnitValue.create_unit("psi", 4000), UnitValue.create_unit("C", 20), UnitValue.create_unit("L", 1.5), UnitValue.create_unit("m/s", 100))
#inlet = pressure_inlet.PressureInlet(TS.quasi_steady_solver, UnitValue.create_unit("inch", 0.25), "N2", UnitValue.create_unit("psi", 350), UnitValue.create_unit("C", 20),  UnitValue.create_unit("m/s", 10))
#p = pipe.Pipe(TS.quasi_steady_solver, UnitValue.create_unit("in", 0.25), "N2", UnitValue.create_unit("m", 0.8)) 
orifice = critical_orifice.CriticalOrifice(TS.quasi_steady_solver, UnitValue.create_unit("in",0.25), UnitValue.create_unit("in",0.25), UnitValue.create_unit("in",0.01), "N2", Cd=0.86)
#chamb = chamber.Chamber(TS.quasi_steady_solver, UnitValue.create_unit("inch", 0.25), "N2", UnitValue.create_unit("psi", 300), UnitValue.create_unit("C", 20), UnitValue.create_unit("m^3", 0.1))
#p2 = pipe.Pipe(TS.quasi_steady_solver, UnitValue.create_unit("in", 0.25), "N2", UnitValue.create_unit("m", 1.1))
#inject = injector.Injector(TS.quasi_steady_solver, UnitValue.create_unit("in", 0.25), UnitValue.create_unit("in", 4), diameter_hole=UnitValue("IMPERIAL", "DISTANCE", "in", 0.04), num_hole=60, fluid="N2") 
#out = pressure_outlet.PressureOutlet(TS.quasi_steady_solver, UnitValue.create_unit("in", 0.25), "N2", UnitValue.create_unit("psig", 0))
#out = mass_flow_outlet.MassFlowOutlet(TS.quasi_steady_solver, UnitValue.create_unit("inch", 0.25), "N2", UnitValue.create_unit("kg/s", 0.2))
out = pressure_outlet.PressureOutlet(TS.quasi_steady_solver, UnitValue.create_unit("in", 0.25), "N2", UnitValue.create_unit("psig", 1500))


inlet.set_connection(downstream=interface1)
orifice.set_connection(interface1, interface2)
#chamb.set_connection(interface2, interface3)
#p2.set_connection(interface3, interface4)
#inject.set_connection(interface4, interface5)
out.set_connection(upstream=interface2)

TS.initialize([inlet, orifice, out])
TS.Output.add_probes([(inlet, "mass"), (inlet, "p"), (inlet, "rho"), (interface1, "T"), (interface2, "T")])
#TS.Output.mute_steady_state()
TS.solve(5.5, 0.1)                                                                                                               

#TS.initialize([inlet, p, chamb, p2, out]) #store copy of original components so it actually re initializes
#TS.solve(0.2, 0.1)


