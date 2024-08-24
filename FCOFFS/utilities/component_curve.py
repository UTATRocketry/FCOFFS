
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
import os
import warnings

from units import UnitValue

class ComponentCurve:
    def __init__(self, data_filepath: str, x_unit: str, y_unit: str, interpolation_method: str = 'linear') -> None:
        '''
        Initializes a curve for a componeent given a dat file csv. Note it is expected that the xdata is in the first column and the ydata is in the second column

        Args:
            data_filepath (str): absolute filepath to the csv containing the curve data.
            x_unit (str): string representing the unit of the xaxis data.
            y_unit (str): string representing the unit of the yaxis data.
            interpolation_method (str): One of the follwoing methods ('linear', 'quadratic', 'cubic')

        Returns:
            None
        '''
        self.xunit = x_unit
        self.yunit = y_unit
        self.method = interpolation_method
        self.load_data(data_filepath)

    def load_data(self, filepath: str) -> None:
        '''
        Loads in data from given filepath csv
        '''
        if not os.path.exists(filepath):
            raise FileExistsError(f"Filepath {filepath} doesn't exist")
        
        data = pd.read_csv(filepath).to_numpy()
        print(data)
        x = []
        y = []
        for point in data:
            x.append(UnitValue.create_unit(self.xunit, float(point[0])).convert_base_metric())
            y.append(UnitValue.create_unit(self.yunit, float(point[1])).convert_base_metric())
            
        if len(x) != len(y): 
            raise IndexError("X and Y axes are not the same size")

        self.X = np.array(x)
        self.Y = np.array(y)
        self.X_Interpolator = interp1d(self.Y, self.X, kind=self.method, fill_value="extrapolate")
        self.Y_Interpolator = interp1d(self.X, self.Y, kind=self.method, fill_value="extrapolate")
        

    def y(self, x_value: float) -> float:
        '''
        Retunrs y value for given x value
        '''
        if x_value < self.X[0] or x_value > self.X[-1]:
            warnings.warn("Asking for value outside of provided data range")
        return self.Y_Interpolator(x_value)
    
    def x(self, y_value: float) -> float:
        '''
        Retunrs x value for given y value
        '''
        if y_value < self.Y[0] or y_value > self.Y[-1]:
            warnings.warn("Asking for value outside of provided data range")
        return self.X_Interpolator(y_value)
