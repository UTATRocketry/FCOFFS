import pandas as pd 
import matplotlib.pyplot as plt
import warnings
from queue import LifoQueue

from FCOFFS.components.componentClass import ComponentClass
from FCOFFS.interfaces.interface import Interface
from FCOFFS.utilities.units import UnitValue

class OutputHandler:
    def __init__(self, filename: str, residual_queue: LifoQueue=LifoQueue()):
        
        self.__filename = filename
        self.residual_queue = residual_queue

        #Customization variables
        self.__active = True
        self._interface_muted = False
        self._transient_muted = False
        self._full_log_muted = False
        self._components_log_muted = False
        self._interfaces_log_muted = False
        self._probes_log_muted = False
        self._convergence_muted = False
        self._probe_plotting_muted = False
        self.__df_toggles = {'f': self._full_log_muted, 'i': self._components_log_muted, 'c': self._interfaces_log_muted, 'p':self._probes_log_muted }

        #Logs initialization
        self.__full_df = pd.DataFrame({"Time": [], "Converged Residual": [], "Object": [], "Density (kg/m^3)": [], "Pressure (kg/ms^2)": [], "Velocity (m/s)": [], "Temperature (K)": [], "Mass Flow Rate (kg/s)": [], "Mass (kg)": [], "Dynamic Pressure (kg/ms^2)": []})
        self.__interfaces_df = pd.DataFrame({"Time": [], "Converged Residual": [], "Interface": [], "Density (kg/m^3)": [], "Pressure (kg/ms^2)": [], "Velocity (m/s)": [], "Temperature (K)": [], "Mass Flow Rate (kg/s)": [], "Dynamic Pressure (kg/ms^2)": []})
        self.__components_df = pd.DataFrame({"Time": [], "Converged Residual": [], "Component": [], "Mass (kg)": [], "Pressure (kg/ms^2)": [], "Density (kg/m^3)": [], "Temperature (K)": []})
        self.__probes_df = None

        #Ouput units
        self.__Output_Unit = {"DISTANCE": "m", 
                              "PRESSURE": "Pa", 
                              "MASS": "kg", 
                              "VELOCITY": "m/s", 
                              "DENSITY": "kg/m^3", 
                              "VOLUME": "m^3", 
                              "AREA": "m^2", 
                              "TEMPERATURE": "K", 
                              "MASS FLOW RATE": "kg/s"}

    def initialize(self, objects):
        self.__objects = objects
        self.__iter_counter = 0
        self.__time = 0 
        self.__probes = []

    def _run(self, dt: float):
        if self.__active is False:
            return
        
        if self.__iter_counter == 0:
            probe_dict = {"Time": []}
            for probe in self.__probes:
                 probe_dict[probe[2]] = []
            self.__probes_df = pd.DataFrame(probe_dict)

        self.__residual = self.residual_queue.get()
        if dt > 0:
            print(f"\nTime Step: {self.__time}, Iteration: {self.__iter_counter}, Convergence Residual: {self.__residual}")
            if self._convergence_muted is False:
                residuals = [self.__residual]
                while self.residual_queue.empty() is False:
                    residuals.append(self.residual_queue.get())
                for i in reversed(range(len(residuals))):
                    print(f"Steady Iteration {len(residuals) - i} Residual = {residuals[i]}")
            if self._interface_muted is False:
                self.print_state()
        else:
            if self._convergence_muted is False:
                print(f"Steady Iteration {self.__iter_counter}, Residual = {self.__residual}")
            if self._interface_muted is False:
                self.print_state()

        self.__add_to_log()
        self.__iter_counter += 1
        self.__time += dt

    def _finish(self):
        if self.__active is False:
            return
        self.__save_logs()
        if self._interface_muted is True:
            self.print_state()
        if self._transient_muted is False and len(self.__probes) > 0:
            self.__transient_results()
        if self._probes_log_muted is False and len(self.__probes) > 0:
            self.__plot_probes()
        self.__reset_dataframes()

    def __add_to_log(self): 
        for obj in self.__objects:
            if isinstance(obj, ComponentClass):
                self.__full_df = pd.concat([self.__full_df, pd.DataFrame({"Time": [self.__time],
                                                                          "Converged Residual": [self.__residual],
                                                                          "Object": [obj.name], 
                                                                          "Density (kg/m^3)": [obj.rho.value if isinstance(getattr(obj, "rho", 'N/A'), UnitValue) else "N/A"], 
                                                                          "Pressure (kg/ms^2)": [obj.p.value if isinstance(getattr(obj, "p", 'N/A'), UnitValue) else "N/A"], 
                                                                          "Velocity (m/s)": [obj.u.value if isinstance(getattr(obj, "u", 'N/A'), UnitValue) else "N/A"], 
                                                                          "Temperature (K)": [obj.T.value if isinstance(getattr(obj, "T", 'N/A'), UnitValue) else "N/A"], 
                                                                          "Mass Flow Rate (kg/s)": [obj.mdot.value if isinstance(getattr(obj, "mdot", 'N/A'), UnitValue) else "N/A"], 
                                                                          "Mass (kg)": [obj.mass.value if isinstance(getattr(obj, "mass", 'N/A'), UnitValue) else "N/A"], 
                                                                          "Dynamic Pressure (kg/ms^2)": [obj.q.value if isinstance(getattr(obj, "q", 'N/A'), UnitValue) else "N/A"]})], 
                                                                          ignore_index=True)

                self.__components_df = pd.concat([self.__components_df, pd.DataFrame({"Time": [self.__time], 
                                                                                      "Converged Residual": [self.__residual],
                                                                                          "Component": [obj.name], 
                                                                                          "Mass (kg)": [obj.mass.value if isinstance(getattr(obj, "mass", 'N/A'), UnitValue) else "N/A"], 
                                                                                          "Pressure (kg/ms^2)": [obj.p.value if isinstance(getattr(obj, "p", 'N/A'), UnitValue) else "N/A"], 
                                                                                          "Density (kg/m^3)": [obj.rho.value if isinstance(getattr(obj, "rho", 'N/A'), UnitValue) else "N/A"], 
                                                                                          "Temperature (K)": [obj.T.value if isinstance(getattr(obj, "T", 'N/A'), UnitValue) else "N/A"]})], 
                                                                                          ignore_index=True)
            if isinstance(obj, Interface):
                self.__full_df = pd.concat([self.__full_df, pd.DataFrame({"Time": [self.__time],
                                                                          "Converged Residual": [self.__residual], 
                                                                          "Object": [obj.name], 
                                                                          "Density (kg/m^3)": [obj.state.rho.value], 
                                                                          "Pressure (kg/ms^2)": [obj.state.p.value], 
                                                                          "Velocity (m/s)": [obj.state.u.value], 
                                                                          "Temperature (K)": [obj.state.T.value], 
                                                                          "Mass Flow Rate (kg/s)": [obj.state.mdot.value], 
                                                                          "Mass (kg)": [obj.mass.value if isinstance(getattr(obj.state, "mass", 'N/A'), UnitValue) else "N/A"], 
                                                                          "Dynamic Pressure (kg/ms^2)": [obj.state.q.value]})], 
                                                                          ignore_index=True)
                self.__interfaces_df = pd.concat([self.__interfaces_df, pd.DataFrame({"Time": [self.__time],
                                                                                      "Converged Residual": [self.__residual], 
                                                                                      "Interface": [obj.name], 
                                                                                      "Density (kg/m^3)": [obj.state.rho.value], 
                                                                                      "Pressure (kg/ms^2)": [obj.state.p.value], 
                                                                                      "Velocity (m/s)": [obj.state.u.value], 
                                                                                      "Temperature (K)": [obj.state.T.value], 
                                                                                      "Mass Flow Rate (kg/s)": [obj.state.mdot.value], 
                                                                                      "Dynamic Pressure (kg/ms^2)": [obj.state.q.value]})], 
                                                                                      ignore_index=True)
        probe_dict = {"Time": [self.__time]}
        for probe in self.__probes:
            if isinstance(probe[0], Interface):
                probe_dict[probe[2]] = [getattr(probe[0].state, probe[1]).value]
            elif isinstance(probe[0], ComponentClass):
                probe_dict[probe[2]] = [getattr(probe[0], probe[1]).value]
        self.__probes_df = pd.concat([self.__probes_df, pd.DataFrame(probe_dict)], ignore_index=True)

    def print_state(self):
        header = f"{'Name':<12} {'Rho':<20} {'Velocity':<20} {'Pressure':<20} {'Temp':<15} {'Mdot':<20} {'Area':<20} {'Fluid':<10}"
        
        output_string = header + "\n" + "-" * len(header) + "\n"
        
        for obj in self.__objects:
            if obj.type == 'interface':
                state = obj.state
                
                output_string += f"{obj.name:<12} {str(round(getattr(state, 'rho', 'N/A').copy().to(self.__Output_Unit['DENSITY']), 4)):<20} {str(round(getattr(state, 'u', 'N/A').copy().to(self.__Output_Unit['VELOCITY']), 2)):<20} {str(round(getattr(state, 'p', 'N/A').copy().to(self.__Output_Unit['PRESSURE']), 4)):<20} {str(round(getattr(state, 'T', 'N/A').copy().to(self.__Output_Unit['TEMPERATURE']), 4)):<15} {str(round(getattr(state, 'mdot', 'N/A').copy().to(self.__Output_Unit['MASS FLOW RATE']), 4)):<20} {str(round(getattr(state, 'area', 'N/A').copy().to(self.__Output_Unit['AREA']), 8)):<20} {getattr(state, 'fluid', 'N/A'):<10}\n"
            else:
                output_string += f"{obj.name:<12}\n"
        output_string = output_string[:-1]
        print("\n" + output_string + "\n")
        #return output_string # maybe needed in future

    def show_tree(self):
        for i in range(len(self.__objects)-1):
            print(self.__objects[i].name)
            print(' | ')
        print(self.__objects[-1].name)
        print()
    
    def __transient_results(self):

        header = f"{'Time':<10}"
        for probe in self.__probes:
            if isinstance(probe[0], ComponentClass):
                unit = self.__Output_Unit[getattr(probe[0], probe[1]).get_dimension]
            elif isinstance(probe[0], Interface):
                unit = self.__Output_Unit[getattr(probe[0].state, probe[1]).get_dimension]
            header += f"{(probe[0].name + '(' + unit + ')'):<25}"
        output_string = header + "\n" + "-" * len(header) + "\n"
        for _, row in self.__probes_df.iterrows():
            output_string += f"{str(round(row['Time'], 6)):<10} "
            for probe in self.__probes:
                if isinstance(probe[0], ComponentClass):
                    unit = self.__Output_Unit[getattr(probe[0], probe[1]).get_dimension]
                    dim = getattr(probe[0], probe[1]).get_dimension
                    base_unit = list(UnitValue.UNITS["METRIC"][getattr(probe[0], probe[1]).get_dimension].keys())[0]
                elif isinstance(probe[0], Interface):
                    unit = self.__Output_Unit[getattr(probe[0].state, probe[1]).get_dimension]
                    dim = getattr(probe[0].state, probe[1]).get_dimension
                    base_unit = list(UnitValue.UNITS["METRIC"][getattr(probe[0].state, probe[1]).get_dimension].keys())[0]
                temp = UnitValue("METRIC", dim, base_unit, row[probe[2]])
                temp.to(unit)
                output_string += f"{str(round(temp.value, 6)):<25} "
            output_string += "\n"

        print("\n" + output_string + "\n")
        #return output_string maybe for future need

    def __plot_probes(self):
        time = self.__probes_df["Time"].to_list()
        for probe in self.__probes:
            values = self.__probes_df[probe[2]].to_list()
            if isinstance(probe[0], ComponentClass):
                unit = self.__Output_Unit[getattr(probe[0], probe[1]).get_dimension]
                dim = getattr(probe[0], probe[1]).get_dimension
                base_unit = list(UnitValue.UNITS["METRIC"][getattr(probe[0], probe[1]).get_dimension].keys())[0]
            elif isinstance(probe[0], Interface):
                unit = self.__Output_Unit[getattr(probe[0].state, probe[1]).get_dimension]
                dim = getattr(probe[0].state, probe[1]).get_dimension
                base_unit = list(UnitValue.UNITS["METRIC"][getattr(probe[0].state, probe[1]).get_dimension].keys())[0]
            if base_unit != unit:
                for i in range(len(values)):
                    temp = UnitValue("METRIC", dim, base_unit, values[i])
                    temp.to(unit)
                    values[i] = temp.value

            fig = plt.figure(probe[2] + "Vs Time Plot")
            plt.plot(time, values, marker="o", markersize=4)
            plt.grid()
            plt.title(f"{probe[0].name} {dim} ({unit}) vs Time", fontsize=12, fontweight='bold', fontname='Times New Roman')
            plt.xlabel("Time (s)", fontsize=11, fontname='Times New Roman')
            plt.ylabel(f"{dim} ({unit})", fontsize=11, fontname='Times New Roman')
            plt.xticks(fontsize=10, fontname='Times New Roman')
            plt.yticks(fontsize=10, fontname='Times New Roman')
        plt.show() 
            
    def __save_logs(self):
        if self._full_log_muted is False:
            self.__full_df.to_csv(f"{self.__filename} Objects.log", index=False)
        if self._interfaces_log_muted is False:
            self.__interfaces_df.to_csv(f"{self.__filename} Interfaces.log", index=False)
        if self._components_log_muted is False:
            self.__components_df.to_csv(f"{self.__filename} Components.log", index=False)
        if self._probes_log_muted is False:
            if len(self.__probes) > 0:
                self.__probes_df.to_csv(f"{self.__filename} Probes.log", index=False)
        if self._full_log_muted or self._interfaces_log_muted or self._components_log_muted or self._probes_log_muted:
            print("LOGS SAVED\n")
    
    def __reset_dataframes(self):
        self.__full_df = self.__full_df[0:0]
        self.__interfaces_df = self.__interfaces_df[0:0]
        self.__components_df = self.__components_df[0:0]
        self.__probes_df = None

    def add_probes(self, items: tuple[ComponentClass, ]|list[tuple]):
        # make probes be of (item, "atribute name ")
        #corresponding = {"p": "Pressure (kg/ms^2)", "rho": "Density (kg/m^3)", "u": "Velocity (m/s)", "T": "Temperature (K)", "mdot": "Mass Flow Rate (kg/s)", "mass": "Mass (kg)", "q": "Dynamic Pressure (kg/ms^2)"}
        if isinstance(items[0], tuple) or isinstance(items[0], list):
            for item in items:
                if self.__check_object_exists(item) is False:
                    warnings.warn(f"Object and or object attribute {item} does not exist! Skipping this probe.")
                    continue
                if isinstance(item[0], ComponentClass):
                    probe = [item[0], item[1], f"{item[0].name} {getattr(item[0], item[1]).get_dimension} ({getattr(item[0], item[1]).get_unit})"] 
                elif isinstance(item[0], Interface):
                    probe = [item[0], item[1], f"{item[0].name} {getattr(item[0].state, item[1]).get_dimension} ({getattr(item[0].state, item[1]).get_unit})"]
                self.__probes.append(probe)
        else:
            if self.__check_object_exists(items) is False:
                    warnings.warn(f"Object and or object attribute {items} does not exist! Skipping this probe.")
            else:
                self.__probes.append(item)

    def remove_probe(self, item: tuple):
        for ind in range(len(self.__probes)):
            if item[0] == self.__probes[ind][0] and item[1] == self.__probes[ind][1]:
                self.__probes.pop(ind)
                return
        warnings.warn(f"No probe was removed as probe {item} doesn't exist.")
                
    def __check_object_exists(self, item):
        for obj in self.__objects:
            if obj == item[0]:
                if isinstance(obj, ComponentClass) and getattr(obj, item[1], 'N/A') != "N/A":
                    return True
                elif isinstance(obj, Interface) and getattr(obj.state, item[1], 'N/A') != "N/A":
                    return True
        return False
    
    # add section of fucntions that creates a software log and logs all actions of the software. Would need to be callable outside by other functions
    # in software so they can add there messages to log. 

    def set_ouput_unit(self, unit):
        temp_unit = UnitValue.create_unit(unit, 0)
        dimension = temp_unit.get_dimension
        self.__Output_Unit[dimension] = temp_unit.get_unit

    def show_config(self):
        output = "\n\n--------------- OUTPUT CONFIGURATIONS ---------------\n"
        output += f"Output Handler Active: {self.__active}\n"
        output += f"Steady State Ouput Muted: {self._interface_muted}\n"
        output += f"Steady Convergence Ouput Muted {self._convergence_muted}\n"
        output += f"Transient Ouput Muted: {self._transient_muted}\n"
        output += f"Full Log Active: {self._full_log_muted}\n"
        output += f"Interface Log Active: {self._interfaces_log_muted}\n"
        output += f"Component Log Active: {self._components_log_muted}\n"
        output += f"Probe Log Active: {self._probes_log_muted}\n"
        output +="-----------------------------------------------------\n"
        print(output)

    def toggle_active(self):
        self.__active = True if self.__active is False else False
        print(f"{self.__filename}, Output Handler set to {'Active' if self.__active is True else 'Unactive'}")

    def toggle_steady_state_output(self):
        self._interface_muted = True if self._interface_muted is False else False
        print(f"{self.__filename}, Steady State Ouput {'Muted' if self._interface_muted == True else 'Unmuted'}")

    def toggle_convergence_output(self):
        self._convergence_muted = True if self._convergence_muted is False else False
        print(f"{self.__filename}, Convergence Ouput {'Muted' if self._interface_muted == True else 'Unmuted'}")

    def toggle_transient_ouput(self):
        self._transient_muted = True if self._transient_muted is False else False
        print(f"{self.__filename}, Transient Ouput {'Muted' if self._transient_muted == True else 'Unmuted'}")

    def toggle_log_ouput(self, log: str):
        '''
        arguments: log: 'c' for component, 'i" for interface, 'f' for full, 'p' for probe.
        '''
        try:
            self.__df_toggles[log] = True if self.__df_toggles[log] is False else False
            print(f"{self.__filename}, {log} log {'Muted' if self._df_toggles[log] == True else 'Unmuted'}")
        except Exception:
            raise ValueError(f"Argument {log} is not valid, please use 'f', 'i', 'c', or 'p'")

    def toggle_probe_plotting(self):
        self._probe_plotting_muted = True if self._probe_plotting_muted is False else False
        print(f"{self.__filename}, Probe Plotting {'Muted' if self._probe_plotting_muted == True else 'Unmuted'}")


    
    
    


    



    
    