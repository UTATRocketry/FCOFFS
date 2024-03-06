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

Each nodal state can be represented by $w$, containing three primitives variables:

```math
w = \begin{bmatrix} \rho \\ u \\ p \end{bmatrix}
```

each representing density, velocity, and pressure. These are the building blocks of all other intrinsic and extrinsic properties of the fluid; temperature, viscosity, mass flow can all be computed based on $w$. [^1]

[^1]: Assuming the fluid is calorically perfect and other physical quantities (i.e. area) are known. 

Each component then produces a function

$$ f(w_1,w_2) \rightarrow R$$

where $R$ is a vector containing three elements, $R_1, R_2, R_3$. 
