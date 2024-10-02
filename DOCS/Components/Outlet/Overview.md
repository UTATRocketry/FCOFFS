# Outlets
Outlets are the components at the very end of the system and set the outlet's initial known conditions for the system. There are currently two types of outlets that can be used in the solver: the **Pressure Outlet** and the **Mass Flow Outlet**. Note unlike other components the outlets only have one residual instead of three. The other two residuals are made up for in the inlet of the system. Note that the outlet only has one interface attached to it and it is on the front/forward side of the component. The residuals for each of these types of outlet are given below:

## Pressure Outlet
For the **Pressure Outler**, you provide the outlet pressure at the system outlet.
### Steady Flow
The only governing equation used in the **Pressure Outler** case is a forced outlet pressure. 

This residual forces the given outlet pressure you provided when initializing the system to be the pressure at the forward interface of the component:
<p align="center">$r_1 = \frac{p_{initial condition} - p_{in}}{p_{in}}$</p> 

### Transient Flow
Still being implemented

## Mass Flow Inlet
For the **Mass Flow Outlet** you must define the mass flow rate at the outlet of the system. 
### Steady Flow
The governing equation used in the **Mass Flow Outlet** case is a forced outlet mass flow rate.
  
This residual forces the initial mass flow rate you provide for the outlet to be the mass flow rate at the forward interface of the component:
<p align="center">$r_1 = \frac{\dot m_{initial condition} - \dot m_{out}}{\dot m_{out}}$</p> 

### Transient Flow
In progress 

# References:
N/A 
