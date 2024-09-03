
import numpy as np # maybe remove
import pandas as pd
from scipy.interpolate import LinearNDInterpolator, NearestNDInterpolator, CloughTocher2DInterpolator
import os
import warnings

from FCOFFS.utilities.units import UnitValue

class ComponentCurve: # How to make data striclty increasing or decreasing? Maybe have user enter number of dimensions

    ALLOWED_METHODS = ['linear', 'nearest', 'cubic']

    def __init__(self, data_filepath: str, interpolation_method: str = 'linear') -> None: #user define dimension of inputs #Spline
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

        try:
            self.__output_values = pd.read_csv(filepath, usecols= ["Output"]).to_numpy() # extract output column and then delete
            self.__output_unit = self.__output_values[0][0]
            self.__output_values = np.delete(self.__output_values, 0)
            self.__points = pd.read_csv(filepath) #extract everything and manually drop the Output column so only the Input columns remain  
            self.__points.drop("Output", axis=1, inplace=True)
            self.__points = self.__points.to_numpy()
            self.__input_units = self.__points[0]
            self.__points = np.delete(self.__points, 0, axis=0) 
        except Exception as e:
            raise Exception(f"CSV provided does not follow expected format. First row should indicate input or output, second row should indicate units, and the rest is data. | {e}")
        
        for i in range(len(self.__points) - 1):
            if len(self.__points[i]) != len(self.__points[i+1]):
                raise IndexError("Inputs are not the same size")
        
        if self.__method == "linear":
            self.Interpolator = LinearNDInterpolator(self.__points, self.__output_values)  
        elif self.__method == "nearest":
            self.Interpolator = NearestNDInterpolator(self.__points, self.__output_values)
        elif self.__method == "cubic":
             self.Interpolator = CloughTocher2DInterpolator(self.__points, self.__output_values) 


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
        
    def __call__(self, inputs: list[UnitValue]) -> UnitValue: # could make this work with multiple inputs at once but don't see the need
        '''
        Returns interpolated output value for given inputs
        '''
        if len(inputs) != len(self.__points[0]):
            raise IndexError(f"Incorrect number of inputs, should be: {len(self.inputs)}")
        for ind, input in enumerate(inputs):
            input.to(self.__input_units[ind])
        return UnitValue.create_unit(self.__output_unit, self.Interpolator(inputs)[0])
    
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
    print(curve([UnitValue.create_unit("psi", 25), UnitValue.create_unit("psi", 500), UnitValue.create_unit("ft^3/min", 0.02001990592322454)]))
    
