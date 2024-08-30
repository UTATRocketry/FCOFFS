
from FCOFFS.pressureSystem.PressureSystem import PressureSystem
from FCOFFS.state.State import State
from FCOFFS.utilities.units import UnitValue
from FCOFFS.utilities.component_curve import ComponentCurve
from ..components.componentClass import ComponentClass

class PressureRegulator(ComponentClass):
    def __init__(self, parent_system: PressureSystem, diameter: UnitValue, fluid: str, flow_curve_filename: str, set_pressure: UnitValue, method: str = 'linear', name: str = "Pressure_Regulator"):
        super().__init__(parent_system, diameter, fluid, name)

        self.set_pressure = set_pressure
        self.flow_curve = ComponentCurve(flow_curve_filename, method)

    def eval(self, new_states: tuple[State, State] | None = None) -> list:
        if new_states is None:
            state_in = self.interface_in.state
            state_out = self.interface_out.state
        else:
            state_in = new_states[0]
            state_out = new_states[1]

        mdot_in = state_in.rho * state_in.area * state_in.u
        mdot_out = state_out.rho * state_out.area * state_out.u
        res1 = (self.flow_curve(self.set_pressure, state_in.p, state_in.u * state_in.area) - state_out.p ) / state_out.p 
        # (curve(p, q) - statr_out.p) / state_out.p
        res3 = (mdot_out - mdot_in) / mdot_in

        res2 =  
        # (h_out - H_in + 1/2((v_out^2 - v_in^2))) / 
        # (Cp(T_out - T_in) + 1/2(v_out^2 - v_in^2)) / ?
        
        return [res1, res2, res3]

