# Houbolt_Jr-PressurizationSystem

The initial research was documented in `Feed System and Injector Analysis.xlsx`. The Python code translated the Excel into an OOP code, and made a few corrections to the initial documentation. User should import the following packages into a fresh `.py` code. 

	from Pressurization_pkg.Utilities import *
	from Pressurization_pkg.componentClass import *
	from Pressurization_pkg.PressureSystem import PressureSystem

The file should be saved immediately outside of the `Pressurization_pkg` package. 

See `example.py` for a sample use case. 

# Solver Theory Guide

A pressure system object includes a list of nodes and components: 
- Node stores the state and properties of the fluids at the interfacial location between the two components connected to it.
- Component contains equations that prescribe the behaviour of such component. This behaviour is translated into a function that evaluates the residual based on the two boundary node states.

## Construction of Nodes and Components

Each nodal state can be represented by $w$, containing three primitives variables:
```math
w = \begin{bmatrix} \rho \\ u \\ p \end{bmatrix}
```
each representing density, velocity, and pressure. These are the building blocks of all other intrinsic and extrinsic properties of the fluid; temperature, viscosity, mass flow, etc can all be computed based on $w$. [^1]

[^1]: Assuming the fluid is calorically perfect and other physical quantities (i.e. area) are known. 

Each component then produces a function

$$ f(w_1,w_2) = r$$

where $r$ is a vector containing three elements, $r_1, r_2, r_3$. The residuals should be normalized to prevent more weighting on one parameter than others. 

For instance, an imaginary component with no loss might expect identical inlet and outlet states (i.e. $w_1 = w_2$). Then the residual can be 
```math
r = \begin{bmatrix} \frac{\rho_1-\rho_2}{\rho_1} \\ \frac{u_1-u_2}{u_1} \\ \frac{p_1-p_2}{p_1} \end{bmatrix}
```

In this case, $r=0$ if and only if $w_1=w_2$. 

## Solver Logic

For a case with $n$ components, the solver takes an initial guess of all the nodal states (after initialization), and iteratively converges to a state where the residual vector is minimized. The nodal state can be represented by $W\in\mathbb{R}^{3n}$, while the residual vector is a vector with the same dimension $R\in\mathbb{R}^{3n}$. The reporting `Residual` value is the RMS of the residual vector. The solver boils down to finding the root of the function

$$ F(W) = R $$

Both the behaviour of all components and the boundary conditions are all represented by the function $F$. 

## Example

**Sample Problem**: PressureInlet - Pipe - Node1 - Injector - PressureOutlet

**Mathematical Description**: 
- Inlet: $`w_i = \begin{bmatrix} \rho_i \\ u_i \\ p_i \end{bmatrix}`$
- Node1: $`w_n = \begin{bmatrix} \rho_n \\ u_n \\ p_n \end{bmatrix}`$
- Outlet: $`w_o = \begin{bmatrix} \rho_o \\ u_o \\ p_o \end{bmatrix}`$
- Pipe: $f_P(w_i,w_n)=r_P$
- Injector: $f_I(w_n,w_o)=r_I$
- Known BC: $p_i, T_i, p_o$

**Pipe**: There are established empirical equations to compute downstream state $\bar{w}_2$ from the upstream state $w_1$, i.e. $Pipe(w_1) = \bar{w}_2$. Using this, the residual is
```math
f_P(w_1,w_2) = \begin{bmatrix} r_{P1} \\ r_{P2} \\ r_{P3} \end{bmatrix} = \begin{bmatrix} \frac{\bar{\rho}_2-\rho_2}{\bar{\rho}_2} \\ \frac{\bar{u}_2-u_2}{\bar{u}_2} \\ \frac{\bar{p}_2-p_2}{\bar{p}_2} \end{bmatrix}
```

**Injector**: Relations exist to compute mass flux based on $p_1,T_1,p_2$, i.e. $`Injector(\begin{bmatrix} \rho_1 \\ p_1 \\ p_2 \end{bmatrix}) = \begin{bmatrix} \bar{\rho}_2 \\ \bar{u}_1 \\ \bar{u}_2 \end{bmatrix}`$. Hence
```math
f_I(w_1,w_2) = \begin{bmatrix} r_{I1} \\ r_{I2} \\ r_{I3} \end{bmatrix} = \begin{bmatrix} \frac{\bar{\rho}_2-\rho_2}{\bar{\rho}_2} \\ \frac{\bar{u}_1-u_1}{\bar{u}_1} \\ \frac{\bar{u}_2-u_2}{\bar{u}_2} \end{bmatrix}
```

**Solver**: We apply root finding algorithm on 

$$ F(W) = R $$

The function input is a list of primitives [^2]
```math
W = \begin{bmatrix} u_i & \rho_n & u_n & p_n & \rho_o & u_o \end{bmatrix}^T
```

[^2]: Keep in mind the pressure inlet BC requires inlet static temperature specification.  

While the output is the list of residuals
```math
R = \begin{bmatrix} r_{P1} & r_{P2} & r_{P3} & r_{I1} & r_{I2} & r_{I3} \end{bmatrix}^T
```

A solution $W^\*$ is accepted when $F(W^\*) \approx 0$ within the specified tolerance. 

# Future Work
## Critical Solver Improvements
1. Expand possible boundary conditions. (Possible BCs: Static Pressure, Total Pressure, Mass Flow, Wall, Vent; not all are critical to the core functionality)
2. Add pseudo-equilibrium explicit time marching capability. $`\frac{dw}{dt}`$ term not considered within each time step, rather a time variable is stored and component behaviour can change with time progression.
3. Apply state limiter to improve stability. (i.e. pressure and temperature should be limited to within a reasonable range)

## Critical System Improvements
1. Describe more components in the `componentClass`. Two-phase tank, pressurant tank, and flow controller (including regulator, critical orifice, venturi, etc.) should be the first ones to add.
2. Should also allow component behaviours to be described by charts in addition to equations.
3. More robust input checks.
4. More human-readable output.
5. More unit options. (i.e. choice of using Pa vs PSI)

## Nice to haves
1. Text inputs (c.f. create the pressuresystem in script)
2. Better illustration of the created system using graphics
3. Support of parallel branches
4. Add implicit time marching scheme
5. Add fully transient capability, i.e. $w$ and $w'$ should both be tracked.
6. Using physics driven method to solve steady-state case, instead of brute-force root finding
7. Combine 4,5,6 for a full dual-time-stepping (DTT) implicit transient solver
8. Connect this to Project DarkMatter to provide better flow rate/pressure estimations
