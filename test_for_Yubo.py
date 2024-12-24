import os

from FCOFFS.utilities.units import *
from FCOFFS.components import *
from FCOFFS.interfaces.interface import *
from FCOFFS.systems.transient import *

SS = SteadySolver()
TS = TransientSolver(ref_p=UnitValue("IMPERIAL", "PRESSURE", "psi", 15)) 

interface1 = Interface("INTER1")
interface2 = Interface("INTER2")
interface3 = Interface("INTER3")
interface4 = Interface("INTER4")
interface5 = Interface("INTER5")
interface6 = Interface("INTER6")
interface7 = Interface("INTER7")
interface8 = Interface("INTER8")
interface9 = Interface("INTER9")
interface10 = Interface("INTER10")
interface11 = Interface("INTER11")

inlet = pressure_tank_inlet.PressurantTank(TS.quasi_steady_solver, UnitValue.create_unit('inch', 0.152), "N2", UnitValue.create_unit("psi", 2000), UnitValue.create_unit("c", 15), UnitValue.create_unit("m^3", 0.1), UnitValue.create_unit("m/s", 10))
pipe1 = pipe.Pipe(TS.quasi_steady_solver, UnitValue.create_unit('inch', 0.192), UnitValue.create_unit('inch', 0.192), "N2", UnitValue.create_unit('inch', 6), name="Pipe 1")
reg = pressure_regulator.PressureRegulator(TS.quasi_steady_solver, UnitValue.create_unit('inch', 0.192), "N2", os.path.join(os.getcwd(), "DOCS", "Components", "Pressure Regulator", "Regulator Curves", "KPF.csv"), UnitValue.create_unit("psi", 800))
pipe2 = pipe.Pipe(TS.quasi_steady_solver, UnitValue.create_unit('inch', 0.192), UnitValue.create_unit('inch', 0.192), "N2", UnitValue.create_unit('ft', 1), name="Pipe 2")
diffuser1= pipe.Pipe(TS.quasi_steady_solver, UnitValue.create_unit('inch', 0.192), UnitValue.create_unit('inch', 0.25), "N2", UnitValue.create_unit('inch', 0.5), name="area change 1")
tube = pipe.Pipe(TS.quasi_steady_solver, UnitValue.create_unit('inch', 0.25), UnitValue.create_unit('inch', 0.25), "N2", UnitValue.create_unit('feet', 20), name="tube", roughness=0.000003)
diffuser2 = pipe.Pipe(TS.quasi_steady_solver, UnitValue.create_unit('inch', 0.25), UnitValue.create_unit('inch', 0.192), "N2", UnitValue.create_unit('inch', 0.5), name="area change 2")
pipe3 = pipe.Pipe(TS.quasi_steady_solver, UnitValue.create_unit('inch', 0.192), UnitValue.create_unit('inch', 0.192), "N2", UnitValue.create_unit('ft', 1), name="pipe 3")
bend1 = pipe.Pipe(TS.quasi_steady_solver, UnitValue.create_unit('inch', 0.192), UnitValue.create_unit('inch', 0.192), "N2", UnitValue.create_unit('inch', 2), name="bend 1")
pipe4 = pipe.Pipe(TS.quasi_steady_solver, UnitValue.create_unit('inch', 0.192), UnitValue.create_unit('inch', 0.192), "N2", UnitValue.create_unit('ft', 1), name="pipe 4")
bend2 = pipe.Pipe(TS.quasi_steady_solver, UnitValue.create_unit('inch', 0.192), UnitValue.create_unit('inch', 0.192), "N2", UnitValue.create_unit('inch', 2), name="bend 2")
chamb = chamber.Chamber(TS.quasi_steady_solver, UnitValue.create_unit("inch", 0.192), "N2", UnitValue.create_unit("psi", 700), UnitValue.cret)

outlet = pressure_outlet.PressureOutlet(TS.quasi_steady_solver, UnitValue.create_unit('inch', 0.192), "N2", UnitValue.create_unit('psi', 700))

inlet.set_connection(downstream=interface1)
pipe1.set_connection(interface1, interface2)
reg.set_connection(interface2, interface3)
pipe2.set_connection(interface3, interface4)
diffuser1.set_connection(interface4, interface5)
tube.set_connection(interface5, interface6)
diffuser2.set_connection(interface6, interface7)
pipe3.set_connection(interface7, interface8)
bend1.set_connection(interface8, interface9)
pipe4.set_connection(interface9, interface10)
bend2.set_connection(interface10, interface11)
outlet.set_connection(upstream=interface11)

# SS.initialize([inlet, pipe1, reg, pipe2, diffuser1, tube, diffuser2, pipe3, bend1, pipe4, bend2, outlet])
# SS.Output.toggle_steady_state_output()
# SS.Output.set_ouput_unit("psi")
# SS.solve()

TS.initialize([inlet, pipe1, reg, pipe2, diffuser1, tube, diffuser2, pipe3, bend1, pipe4, bend2, outlet])
TS.Output.toggle_steady_state_output()
TS.Output.toggle_convergence_output()
TS.Output.set_ouput_unit("psi")
TS.Output.add_probes(((interface11, "u"), (interface11, "mdot"), (interface5, "p"), (interface6, "p")))
TS.solve(0.1, 0.01)

