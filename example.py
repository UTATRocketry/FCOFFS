from Pressurization_pkg.Utilities import *
from Pressurization_pkg.componentClass import *
from Pressurization_pkg.Node import *
from Pressurization_pkg.PressureSystem import PressureSystem

PS = PressureSystem(ref_p=psi2pa(15))

inlet = PressureInlet(psi2pa(780),295)
node1 = Node("NODE1")
node2 = Node("NODE2")
node3 = Node("NODE3")
outlet = PressureOutlet(psi2pa(315))

pipe1 = Pipe(PS, inch2meter(0.8), "N2O", name="PIPE1",length=inch2meter(72))
bend1 = Pipe(PS, inch2meter(0.8), "N2O", name="BEND1",length=inch2meter(2))
pipe2 = Pipe(PS, inch2meter(0.8), "N2O", name="PIPE2",length=inch2meter(72))
injector = Injector(PS, inch2meter(0.8), inch2meter(4), inch2meter(0.04),60,"N2O")

pipe1.set_connection(inlet,node1)
bend1.set_connection(node1,node2)
pipe2.set_connection(node2,node3)
injector.set_connection(node3,outlet)

PS.initialize([pipe1,bend1,pipe2,injector],"PressureInlet","PressureOutlet")
PS.show_tree()
PS.output()
PS.solve()
PS.output()