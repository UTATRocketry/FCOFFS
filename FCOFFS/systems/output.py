import pandas as pd 
import warnings

from FCOFFS.components.componentClass import ComponentClass
from FCOFFS.interfaces.interface import Interface
from FCOFFS.utilities.units import UnitValue

class OutputHandler:
    def __init__(self, objects: list, is_transient: bool, filename: str):
        self.__active = True
        self.__filename = filename
        self.__is_transient = is_transient
        self.__iter_counter = 0
        self.__time = 0 
        self._interface_muted = False
        self.__objects = objects
        self.__probes = []

        self.__full_df = pd.DataFrame({"Time": [], "Object": [], "Density (kg/m^3)": [], "Pressure (kg/ms^2)": [], "Velocity (m/s)": [], "Temperature (K)": [], "Mass Flow Rate (kg/s)": [], "Mass (kg)": [], "Dynamic Pressure (kg/ms^2)": []})
        self.__interfaces_df = pd.DataFrame({"Time": [], "Interface": [], "Density (kg/m^3)": [], "Pressure (kg/ms^2)": [], "Velocity (m/s)": [], "Temperature (K)": [], "Mass Flow Rate (kg/s)": [], "Dynamic Pressure (kg/ms^2)": []})
        if is_transient is True:
            self.__components_df = pd.DataFrame({"Time": [], "Component": [], "Mass (kg)": [], "Pressure (kg/ms^2)": [], "Density (kg/m^3)": [], "Temperature (K)": []})
        
    def _run(self, dt: float):
        if self.__iter_counter == 0:
            probe_dict = {"Time": []}
            for probe in self.__probes:
                 probe_dict[probe[2]] = []
            self.__probes_df = pd.DataFrame(probe_dict)
        if self.__active is False:
            return
        self.__add_to_log()
        if self.__is_transient is True:
                print(f"\nTransient Time Step: {self.__time}, Transient Iteration: {self.__iter_counter}")
        if self._interface_muted is False:
            self.__print_converged_state()
        self.__iter_counter += 1
        self.__time += dt

    def _finish(self):
        if self._interface_muted is True:
            self.__print_converged_state()
        if self.__is_transient is True:
            self.__transient_results()
        if self.__active is False:
            return
        self.__save_log()

    def deactivate(self):
        self.__active = False
        pass

    def __add_to_log(self): 
        for obj in self.__objects:
            if isinstance(obj, ComponentClass):
                self.__full_df = pd.concat([self.__full_df, pd.DataFrame({"Time": [self.__time], 
                                                                          "Object": [obj.name], 
                                                                          "Density (kg/m^3)": [obj.rho.value if isinstance(getattr(obj, "rho", 'N/A'), UnitValue) else "N/A"], 
                                                                          "Pressure (kg/ms^2)": [obj.p.value if isinstance(getattr(obj, "p", 'N/A'), UnitValue) else "N/A"], 
                                                                          "Velocity (m/s)": [obj.u.value if isinstance(getattr(obj, "u", 'N/A'), UnitValue) else "N/A"], 
                                                                          "Temperature (K)": [obj.T.value if isinstance(getattr(obj, "T", 'N/A'), UnitValue) else "N/A"], 
                                                                          "Mass Flow Rate (kg/s)": [obj.mdot.value if isinstance(getattr(obj, "mdot", 'N/A'), UnitValue) else "N/A"], 
                                                                          "Mass (kg)": [obj.mass.value if isinstance(getattr(obj, "mass", 'N/A'), UnitValue) else "N/A"], 
                                                                          "Dynamic Pressure (kg/ms^2)": [obj.q.value if isinstance(getattr(obj, "q", 'N/A'), UnitValue) else "N/A"]})], 
                                                                          ignore_index=True)
                if self.__is_transient is True:
                    self.__components_df = pd.concat([self.__components_df, pd.DataFrame({"Time": [self.__time], 
                                                                                          "Component": [obj.name], 
                                                                                          "Mass (kg)": [obj.mass.value if isinstance(getattr(obj, "mass", 'N/A'), UnitValue) else "N/A"], 
                                                                                          "Pressure (kg/ms^2)": [obj.p.value if isinstance(getattr(obj, "p", 'N/A'), UnitValue) else "N/A"], 
                                                                                          "Density (kg/m^3)": [obj.rho.value if isinstance(getattr(obj, "rho", 'N/A'), UnitValue) else "N/A"], 
                                                                                          "Temperature (K)": [obj.T.value if isinstance(getattr(obj, "T", 'N/A'), UnitValue) else "N/A"]})], 
                                                                                          ignore_index=True)
            if isinstance(obj, Interface):
                self.__full_df = pd.concat([self.__full_df, pd.DataFrame({"Time": [self.__time], 
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
            probe_dict[probe[2]] = [getattr(probe[0], probe[1])]
        self.__probes_df = pd.concat([self.__probes_df, pd.DataFrame(probe_dict)], ignore_index=True)

    def __print_converged_state(self):
        header = f"{'Name':<12} {'Rho':<20} {'Velocity':<20} {'Pressure':<20} {'Temp':<15} {'Mdot':<20} {'Area':<20} {'Fluid':<10}"
        
        output_string = header + "\n" + "-" * len(header) + "\n"
        
        for obj in self.__objects:
            if obj.type == 'interface':
                state = obj.state
                
                output_string += f"{obj.name:<12} {str(round(getattr(state, 'rho', 'N/A'), 4)):<20} {str(round(getattr(state, 'u', 'N/A'), 2)):<20} {str(round(getattr(state, 'p', 'N/A'), 4)):<20} {str(round(getattr(state, 'T', 'N/A'), 4)):<15} {str(round(getattr(state, 'mdot', 'N/A'), 4)):<20} {str(round(getattr(state, 'area', 'N/A'), 8)):<20} {getattr(state, 'fluid', 'N/A'):<10}\n"
            else:
                output_string += f"{obj.name:<12}\n"
        output_string = output_string[:-1]
        print("\n" + output_string + "\n")
        #return output_string # maybe needed in future
    
    def __transient_results(self):
       #Use saved datframe for this
        # result = [[]]
        # for _ in range(len(self.__probes)):
        #     result += [[]]
        # prev_time = -1 
        # for _, row in self.__probes_df.iterrows():
        #     if prev_time < row["Time"]:
        #         result[0].append(row["Time"])
        #         prev_time = result[0][-1]
        #     for ind2, probe in enumerate(self.__probes):
        #         if row["Object"] == probe[0]:
        #             result[ind2 + 1].append(row[probe[1]])

        # col_dict = {"Time" : result[0]}
        # for ind, probe in enumerate(self.__probes):
        #     col_dict[probe[0] + ' ' + probe[1]] = result[ind + 1]
        # transient_df = pd.DataFrame(col_dict)  
        # transient_df.to_csv(f"{self.__filename} Probes.csv", index=False) 
        # del transient_df       
        self.__probes_df.to_csv(f"{self.__filename} Probes.csv", index=False)

        header = f"{'Time':<10}"
        for probe in self.__probes:
            header += f" {(probe[2]):<25}"
        output_string = header + "\n" + "-" * len(header) + "\n"
        # for column in range(len(result[0])):
        #     for row in range(len(result)):
        #         if row == 0:
        #             output_string += f"{str(round(result[row][column], 6)):<10} "
        #         else:
        #             output_string += f"{str(round(result[row][column], 6)):<25} " 
        #     output_string += "\n"

        for _, row in self.__probes_df.iterrows():
            output_string += f"{str(round(row['Time'], 6)):<10} "
            for probe in self.__probes:
                output_string += f"{str(round(row[probe[2]].value, 6)):<25} "
            output_string += "\n"

                

        print("\n" + output_string + "\n")
        #return output_string maybe for future need
                    
    def __save_log(self):
        self.__full_df.to_csv(f"{self.__filename} Full Log.csv", index=False)
        self.__interfaces_df.to_csv(f"{self.__filename} Interface Log.csv", index=False)
        if self.__is_transient is True:
            self.__components_df.to_csv(f"{self.__filename} Component Log.csv", index=False)
        print("LOGS SAVED\n")
        self.__full_df = self.__full_df[0:0]
        self.__components_df = self.__components_df[0:0]
        self.__interfaces_df = self.__interfaces_df[0:0]

    def mute_steady_state(self):
        self._interface_muted = True

    def mute_transient_state(self):
        pass

    def print_state(self):
        self.__print_converged_state()

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
                    probe = [item[0], item[1], f"{item[0].name} {getattr(item[0], item[1]).get_dimension} ({getattr(item[0], item[1]).get_unit})"]
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
                
    def __check_object_exists(self, item):
        for obj in self.__objects:
            if obj == item[0]:
                if isinstance(obj, ComponentClass) and getattr(obj, item[1], 'N/A') != "N/A":
                    return True
                elif isinstance(obj, Interface) and getattr(obj.state, item[1], 'N/A') != "N/A":
                    return True
        return False
    
    


    



    
    