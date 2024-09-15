'''
Description
'''

from FCOFFS.utilities.units import *

from FCOFFS.components import *
from FCOFFS.interfaces.interface import *
from FCOFFS.pressureSystem.PressureSystem import *

PS = PressureSystem(ref_p=UnitValue("IMPERIAL", "PRESSURE", "psi", 15)) 

#can be dynamically initialized now
interface1 = Interface("INTER1")
interface2 = Interface("INTER2")
interface3 = Interface("INTER3")
interface4 = Interface("INTER4")
interface5 = Interface("INTER5")


inlet = pressure_inlet.PressureInlet(PS, diameter=UnitValue("IMPERIAL", "DISTANCE", "in", 0.8), fluid="N2O", name="Inlet", pressure=UnitValue("IMPERIAL", "PRESSURE", "psi", 780), temperature=UnitValue("METRIC", "TEMPERATURE", "K", 295))
pipe1 = pipe.Pipe(PS, diameter=UnitValue("IMPERIAL", "DISTANCE", "in", 0.8), fluid="N2O", name="PIPE1", length=UnitValue("IMPERIAL", "DISTANCE", "in", 72))
bend1 = pipe.Pipe(PS, diameter=UnitValue("IMPERIAL", "DISTANCE", "in", 0.8), fluid="N2O", name="BEND1", length=UnitValue("IMPERIAL", "DISTANCE", "in", 2))
pipe2 = pipe.Pipe(PS, diameter=UnitValue("IMPERIAL", "DISTANCE", "in", 0.8), fluid="N2O", name="PIPE2", length=UnitValue("IMPERIAL", "DISTANCE", "in", 72))
injectr = injector.Injector(PS, diameter_in=UnitValue("IMPERIAL", "DISTANCE", "in", 0.8), diameter_out=UnitValue("IMPERIAL", "DISTANCE", "in", 4), 
                    diameter_hole=UnitValue("IMPERIAL", "DISTANCE", "in", 0.04), num_hole=60, fluid="N2O")
outlet = pressure_outlet.PressureOutlet(PS, diameter=UnitValue("IMPERIAL", "DISTANCE", "in", 0.8), fluid="N2O", name="Outlet", pressure=UnitValue("IMPERIAL", "PRESSURE", "psi", 315))

#could be done dynmaically
inlet.set_connection(downstream=interface1)
pipe1.set_connection(interface1, interface2)
bend1.set_connection(interface2, interface3)
pipe2.set_connection(interface3, interface4)
injectr.set_connection(interface4, interface5)
outlet.set_connection(upstream=interface5)

'''
 inter_face
'''

PS.initialize([inlet,pipe1,bend1,pipe2,injectr,outlet])
PS.show_tree()
PS.output()
PS.solve()
PS.output()
