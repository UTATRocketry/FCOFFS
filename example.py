from Pressurization_pkg.Utilities import *
from Pressurization_pkg.componentClass import Source, Pipe
from Pressurization_pkg.PressureSystem import PressureSystem

source = Source(0.02, 0.31, psi2pa(800))
pipe1 = Pipe(1,0.1)
pipe2 = Pipe(1,0.1)

PS = PressureSystem(source,[pipe1,pipe2])
PS.show()