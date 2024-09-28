# Outlets
Outlets are the components at the very end of the system and set the outlet's initial known conditions for the system. There are currently two types of outlets that can be used in the solver: the **Pressure Outlet** and the **Mass Flow Outlet**. Note unlike other components the outlets only have one residual instead of three. The other two residuals are made up for in the inlet of the system. Not ethat the outlet only has one interface attached to it and it is on the front/forward side of the component. The residuals for each of these types of outlet are given below:
# in progress 
## Pressure Outlet
For the **Pressure Outler**, you provide the outlet pressure at the system outlet.
### Steady Flow
The two governing equations used in the case of the **Pressure Inlet** are:
  - Forced inlet pressure
  - Forced inlet temperature

The first residual forces the supplied inlet pressure to be the pressure at the aft interface of the component:
<p align="center">$r_1 = \frac{p_{initial condition} - p_{out}}{p_{initial condition}}$</p> 

The second residual forces the temperature given as the initial temperature to be the temperature at the aft interface of the component:
<p align="center">$r_2 = \frac{T_{initial condition} - T_{out}}{T_{initial condition}}$</p>  

### Transient Flow
Still being implemented

## Mass Flow Inlet
For the **Mass Flow Inlet** you must define the mass flow rate and temperature at the inlet of the system. 
### Steady Flow
The two governing equations used in the case of the **Mass Flow Inlet** are:
  - Forced inlet mass flow rate
  - Forced inlet temperature

The first residua forces the given inlet mass flow rate condition to be the mass flow rate at the aft interface of the component:
<p align="center">$r_1 = \frac{\dot m_{initial condition} - \dot m_{out}}{\dot m_{initial condition}}$</p> 

The second residual forces the temperature given as the initial temperature to be the temperature at the aft interface of the component:
<p align="center">$r_2 = \frac{T_{initial condition} - T_{out}}{T_{initial condition}}$</p>

### Transient Flow
In progress 

# References:
N/A 
