'''
Description
'''

from FCOFFS.utilities.utilities import *
from FCOFFS.utilities.units import *

from FCOFFS.components.componentClass import *
from FCOFFS.interfaces.interface import *
from FCOFFS.pressureSystem.PressureSystem import *

PS = PressureSystem(ref_p=(15, UnitPressure.psi))

inlet = PressureInlet((780, UnitPressure.psi), 295)
interface1 = Interface("INTER1")
interface2 = Interface("INTER2")
interface3 = Interface("INTER3")
outlet = PressureOutlet((315, UnitPressure.psi))

pipe1 = Pipe(PS, diameter=(0.8, UnitLength.inch), fluid="N2O", name="PIPE1", length=(72, UnitLength.inch))
bend1 = Pipe(PS, diameter=(0.8, UnitLength.inch), fluid="N2O", name="BEND1", length=(2, UnitLength.inch))
pipe2 = Pipe(PS, diameter=(0.8, UnitLength.inch), fluid="N2O", name="PIPE2", length=(72, UnitLength.inch))
injector = Injector(PS, diameter_in=(0.8, UnitLength.inch), diameter_out=(4, UnitLength.inch), 
                    diameter_hole=(0.04, UnitLength.inch), num_hole=60, fluid="N2O")

pipe1.set_connection(inlet,interface1)
bend1.set_connection(interface1,interface2)
pipe2.set_connection(interface2,interface3)
injector.set_connection(interface3,outlet)

PS.initialize([pipe1,bend1,pipe2,injector],"PressureInlet","PressureOutlet")
PS.show_tree()
PS.output()
PS.solve()
PS.output()