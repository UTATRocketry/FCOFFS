from CoolProp.CoolProp import PropsSI

class Fluid:
    supported_fluids = {"N2","N2O","C2H6O"}

    # density [kg/m3]
    # dynamic_viscosity [Pa-s]
    def density(fluid,T,p):
        return PropsSI('D', 'T', T, 'P', p, fluid)

    def T(fluid,rho,p):
        return PropsSI('T', 'D',rho, 'P',p, fluid)

    def p(fluid,rho,T):
        return PropsSI('P', 'D',rho, 'T',T, fluid)

    def dynamic_viscosity(fluid,rho=None,T=None,p=None):
        if fluid=="N2O":
            return 0.0000552
        elif fluid=="C2H6O":
            return 0.001198
        else:
            raise Exception("Fluid "+fluid+" not supported")

    def kinematic_viscosity(fluid,rho=None,T=None,p=None):
        if rho == None:
            rho = Fluid.density(fluid,T,p)
        return Fluid.dynamic_viscosity(fluid,rho,T,p) / rho


    # def __init__(self, density, dynamic_viscosity,name=None):
    #     self.name = name
    #     self.density = density
    #     self.dynamic_viscosity = dynamic_viscosity
    #     self.kinematic_viscosity = dynamic_viscosity / density
    #
    # def __repr__(self):
    #     txt = ""
    #     if self.name:
    #         txt = 'Fluid Type: ' + self.name + '\n'
    #     txt += 'Density[kg/m3]: ' + str(self.density) + '\n'
    #     txt += 'Dynamic Viscosity[Pa-s]: ' + str(self.dynamic_viscosity) + '\n'
    #     txt += 'Kinematic Viscosity[m2/s]: ' + str(self.kinematic_viscosity)
    #     return txt

#fluid_N2O = Fluid(PropsSI('D', 'T', 295, 'P', 800*6894.76, 'N2O'),0.0000552,'N2O|Nitrous Oxide')
# http://edge.rit.edu/edge/P07106/public/Nox.pdf (pg. 17)
#fluid_C2H6O = Fluid(PropsSI('D', 'T', 295, 'P', 800*6894.76, 'C2H6O'),0.001198,'C2H60|Ethanol')
# http://www.thermalfluidscentral.org/encyclopedia/index.php/Thermophysical_Properties:_Ethanol

def psi2pa(psi):
    return psi * 6894.4572931783

def pa2psi(pa):
    return pa / 6894.4572931783

def inch2meter(inch):
    return inch / 39.37

def meter2inch(meter):
    return meter * 39.37