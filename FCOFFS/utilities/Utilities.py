'''
Description
'''

import numpy as np
    

def rms(arr):
    sum = 0
    for num in arr:
        sum += num**2
    sum /= len(arr)
    return np.sqrt(sum)