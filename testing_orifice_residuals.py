# Conducting unit tests on the current residuals for the critical orifice component,
# to verify the existence of a root for a given initialized system

from FCOFFS.utilities.units import UnitValue
from FCOFFS.components.critical_orifice import CriticalOrifice
from FCOFFS.state import State
from FCOFFS.fluids.Fluid import Fluid
from numpy import pi

fluid = "N2" 

#Upstream Conditions
p1 = UnitValue.create_unit("psi", 314.7)
T1 = UnitValue.create_unit("K", 295)
#rho_1 = UnitValue.create_unit("kg/m^3", 26.5)
rho_1 = Fluid.density(fluid, T1, p1.convert_base_metric())
inlet_diameter = UnitValue.create_unit("in", 0.25)
inlet_area = pi/4 * inlet_diameter**2
u_1 = UnitValue.create_unit("m/s", 6)
m_dot = rho_1*u_1*inlet_area


state_in = State.State(inlet_area.convert_base_metric(), fluid, rho_1, u_1, p1.convert_base_metric())
state_in.update()

#Constants of Flow
cp_in = Fluid.Cp(fluid, T1, p1)
cv_in = Fluid.Cv(fluid, T1, p1)
gamma = cp_in/cv_in
R_molar = Fluid.get_gas_constant(fluid)

isentropic_coefficient = (1+((gamma-1)/2)*(u_1.value**2/(gamma*296.8*T1.value)))
p_o = p1.value * (isentropic_coefficient**(gamma/(gamma-1)))
T_o = T1.value * isentropic_coefficient
A_star = m_dot.value/(0.86*(2/(gamma+1))**((gamma+1)/(2*(gamma-1)))*p_o*((gamma/(296.8*T_o))**0.5))
A_star_Unit = UnitValue.create_unit("m^2", A_star) 
orifice_diameter = (4 * A_star_Unit / pi )**0.5


#Downstream Conditions
p2 = UnitValue.create_unit("psi", 14.7)
T2 = UnitValue.create_unit("K", ( (p2/p1)**( (gamma-1)/gamma) ) * T1)
rho_2 = Fluid.density(fluid, T2, p2.convert_base_metric())
outlet_diameter = UnitValue.create_unit("in", 0.25)
outlet_area = pi/4 * outlet_diameter**2
u_2 = m_dot / (rho_2*outlet_area)

state_out = State.State(outlet_area.convert_base_metric(), fluid, rho_2, u_2, p2.convert_base_metric())
state_out.update()

the_one_orfice_to_rule_them_all = CriticalOrifice(None, inlet_diameter, outlet_diameter, orifice_diameter, "N2", Cd=0.86)
print(A_star)
print(UnitValue.create_unit("psi", p_o).convert_base_metric(), UnitValue.create_unit("K",T_o).convert_base_metric() )
print(f'Inlet Mass Flow Rate = {m_dot} ')
print(the_one_orfice_to_rule_them_all.eval((state_in, state_out)))
