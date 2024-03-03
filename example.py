from Pressurization_pkg.Utilities import *
from Pressurization_pkg.componentClass import *
from Pressurization_pkg.Node import *
from Pressurization_pkg.PressureSystem import PressureSystem

PS = PressureSystem(ref_p=psi2pa(800))

inlet = PressureInlet(psi2pa(800),285)
node1 = Node("NODE1")
outlet = MassOutlet(1.24)

pipe1 = Pipe(PS, inch2meter(0.8), "N2O", name="PIPE1",length=inch2meter(12))
bend1 = Pipe(PS, inch2meter(0.8), "N2O", name="BEND1",length=inch2meter(2))
pipe2 = Pipe(PS, inch2meter(0.8), "N2O", name="PIPE2",length=inch2meter(72))

pipe1.set_connection(inlet,node1)
bend1.set_connection(node1,pipe2)
pipe2.set_connection(bend1,outlet)

PS.initialize([pipe1,bend1,pipe2],"PressureInlet","MassOutlet")
PS.show_tree()
PS.solve()
PS.output()