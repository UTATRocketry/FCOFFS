# Pipe Documentation
The pipe class represents any pipe-like component in a plumbing system. The expected crossectional shape is a circle and all types of fluids and flows are allowed in this component
## Steady State
The pipe is one of the few components in the software that supports compressible flow. The main thing is to look for the pressure drop across the length of the pipe as the fluid travels through it. For the pipe when calculating the residuals the phase of the fluid at the 
inlet of the pipe is checked to see if it is a liquid or gas. Then after that, the Mach number of the flow is determined and if the number is above 0.3, we cannot assume the flow is incompressible. The residuals for both cases are given below.

### Incompressible 
  If the flow through the tube is considered to be incompressible then we will use the following three residual types:  
  
  - **mass conservation**
  - **energy conservation**
  - **expected pressure loss**

  >[!IMPORTANT]
  >All residuals are normalized by some factor typically one of the input or output values or an average of the values being subtracted. This is to reduce the magnitude of the residuals.
  
  For mass conservation, since the fluid is incompressible we expect the density at the inlet to equal the density at the outlet thus we have:  
  <p align="center">$r_1 = \frac{\rho_{out} - \rho_{in}}{\rho_{out}}$</p>  
  Then for energy conservation, we have that the velocity of the fluid coming into the pipe should equal the velocity of the fluid exiting the pipe:
  <p align="center">$r_2 = \frac{u_{out} - u_{in}}{u_{out}}$</p>  
  Now we have the expected pressure loss (head loss) over the length of the pipe. To get this for incompressible fluid we have to determine the friction factor for the pipe and then use that to determine the pressure loss we expect over the pipe. 
  If the Reynolds number for the fluid is greater than 2000, then the Colebrook method for calculating the friction factor is used (See references for more info on friction factors). This equation is implicit, so an iterative solver is used to get the friction factor. If the flow has a lower Reynolds number than 200 we use $\frac{64}{Re}$.
  After we have the friction factor we multiply by the length of the pipe and divide by the diameter to get the pressure loss coefficient. Once we have the pressure loss coefficient we can multiply this by the dynamic pressure to get the expected pressure loss over the pipe.
  We then take the inlet pressure subtract the expected pressure loss and then also subtract or add any expected pressure loss/gain from a change in height. The final residual subtracts this expected pressure value at the outlet form the guessed outlet pressure by the solver. The overall breakdown for the residual computation is a follows below:  
  
  **Colebrook**  
  <p align="center">$f_D = \frac{1}{\sqrt{f_D}}+2log_{10}(\frac{roughness}{3.7}+\frac{2.51}{Re\sqrt{f_D}})$</p>
  
  **Pressure Loss Coefficient & Delta pressure:**  
  <p align="center">$PLC = \frac{f_D \times L}{D}$</p>  
  <p align="center">$dp = PLC \times q_{in}$</p>
  where L, D, and q are the length and diameter of the pipe and q is the dynamic pressure at the inlet respectively.  
  
  **Expected Pressure:**
  <p align="center">$p_{out, expected} = p_{in} - dp + 9.81\rho_{in}\Delta h$</p>  
  We now finally get our residual of:
  <p align="center">$r_3 = \frac{p_{out} - p_{out, expected}}{p_{out, expected}}$</p>

### Compressible 
  For compressible flow, we can't make as many assumptions and thus the residuals get slightly more complicated. The three governing properties used for the residuals are given in the list below: 
  - **mass conservation**
  - **energy conservation**
  - **momentum conservation**

  For mass conservation, we can simply compare the flow rates at the inlet and outlet of the pipe knowing that they must be equal:  
  <p align="center">$r_1 = \frac{\dot m_{out} - \dot m_{in}}{\dot m_{out}}$</p>  
  For energy conservation, the equation is a little more complicated but it essentially checks that all elements of energy for both the inlet and outlet are equal:
  <p align="center">$r_2 = \frac{u_{in}^2 - (2Cp(T_{out} - T_{in}) + 2\times 9.81\Delta h + u_{out}^2)}{\frac{1}{2}(Cp(T_{out} + T_{in}) +9.81\Delta h + \frac{1}{2}(u_{in}^2 + u_{out}^2))}$</p>  
  For the final residual momentum conservation the process is more complicated. Firstly we need the friction factor which is calculated the same as we do for the incompressible flow. The only difference is we divide by four to convert to the fanning factor. Then we solve the implicit momentum equation for 
  compressible flow which gives us a resultant Mach number for the flow at the outlet of the tube. Since this equation is implicit it must also be iteratively solved for our Mach number out. We then convert the solver guessed outlet speed to its Mach number and then for the final residual we compare these two numbers.  
  
  **Momentum Equation:**  
  <p align="center">$M_{out} = (M_{in} = \gamma M_{in}^2M_{out}^2(\frac{4fL}{D_H}-\frac{\gamma + 1}{2\gamma}ln[\frac{M_{in}^2(1 + \frac{\gamma - 1}{2}M_{out}^2)}{M_{out}^2(1 + \frac{\gamma - 1}{2}M_{in}^2}]))^{\frac{1}{2}}$</p>  
  The final residual is then:
   <p align="center">$r_3 = \frac{M_{out, guessed} - M_{out, expected}}{\frac{1}{2}(M_{out, guessed}+M_{out})}$</p>


Once the residuals are calculated they are returned in a list to be used in the convex optimization.

## Transient 
Still being implemented


# References:
Information on friction factors: https://en.wikipedia.org/wiki/Fanning_friction_factor 
