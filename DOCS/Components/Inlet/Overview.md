# Inlets
Inlets are a component used at the very start of the system and set the initial known conditions, which will be enforced and used to solve the rest of the system. There are currently two types of inlets that can be used in the solver: the **Pressure Inlet** and the **Mass Flow Inlet**. Unlike most other components the inlets only have two residuals instead of three as to solve the system we only require three known quantities. Our solver setup takes two of these known quantities at the inlet and only one at the outlet, thus we only have two residuals for the inlet. A final thing to note is that, since this component is the inlet and is "where the fluid originates from", there is no interface in front of the component and there is only an interface on the back end (aft) of the component. The residuals for each of these types of inlets are given below:

>[!WARNING] 
>If you use any components that decouple information (e.g., Pressure) from the inlet to the outlet, such as the cavitating venturi, critical orifice, or pressure regulator, you must use a **Pressure Inlet**.

## Pressure Inlet
For the **Pressure Inlet**, you provide the initial pressure and temperature conditions at the system inlet.
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
