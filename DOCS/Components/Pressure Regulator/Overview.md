# Pressure Regulator Documentation
The pressure regulator class is used to simulate the effects of having a pressure regulator in your plumbing system. It is one of the components in the software that uses manufacturer graphs and data to come up with one of its residuals (By extrapolating and interpolating the data). In this case, pressure regulators are somewhat more complex than some other graph/data-reliant type components as their curves have three inputs (flow rate, set pressure, and inlet pressure) to give one output (outlet pressure) thus we had to interpolate in 3 dimensions. If you are more interested in the curves see the references section.

## Data Acquisition
To use the regulator for a given regulator you must have the relevant curve data for the regulator you wish to model. To do this, we ask that you go to the site which contains the flow curves for your given regulator and then use a tool such as https://plotdigitizer.com/app to grab data points from the curve provided by the manufacture if they do not provide data points for you. For this component, the CSV file containing the flow curve data should have the format below (the first line should be "Pressure Regulator" and then the type details and then the rest of the CSV should follow the table structure below):
Pressure Regulator (type) (flow_coefficient) (PCP)
| Set Pressure  | Inlet Pressure | Flow Rate | Outlet Pressure |
| ------------- | ------------- | ----------- | ----------- |
| Input  | Input | Input | Output |
| (enter unit)  |  (enter unit)  | (enter unit) | (enter unit) |
| data | data | data | data |
| ... | ... | ... | ... |
---------
If you need more guidance you can also look at the couple of regulator flow curve files we have already created which are also in the folder under the Data subfolder. 

>[!IMPORTANT]
>When initializing a pressure regulator component ensure you provide the absolute file path to the manufacturer regulator curve data CSV as this is what is expected.

## Steady State
The three governing equations for the pressure regulator are:
  - Conservation of energy
  - Conservation of mass
  - Manufacturing pressure and flow plots

The first residual is based on the interpolated curve provided by the manufacturer which gives us the expected output pressure given the flow rate, set pressure, and inlet pressure of the regulator:
<p align="center">$r_1 = \frac{p_{interpolated} - p_{out}}{p_{out}}$</p> 

The second residual is simply the conservation of mass and thus have that the mass flow rate in and out of the regulator must be equal:
<p align="center">$r_2 = \frac{\dot m_{out} - \dot m_{in}}{\dot m_{in}}$</p>  

The third residual is about the conservation of energy. We are assuming that the height difference is negligible for the inlet and outlet we have that the energy at either the inlet and outlet is a property of kinetic energy and specific internal energy. We first calculate the inlet and outlet energies:
<p align="center">$e_{in} = Cp_{in}T_{in} + \frac{1}{2}v_{in}^{2} $</p> 
<p align="center">$e_{out} = Cp_{out}T_{out} + \frac{1}{2}v_{out}^{2} $</p>
Finally, we arrive at the residual:
<p align="center">$r_3 = \frac{e_{out} - e_{in}}{\frac{1}{2}(e_{in}+e_{out})}$</p> 

## Transient 
Still being implemented


# References:
Pressure regulator curves: https://www.swagelok.com/downloads/webcatalogs/en/ms-06-114.pdf 
