
import numpy as np # maybe remove
import pandas as pd
from scipy.interpolate import LinearNDInterpolator, NearestNDInterpolator, CloughTocher2DInterpolator
import os
import warnings

from units import UnitValue

class ComponentCurve: # How to make data striclty increasing or decreasing? Maybe have user enter number of dimensions

    ALLOWED_METHODS = ['linear', 'nearest', 'cubic']

    def __init__(self, data_filepath: str, interpolation_method: str = 'linear') -> None:
        '''
        Initializes a curve for a componeent given a dat file csv. Note it is expected that the xdata is in the first column and the ydata is in the second column

        Args:
            data_filepath (str): absolute filepath to the csv containing the curve data.
            x_unit (str): string representing the unit of the xaxis data.
            y_unit (str): string representing the unit of the yaxis data.
            interpolation_method (str): One of the follwoing methods ("linear", “nearest”, “cubic”)

        Returns:
            None
        '''
        if interpolation_method not in self.ALLOWED_METHODS:
            raise Exception(f"Invalid method {interpolation_method} for interpolation")
        
        self.__method = interpolation_method
        self.load_data(data_filepath)

    def load_data(self, filepath: str) -> None:
        '''
        Loads in data from given filepath csv, and generates interpolator whihc willl be used when calling the class to give output values.
        '''
        if not os.path.exists(filepath):
            raise FileExistsError(f"Filepath {filepath} doesn't exist")
        
        self.__inputs = []
        self.__units = []
        self.__output_values = []
        data = pd.read_csv(filepath).to_numpy()
        
        self.__output_ind = None
        try: # Allows output column to be anywhere in csv
            for ind, string in enumerate(data[0]):
                if string.lower() == "input":
                    self.__inputs.append([])
                elif string.lower() == "output":
                    if self.__output_ind is None:
                        self.__output_ind = ind
                    else:
                        raise Exception("To many outputs must only be one")
            for unit in data[1]:
                self.__units.append(unit)
        except Exception as e:
            raise Exception(f"CSV provided does not follow expected format. First row should indicate input or output, second row should indicate units, and the rest is data. | {e}")

        for point in data[2:]:
            input_ind = 0
            for ind, val in enumerate(point):
                if ind == self.__output_ind:
                    self.__output_values.append(UnitValue.create_unit(self.__units[ind], float(val)).convert_base_metric())
                else:
                    self.__inputs[input_ind].append(UnitValue.create_unit(self.__units[ind], float(val)).convert_base_metric())
                    input_ind += 1
            
        for i in range(len(self.__inputs) - 1):
            if len(self.__inputs[i]) != len(self.__inputs[i+1]):
                raise IndexError("X and Y axes are not the same size")
        
        self.__points = []
        for i in range(len(self.__inputs[0])):
            point = []
            for input in self.__inputs:
                point.append(input[i])
            self.__points.append(point)

        if self.__method == "linear":
            self.Interpolator = LinearNDInterpolator(self.__points, self.__output_values)  
        elif self.__method == "nearest":
            NearestNDInterpolator(self.__points, self.__output_values)
        elif self.__method == "cubic":
            CloughTocher2DInterpolator(self.__points, self.__output_values) 

    def set_method(self, interpolation_method: str) -> None: 
        '''
        Set/Change the interpolation method.
        '''
        if interpolation_method not in self.ALLOWED_METHODS:
            raise Exception(f"Invalid method {interpolation_method} for interpolation")
        
        self.__method = interpolation_method
        if self.__method == "linear":
            LinearNDInterpolator(self.__points, self.__output_values) 
        elif self.__method == "nearest":
            NearestNDInterpolator(self.__points, self.__output_values)
        elif self.__method == "cubic":
            CloughTocher2DInterpolator(self.__points, self.__output_values)
        
    def __call__(self, inputs: tuple) -> UnitValue: # could make this work with multiple inputs at once but don't see the need
        '''
        Returns interpolated output value for given inputs
        '''
        if len(inputs) != len(self.__inputs):
            raise IndexError(f"Incorrect number of inputs, should be: {len(self.inputs)}")
        for ind, input in enumerate(self.__inputs):
            if inputs[ind] < min(input) or inputs[ind] > max(input):
                warnings.warn("Asking for value outside of provided data range")
        return UnitValue.create_unit(self.__units[self.__output_ind], self.Interpolator(inputs)[0])
    
    @property
    def points(self) -> list:
        return self.__points

    @property
    def units(self) -> list:
        return self.__units
    
    @property
    def outputs(self) -> list:
        return self.__output_values

if __name__ == "__main__": 
    curve = ComponentCurve(os.path.join(os.getcwd(), 'FCOFFS', 'utilities', 'test.csv'))
    print(curve([172369, 3447380, 0.002]))
    
