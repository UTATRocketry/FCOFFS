import pandas as pd 
import warnings

from FCOFFS.components.componentClass import ComponentClass
from FCOFFS.interfaces.interface import Interface

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

        self.__full_df = pd.DataFrame({"Time": [], "Object": [], "Rho": [], "Pressure": [], "Velocity": [], "Temperature": [], "Mass Flow Rate": [], "Mass": [], "Dynamic Pressure": []})
        self.__interfaces_df = pd.DataFrame({"Time": [], "Interface": [], "Rho": [], "Pressure": [], "Velocity": [], "Temperature": [], "Mass Flow Rate": [], "Dynamic Pressure": []})
        if is_transient is True:
            self.__components_df = pd.DataFrame({"Time": [], "Component": [], "Mass": [], "Pressure": [], "Rho": [], "Temperature": []})
        
    def _run(self, dt: float):
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
                self.__full_df = pd.concat([self.__full_df, pd.DataFrame({"Time": [self.__time], "Object": [obj.name], "Rho": [getattr(obj, "rho", 'N/A')], "Pressure": [getattr(obj, "p", 'N/A')], "Velocity": [getattr(obj, "u", 'N/A')], "Temperature": [getattr(obj, "T", 'N/A')], "Mass Flow Rate": [getattr(obj, "mdot", 'N/A')], "Mass": [getattr(obj, "mass", 'N/A')], "Dynamic Pressure": [getattr(obj, "q", 'N/A')]})], ignore_index=True)
                if self.__is_transient is True:
                    self.__components_df = pd.concat([self.__components_df, pd.DataFrame({"Time": [self.__time], "Component": [obj.name], "Mass": [getattr(obj, "mass", 'N/A')], "Pressure": [getattr(obj, "p", 'N/A')], "Rho": [getattr(obj, "rho", 'N/A')], "Temperature": [getattr(obj, "T", 'N/A')]})], ignore_index=True)
            if isinstance(obj, Interface):
                self.__full_df = pd.concat([self.__full_df, pd.DataFrame({"Time": [self.__time], "Object": [obj.name], "Rho": [obj.state.rho], "Pressure": [obj.state.p], "Velocity": [obj.state.u], "Temperature": [obj.state.T], "Mass Flow Rate": [obj.state.mdot], "Mass": [getattr(obj, "mass", 'N/A')], "Dynamic Pressure": [obj.state.q]})], ignore_index=True)
                self.__interfaces_df = pd.concat([self.__interfaces_df, pd.DataFrame({"Time": [self.__time], "Interface": [obj.name], "Rho": [obj.state.rho], "Pressure": [obj.state.p], "Velocity": [obj.state.u], "Temperature": [obj.state.T], "Mass Flow Rate": [obj.state.mdot], "Dynamic Pressure": [obj.state.q]})], ignore_index=True)

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
       #USe saved datframe for this
        result = [[]]
        for _ in range(len(self.__probes)):
            result += [[]]
        prev_time = -1 
        for _, row in self.__full_df.iterrows():
            if prev_time < row["Time"]:
                result[0].append(row["Time"])
                prev_time = result[0][-1]
            for ind2, probe in enumerate(self.__probes):
                if row["Object"] == probe[0]:
                    result[ind2 + 1].append(row[probe[1]])

        col_dict = {"Time" : result[0]}
        for ind, probe in enumerate(self.__probes):
            col_dict[probe[0] + ' ' + probe[1]] = result[ind + 1]
        transient_df = pd.DataFrame(col_dict)  
        transient_df.to_csv(f"{self.__filename} Probes.csv", index=False) 
        del transient_df       

        header = f"{'Time':<10}"
        for probe in self.__probes:
            header += f" {(probe[0] + ' ' + probe[1]):<25}"
        output_string = header + "\n" + "-" * len(header) + "\n"
        for column in range(len(result[0])):
            for row in range(len(result)):
                if row == 0:
                    output_string += f"{str(round(result[row][column], 6)):<10} "
                else:
                    output_string += f"{str(round(result[row][column], 6)):<25} " 
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

    def add_probes(self, items: tuple|list[tuple]):
        corresponding = {"p": "Pressure", "rho": "Rho", "u": "Velocity", "T": "Temperature", "mdot": "Mass Flow Rate", "mass": "Mass", "q": "Dynamic Pressure"}
        if isinstance(items[0], tuple) or isinstance(items[0], list):
            for item in items:
                if self.__check_object_exists(item) is False:
                    warnings.warn(f"Object and or object attribute {item} does not exist! Skipping this probe.")
                    continue
                self.__probes.append([item[0], corresponding[item[1]]])
        else:
            if self.__check_object_exists(items) is False:
                    warnings.warn(f"Object and or object attribute {items} does not exist! Skipping this probe.")
            else:
                self.__probes.append([items[0], corresponding[items[1]]])

    def remove_probe(self, item: tuple):
        for ind in range(len(self.__probes)):
            if item[0] == self.__probes[ind][0] and item[1] == self.__probes[ind][1]:
                self.__probes.pop(ind)
                return
                
    def __check_object_exists(self, item):
        for obj in self.__objects:
            if obj.name == item[0]:
                if isinstance(obj, ComponentClass) and getattr(obj, item[1], 'N/A') != "N/A":
                    return True
                elif isinstance(obj, Interface) and getattr(obj.state, item[1], 'N/A') != "N/A":
                    return True
        return False
    
    


    



    
    