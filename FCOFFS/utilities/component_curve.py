
import numpy as np # maybe remove
import pandas as pd
from scipy.interpolate import interp1d, RegularGridInterpolator, LinearNDInterpolator, NearestNDInterpolator
import warnings
import os

from FCOFFS.utilities.units import UnitValue

class ComponentCurve: # How to make data striclty increasing or decreasing, write algo 

    ALLOWED_METHODS = {True: {1:{"linear": interp1d, "nearest": interp1d, "nearest-up": interp1d, "zero": interp1d, "slinear": interp1d, "quadratic": interp1d, "cubic": interp1d, "previous": interp1d, "next": interp1d},
                        "N":{"linear": RegularGridInterpolator, "nearest": RegularGridInterpolator, "slinear": RegularGridInterpolator, "cubic": RegularGridInterpolator, "quintic": RegularGridInterpolator, "pchip": RegularGridInterpolator}},
                   False: {"N": {"linear": LinearNDInterpolator, "nearest": NearestNDInterpolator}}
                  }

    def __init__(self, data_filepath: str, strictly_inc_dec: bool, interpolation_method: str = 'linear') -> None: 
        '''
        Initializes a curve for a componeent given a dat file csv. Note it is expected to have a first row defining "Inputs" and "Outputs" then the next row defines each columns units then enter the data.
        Extrapolation is only availale for striclty increasing or decreasing data sets else NaN is typicaly returned for out of domain values.

        Args:
            data_filepath (str): absolute filepath to the csv containing the curve data.
            strictly_inc_dec (bool): Whether or not the data in the CSV is strictly decreasing or increaing. If it is then enter True of not enter False.
            interpolation_method (str): One of the follwoing methods ("linear", “nearest”, “cubic”)

        Returns:
            None
        '''

        self.__method = interpolation_method.lower()
        self.load_data(data_filepath, strictly_inc_dec)

    def load_data(self, filepath: str, strictly_inc_dec: bool) -> None:
        '''
        Loads in data from given filepath csv, and generates interpolator whihc willl be used when calling the class to give output values.
        
        Args:
            data_filepath (str): absolute filepath to the csv containing the curve data.
            strictly_inc_dec (bool): Whether or not the data in the CSV is strictly decreasing or increaing. If it is then enter True of not enter False.

        Returns:
            None
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
        
        self.__ordered = strictly_inc_dec
        if self.__ordered == True and len(self.__input_units) == 1:
            self.__N = 1
        else:
            self.__N = "N"

        for i in range(len(self.__points) - 1):
            if len(self.__points[i]) != len(self.__points[i+1]):
                raise IndexError("Inputs are not the same size")
             
        self.set_method(self.__method)

    def set_method(self, interpolation_method: str) -> None: 
        '''
        Set/Change the interpolation method.
        '''
        interp_func = self.method_exists(interpolation_method)
        if interp_func is False:
            raise Exception(f"Invalid method {interpolation_method} for interpolation of {self.__N} dimensions and ")
        
        self.__method = interpolation_method
        if self.__ordered is True:
            self.Interpolator = interp_func(self.__points, self.__output_values, self.__method, fill_value="extrapolate")
        else: 
            self.Interpolator = interp_func(self.__points, self.__output_values)

    def method_exists(self, interp_method):    
        if interp_method in self.ALLOWED_METHODS[self.__ordered][self.__N]:
            return self.ALLOWED_METHODS[self.__ordered][self.__N][interp_method]
        else:
            return False
        
    def __call__(self, inputs: list[UnitValue]) -> UnitValue: # could make this work with multiple inputs at once but don't see the need
        '''
        Returns interpolated output value for given inputs
        '''
        if len(inputs) != len(self.__points[0]):
            raise IndexError(f"Incorrect number of inputs, should be: {len(self.inputs)}")
        inputs = [input.copy() for input in inputs]
        for ind, input in enumerate(inputs): 
            input.to(self.__input_units[ind])
        return (UnitValue.create_unit(self.__output_unit, self.Interpolator(inputs)[0])).convert_base_metric()
    
    @property
    def points(self) -> list:
        return self.__points

    @property
    def units(self) -> list:
        return {"Inputs": [self.__input_units], "Output": self.__output_unit}
    
    @property
    def outputs(self) -> list:
        return self.__output_values
    
    @property
    def method(self) -> str:
        return self.__method

if __name__ == "__main__": 
    curve = ComponentCurve(os.path.join(os.getcwd(), 'FCOFFS', 'utilities', 'test.csv'), False)
    print(curve([UnitValue.create_unit("psi", 25), UnitValue.create_unit("psi", 500), UnitValue.create_unit("ft^3/min", 0.02001990592322454)]))
    
