
from FCOFFS.utilities.units import UnitValue
from FCOFFS.components.pipe import Pipe
from FCOFFS.state import State
from FCOFFS.fluids.Fluid import Fluid
import numpy as np
from scipy.optimize import brentq
import matplotlib.pyplot as plt



flow = "compressible"

match flow:
    case  "incompressible": 
        #Upstream Conditions, incompressible flow
        fluid = "C2H6O"
        roughness = 0.045
        p1 = UnitValue.create_unit("psi", 500)
        T1 = UnitValue.create_unit("K", 295)
        rho_1 = Fluid.density(fluid, T1, p1.convert_base_metric())
        u_1 = UnitValue.create_unit("m/s", 0.14)
        length = UnitValue.create_unit("ft", 2)
        diameter = UnitValue.create_unit("in", 0.25)
        inlet_area = np.pi * diameter**2 / 4
        Q_in = rho_1 * u_1**2 / 2

        cs_in = Fluid.local_speed_sound(fluid, T1, rho_1)
        M_in = u_1/cs_in

        state_in = State.State(inlet_area.convert_base_metric(), fluid, rho_1, u_1, p1.convert_base_metric())
        state_in.update()


        # friction_factor = 0.03
        # epsilon
        # PLC = friction_factor * length / diameter

        cp_in = Fluid.Cp(fluid, T1, p1.convert_base_metric())
        cv_in = Fluid.Cv(fluid, T1, p1.convert_base_metric())
        GAMMA = cp_in/cv_in 

        Re = u_1 * diameter / Fluid.kinematic_viscosity(fluid, rho_1)
        def colebrook(f):
            return 1/np.sqrt(f) + 2*np.log10(roughness/3.7 + 2.51/(Re*np.sqrt(f)))
        if Re > 2000:
            F = brentq(colebrook, 0.005, 0.1)
        else:
            F = 64 / Re
        print(F)

        L = UnitValue.create_unit("ft", 2).convert_base_metric()
        DH = UnitValue.create_unit("in", 0.25).convert_base_metric()

        def incompressible_flow(p1, v, darcy_friction_factor, diameter, rho, length):
            p2 = p1 - 0.5*rho*v**2*darcy_friction_factor*length/diameter 
            return p2
        
        # #return (M**2-M_in**2)/(GAMMA*(M**2)*(M_in**2)) + ((GAMMA+1)/(2*GAMMA))*np.log((M_in**2/M**2)*((1+((GAMMA-1)/2)*(M**2))/(1+((GAMMA-1)/2)*(M_in**2)))) - 4*F*L/DH 


        rho_2 = rho_1
        #print(rho_1)
        u_2 = u_1
        #rho_2 = rho_1*(M_in/M2)*((1+((GAMMA-1)/2)*(M2**2))/(1+((GAMMA-1)/2)*(M_in**2)))**(1/2)
        p2 = incompressible_flow(p1.convert_base_metric(), u_1.convert_base_metric(), F, diameter.convert_base_metric(), rho_1.convert_base_metric(), length.convert_base_metric())
        print(p2)
        T2 = Fluid.temp(fluid, rho_2, p2)

        # T2 = T1 * (   (1 + (GAMMA-1)/2 * M_in**2) / (1 + (GAMMA-1)/2 * M_in**2)    )
        print(T1, T2)

        state_out = State.State(inlet_area.convert_base_metric(), fluid, rho_2, u_2, p2)
        state_out.update()


        the_one_pipe_to_rule_them_all = Pipe(None, diameter, fluid, L, roughness=0.045)

        print(the_one_pipe_to_rule_them_all.eval((state_in, state_out)))

    case "compressible":
        
        fluid = "N2"

        roughness = 0.045
        p1 = UnitValue.create_unit("psi", 500).convert_base_metric()
        T1 = UnitValue.create_unit("K", 295)
        rho_1 = Fluid.density(fluid, T1, p1)
        u_1 = UnitValue.create_unit("m/s", 50)
        length = UnitValue.create_unit("m", 1).convert_base_metric()
        diameter = UnitValue.create_unit("in", 0.25).convert_base_metric()
        print(diameter)
        print(length)
        inlet_area = np.pi * diameter**2 / 4

        R = Fluid.get_gas_constant(fluid)
        cp_in = Fluid.Cp(fluid, T1, p1)
        cv_in = Fluid.Cv(fluid, T1, p1)
        GAMMA = cp_in/cv_in 
        print(f"GAMMA = {GAMMA}")
        
        M_in = u_1 / np.sqrt(GAMMA*R*T1) #(Fluid.local_speed_sound(fluid, T1, rho_1))
        print(M_in)
        
        Re = u_1 * diameter / Fluid.kinematic_viscosity(fluid, rho_1)
        def colebrook(f):
            return 1/np.sqrt(f) + 2*np.log10(roughness/3.7 + 2.51/(Re*np.sqrt(f)))
        if Re > 2000:
            F = brentq(colebrook, 0.005, 0.1)
        else:
            F = 64 / Re

        print(F)
            
        state_in = State.State(inlet_area.convert_base_metric(), fluid, rho_1, u_1, p1.convert_base_metric())
        state_in.update()

        def Fanno_line(M2):
            term1 = (M2**2 - M_in**2)/(GAMMA*M_in**2*M2**2)
            term3 = 4*F*length/diameter
            term2 = (GAMMA + 1) / (2*GAMMA)
            term4 = np.log( (M_in**2/M2**2) * ((1+((GAMMA-1)/2)*M2**2)/(1+((GAMMA-1)/2)*M_in**2)) )
            return term1 + term2*term4 - term3
        
        M_out = brentq(Fanno_line, 0.05, 2)
        
        print(f'FannoLine Output : {Fanno_line(M_out)}')
        print(f' Friction Factor = {F} ')
        print(f' Mach Numbers In and Out = {M_in} , {M_out}' )


        p2 = p1*(M_in/M_out)*(((1+(M_in**2)*(GAMMA-1)/2) / (1+(M_out**2)*(GAMMA-1)/2))**0.5)
        print(f'Inlet and Outlet Pressures  = {p1}, {p2} ' )
        
        rho_2 = rho_1*(M_in/M_out)*((1+(M_out**2)*(GAMMA-1)/2) / (1+(M_in**2)*(GAMMA-1)/2))**0.5
        # rho2 = Fluid.density(fluid,T2,p2)
        print(f"Desnity in: {rho_1} ")
        print(f"Densities out: {rho_2} ")

        T2 = Fluid.temp(fluid, rho_2, p2) #T1* (1+(M_in**2)*(GAMMA-1)/2) / (1+(M_out**2)*(GAMMA-1)/2)
        print(f" Temperatures In and Out: {T1} , {T2} ")
        
        u_2 = M_out * np.sqrt(GAMMA*R*T2) #Fluid.local_speed_sound(fluid, T2, rho_2)
        print(f'Velocity In and Out: {u_1} , {u_2}')

        print(f' Inlet and Outlet mass flow rate : {rho_1 * inlet_area* u_1} , {rho_2 * inlet_area * u_2}')

        state_out = State.State(inlet_area.convert_base_metric(), fluid, rho_2, u_2, p2)
        state_out.update()
        
        the_one_pipe_to_rule_them_all = Pipe(None, diameter, fluid, length, roughness=0.045)

        print(the_one_pipe_to_rule_them_all.eval((state_in, state_out)))

# mach out     
#  0.3065593283503023 putting in
#  0.30676238577659143 in residual

# M = np.linspace(0.1, 1, 100 , endpoint=True)
# vals = Fanno_line(M)
# plt.plot(M, vals)
# plt.show()




# M2 = brentq(Fanno_line, 0.2, 1)

# p2 = p1.convert_base_metric()*(M_in/M2)*((1+((GAMMA-1)/2)*(M_in**2))/(1+((GAMMA-1)/2)*(M2**2)))**(1/2)

# # rho_2 = rho_1
# rho_2 = rho_1*(M_in/M2)*((1+((GAMMA-1)/2)*(M2**2))/(1+((GAMMA-1)/2)*(M_in**2)))**(1/2)
# print(rho_1, rho_2)

# T2 = T1 * (   (1 + (GAMMA-1)/2 * M_in**2) / (1 + (GAMMA-1)/2 * M2**2)    )
# print(T1, T2)

# u_2 = M2*Fluid.local_speed_sound(fluid, T2, rho_2)
# state_out = State.State(inlet_area.convert_base_metric(), fluid, rho_2, u_2, p2)
# state_out.update()