from Pressurization_pkg.Utilities import *
from Pressurization_pkg.componentClass import Source, Pipe, Bend, BallValve
from Pressurization_pkg.PressureSystem import PressureSystem

source = Source(0.02, 0.31, psi2pa(800))
pipe1 = Pipe(1,0.01)
bend1 = Bend(1,0.01,0.05,'Redirector')
valve1 = BallValve(1,0.01,0.08,'Ball Valve')
pipe2 = Pipe(1,0.01)

PS = PressureSystem(source,[pipe1,bend1,valve1,pipe2],'C2H6O')
PS.show(pressure_unit='imperial')