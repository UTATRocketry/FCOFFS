# Pressure Regulator Documentation
The pressure regulator class is used to simulate the effects of having a pressure regulator in your plumbing system. It is one of the components in the software that uses manufacturer graphs and data to come up with one of its residuals (By extrapolating and interpolating the data). In this case, pressure regulators are somewhat more complex then some other graph/data-reliant type components as it's curves have three inputs (flow rate, set pressure, and inlet pressure) to give one output (outlet pressure) thus we had to interpolate in 3 dimensions.

## Steady State
The three governing equations for the pressure regulator are:



## Transient 
Still being implemented


# References:
