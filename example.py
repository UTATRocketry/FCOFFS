'''
Description
'''

from FCOFFS.utilities.Utilities import *
from FCOFFS.utilities.units import *

from FCOFFS.components import *
from FCOFFS.interfaces.interface import *
from FCOFFS.pressureSystem.PressureSystem import *

PS = PressureSystem(ref_p=UnitValue("IMPERIAL", "PRESSURE", "psi", 15)) #UnitValue("IMPERIAL", "PRESSURE", "psi", 15)

inlet = PressureInlet((780, UnitPressure.psi), 295) # look at chnaging units for these later
interface1 = Interface("INTER1")
interface2 = Interface("INTER2")
interface3 = Interface("INTER3")
outlet = PressureOutlet((315, UnitPressure.psi))

pipe1 = pipe.Pipe(PS, diameter=UnitValue("IMPERIAL", "DISTANCE", "in", 0.8), fluid="N2O", name="PIPE1", length=UnitValue("IMPERIAL", "DISTANCE", "in", 72))
bend1 = pipe.Pipe(PS, diameter=UnitValue("IMPERIAL", "DISTANCE", "in", 0.8), fluid="N2O", name="BEND1", length=UnitValue("IMPERIAL", "DISTANCE", "in", 2))
pipe2 = pipe.Pipe(PS, diameter=UnitValue("IMPERIAL", "DISTANCE", "in", 0.8), fluid="N2O", name="PIPE2", length=UnitValue("IMPERIAL", "DISTANCE", "in", 72))
injector = injector.Injector(PS, diameter_in=UnitValue("IMPERIAL", "DISTANCE", "in", 0.8), diameter_out=UnitValue("IMPERIAL", "DISTANCE", "in", 4), 
                    diameter_hole=UnitValue("IMPERIAL", "DISTANCE", "in", 0.04), num_hole=60, fluid="N2O")

pipe1.set_connection(inlet,interface1)
bend1.set_connection(interface1,interface2)
pipe2.set_connection(interface2,interface3)
injector.set_connection(interface3,outlet)

PS.initialize([pipe1,bend1,pipe2,injector],"PressureInlet","PressureOutlet")
PS.show_tree()
PS.output()
PS.solve()
PS.output()