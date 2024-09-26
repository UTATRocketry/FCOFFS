# Two Phase Tank
The two-phase tank is a complicated component which encompasses fuel/oxidizer tanks which are pressurized by a gas. This component is the only component which has to consider having two phases throughout it at once. Due to the complexity of this component and it's more transient properties the steady-state version makes some large assumptions and the accuracy is likely low. 

## Steady State
The three governing equations for the pressure regulator are:
  - Conservation of volume
  - Conservation of pressure*
  - Conservation of energy

The first residual is based on the conservation of the volume of our control volume. This is derived as the volume of fluid that enters the tank must equal the volume that leaves the tank. This residual is given by
<p align="center">$r_1 = \frac{\frac{\dot m_{in}}{\rhp_{in}} - \frac{\dot m_{out}}{\rhp_{out}}}{\frac{1}{2}(\frac{\dot m_{in}}{\rhp_{in}} + \frac{\dot m_{out})}$</p> 

The second residual is a large assumption and assumes that the pressure at the inlet of the tank will be equal to the pressure at the outlet:
<p align="center">$r_2 = \frac{p_{in} - p_{out}}{\frac{1}{2}(p_{in} + p_{out})}$</p>  

The third residual is a sort of energy conservation in that we assume the initial temperature of the liquid in the tank will always be the temperature at the outlet state of the tank. Note that $T_{liquid}$ is the initial temperature of the liquid in the tank:
<p align="center">$r_3 = \frac{T_{out} - T_{liquid}}{T_{liquid}}$</p> 

## Transient 
Still being implemented


# References:
N/A
