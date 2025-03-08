from FCOFFS.utilities.units import *
#from FCOFFS.utilities.uniSS import *
from FCOFFS.components import *
from FCOFFS.interfaces.interface import *
from FCOFFS.systems.steady import *
from FCOFFS.systems.transient import *

import matplotlib.pyplot as plt

SS = SteadySolver(ref_p=UnitValue("IMPERIAL", "PRESSURE", "psig", 0))
# TS = TransientSolver(ref_p=UnitValue("IMPERIAL", "PRESSURE", "psig", 0)) 


interface1 = Interface("INTER1")
interface2 = Interface("INTER2")
interface3 = Interface("INTER3")
interface4 = Interface("INTER4")



inlet = pressure_tank_inlet.PressurantTank(SS, UnitValue.create_unit("in", 0.25), "N2", UnitValue.create_unit("psig", 300), UnitValue.create_unit("C", 15), UnitValue.create_unit("m^3", 0.1), UnitValue.create_unit("m/s", 10))
#inlet = pressure_inlet.PressureInlet(SS.quasi_steady_solver, UnitValue.create_unit("in", 0.25), "N2", UnitValue.create_unit("psi", 800), UnitValue.create_unit("C", 5), UnitValue.create_unit("m/s", 10), "pressure_inlet")
p = pipe.Pipe(SS, UnitValue.create_unit('in', 0.25), "N2", UnitValue.create_unit('ft', 2))
orifice = critical_orifice.CriticalOrifice(SS, UnitValue.create_unit("in",0.25), UnitValue.create_unit("in", 0.25), UnitValue.create_unit("in", 0.0635), "N2", Cd=0.86)
p2 = pipe.Pipe(SS, UnitValue.create_unit('in', 0.25), "N2", UnitValue.create_unit('ft', 2), name = "pipe 2")
outlet = pressure_outlet.PressureOutlet(SS, UnitValue.create_unit("in",0.25), "N2", UnitValue.create_unit("psig", 0))
#outlet = mass_flow_outlet.MassFlowOutlet(SS, UnitValue.create_unit("in", 0.25), "N2", UnitValue.create_unit("kg/s", 0.06))

inlet.set_connection(downstream=interface1)
p.set_connection(interface1, interface2)
orifice.set_connection(interface2, interface3)
p2.set_connection(interface3, interface4)
outlet.set_connection(upstream=interface4)

'''
 inter_face
'''
SS.Output.toggle_steady_state_output()
SS.Output.set_ouput_unit("psi")
SS.initialize([inlet, p, orifice, p2, outlet])
SS.solve()


# SS.solve(0, 0.1)

flow = interface2.state.mdot/interface2.state.rho
#flow.to("SCFM")
print(flow)


# def comp_eval(component: componentClass.ComponentClass, inlet: componentClass.ComponentClass, outlet: componentClass.ComponentClass):
#         system = SteadySolver()
#         system.initialize([inlet, component, outlet])
#         system.solve()




     

