class Fluid:
    # density [kg/m3]
    # dynamic_viscosity [Pa-s]
    def __init__(self, density, dynamic_viscosity):
        self.density = density
        self.dynamic_viscosity = dynamic_viscosity
        self.kinematic_viscosity = dynamic_viscosity / density

def psi2pa(psi):
    return psi * 6894.4572931783

def pa2psi(pa):
    return pa / 6894.4572931783