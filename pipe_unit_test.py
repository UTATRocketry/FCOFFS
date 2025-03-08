
from FCOFFS.utilities.units import UnitValue
from FCOFFS.components.pipe import Pipe
from FCOFFS.state import State
from FCOFFS.fluids.Fluid import Fluid
import numpy as np
from scipy.optimize import brentq
import matplotlib.pyplot as plt

fluid = "N2"

#Upstream Conditions, incompressible flow
roughness = 0.045
p1 = UnitValue.create_unit("psi", 314.7)
T1 = UnitValue.create_unit("K", 295)
rho_1 = Fluid.density(fluid, T1, p1.convert_base_metric())
u_1 = UnitValue.create_unit("m/s", 120)
length = UnitValue.create_unit("ft", 2)
diameter = UnitValue.create_unit("in", 0.25)
inlet_area = np.pi * diameter**2 / 4
Q_in = rho_1 * u_1**2 / 2

cs_in = Fluid.local_speed_sound(fluid, T1, rho_1)
M_in = u_1/cs_in

state_in = State.State(inlet_area.convert_base_metric(), fluid, rho_1, u_1, p1.convert_base_metric())
state_in.update()


# friction_factor = 0.03
# epsilon
# PLC = friction_factor * length / diameter

cp_in = Fluid.Cp(fluid, T1, p1.convert_base_metric())
cv_in = Fluid.Cv(fluid, T1, p1.convert_base_metric())
GAMMA = cp_in/cv_in 

Re = u_1 * diameter / Fluid.kinematic_viscosity(fluid, rho_1)
def colebrook(f):
    return 1/np.sqrt(f) + 2*np.log10(roughness/3.7 + 2.51/(Re*np.sqrt(f)))
if Re > 2000:
    F = brentq(colebrook, 0.005, 0.1)
else:
    F = 64 / Re
print(F)

L = UnitValue.create_unit("ft", 2).convert_base_metric()
DH = UnitValue.create_unit("in", 0.25).convert_base_metric()

def Fanno_line(M):
    return (M**2-M_in**2)/(GAMMA*(M**2)*(M_in**2)) + ((GAMMA+1)/(2*GAMMA))*np.log((M_in**2/M**2)*((1+((GAMMA-1)/2)*(M**2))/(1+((GAMMA-1)/2)*(M_in**2)))) - ((4*0.068195266*L)/DH)



M = np.linspace(0.1, 1, 100 , endpoint=True)
vals = Fanno_line(M)
plt.plot(M, vals)
plt.show()

# M2 = brentq(Fanno_line, 0.2, 1)

# p2 = p1.convert_base_metric()*(M_in/M2)*((1+((GAMMA-1)/2)*(M_in**2))/(1+((GAMMA-1)/2)*(M2**2)))**(1/2)

# # rho_2 = rho_1
# rho_2 = rho_1*(M_in/M2)*((1+((GAMMA-1)/2)*(M2**2))/(1+((GAMMA-1)/2)*(M_in**2)))**(1/2)
# print(rho_1, rho_2)

# T2 = T1 * (   (1 + (GAMMA-1)/2 * M_in**2) / (1 + (GAMMA-1)/2 * M2**2)    )
# print(T1, T2)

# u_2 = M2*Fluid.local_speed_sound(fluid, T2, rho_2)
# state_out = State.State(inlet_area.convert_base_metric(), fluid, rho_2, u_2, p2)
# state_out.update()


# the_one_pipe_to_rule_them_all = Pipe(None, diameter, fluid, L, roughness=0.045)

# print(the_one_pipe_to_rule_them_all.eval((state_in, state_out)))
