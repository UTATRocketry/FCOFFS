
import numpy as np
    
def rms(arr):
    sum = 0
    for num in arr:
        sum += num**2
    sum /= len(arr)
    return np.sqrt(sum)

def relaxation(f, initial_guess: float): 
    '''takes in callable f, x = f(x)'''
    tolerance = 1e-6
    guess = initial_guess
    step = 0 #keeps track of number of iterations
    f_x = f(guess)
    while abs(f_x - guess) > tolerance:
        guess = f_x #successive approximation step
        step += 1
        f_x = f(guess)
        if step > 100:
            raise Exception(f"Could not converge on root of function. Last guess was: {guess}")
    root = round(guess,3)
    return root

def Newtons_Method(f,fprime):
    tolerance = 1e-5
    x_approx = 2 #initial guess
    step = 0 #to keep track of number of iterations
    while f(x_approx) > tolerance:
        #estimate the successive value
        x_approx = x_approx - f(x_approx) / fprime(x_approx)
        step += 1
        if step > 1000:
            raise Exception(f"Could not converge on root of function. Last guess was: {x_approx}")
    return x_approx
