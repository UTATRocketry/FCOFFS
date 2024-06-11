'''
Description
'''

from FCOFFS.utilities.utilities import *
from FCOFFS.utilities.units import *

from FCOFFS.components.componentClass import *
from FCOFFS.nodes.Node import *
from FCOFFS.pressureSystem.PressureSystem import PressureSystem

PS = PressureSystem(ref_p=(15, UnitPressure.psi))

inlet = PressureInlet((780, UnitPressure.psi), 295)
node1 = Node("NODE1")
node2 = Node("NODE2")
node3 = Node("NODE3")
outlet = PressureOutlet((315, UnitPressure.psi))

pipe1 = Pipe(PS, (0.8, UnitLength.inch), "N2O", name="PIPE1", length=(72, UnitLength.inch))
bend1 = Pipe(PS, (0.8, UnitLength.inch), "N2O", name="BEND1", length=(2, UnitLength.inch))
pipe2 = Pipe(PS, (0.8, UnitLength.inch), "N2O", name="PIPE2", length=(72, UnitLength.inch))
injector = Injector(PS, (0.8, UnitLength.inch), (4, UnitLength.inch), (0.04, UnitLength.inch), 60, "N2O")

pipe1.set_connection(inlet,node1)
bend1.set_connection(node1,node2)
pipe2.set_connection(node2,node3)
injector.set_connection(node3,outlet)

PS.initialize([pipe1,bend1,pipe2,injector],"PressureInlet","PressureOutlet")
PS.show_tree()
PS.output()
PS.solve()
PS.output()