from FCOFFS.utilities.units import *
from FCOFFS.components import *
from FCOFFS.interfaces.interface import *
from FCOFFS.pressureSystem.PressureSystem import *

PS = PressureSystem(ref_p=UnitValue("IMPERIAL", "PRESSURE", "psi", 15)) 

interface1 = Interface("INTER1")
interface2 = Interface("INTER2")

inlet = pressure_inlet.PressureInlet(PS, diameter=UnitValue("IMPERIAL", "DISTANCE", "in", 0.8), fluid="C2H6O", name="Inlet", pressure=UnitValue("IMPERIAL", "PRESSURE", "psi", 780), temperature=UnitValue("METRIC", "TEMPERATURE", "K", 295))
pipe1 = pipe.Pipe(PS, diameter=UnitValue("IMPERIAL", "DISTANCE", "in", 0.8), fluid="C2H6O", name="PIPE1", length=UnitValue("IMPERIAL", "DISTANCE", "in", 72))
outlet = pressure_outlet.PressureOutlet(PS, diameter=UnitValue("IMPERIAL", "DISTANCE", "in", 0.8), fluid="C2H6O", name="Outlet", pressure=UnitValue("IMPERIAL", "PRESSURE", "psi", 765))

inlet.set_connection(downstream=interface1)
pipe1.set_connection(interface1, interface2)
outlet.set_connection(upstream=interface2)

PS.initialize([inlet,pipe1,outlet])
PS.show_tree()
PS.output()
PS.solve()
PS.output()