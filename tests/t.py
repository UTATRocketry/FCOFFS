import numpy as np
import matplotlib.pyplot as plt

# Define constants
L = 1.0       # Define L (change as needed)
rho_0 = 1.0   # Define base density (change as needed)
n = 0.3      # Some value between 0 and 1

# Define the density function
def density(x, y, L, rho_0, n):
    return rho_0 / ((1 - n) + (2 * n * y / L) + (2 * x * n**2 / L))

def strain(a1, a2, L, n):
    e11 = -n / 2 + (n / L) * a2
    e22 = n / 2 - (n / L) * a2
    e12 = ((n / L) * a1 - n/2)
    
    return np.sqrt((2/3) * (e11**2 + e22**2 + 2 * e12**2))

# Generate a grid over the square domain [0, L] x [0, L]
x = np.linspace(0, L, 100)
y = np.linspace(0, L, 100)
X, Y = np.meshgrid(x, y)
Z = density(X, Y, L, rho_0, n)
Z2 = strain(X, Y, L, n)

# Create contour plot
plt.figure(figsize=(6, 5))
contour = plt.contourf(X, Y, Z, levels=50, cmap="plasma")
plt.colorbar(contour, label=r"$\rho(x, y)$")
plt.xlabel("$x$")
plt.ylabel("$y$")
plt.title("Contour Plot of Density")
plt.show()

plt.figure(figsize=(6, 5))
contour = plt.contourf(X, Y, Z2, levels=50, cmap="plasma")
plt.colorbar(contour, label=r"$\epsilon(x, y)$")
plt.xlabel("$x$")
plt.ylabel("$y$")
plt.title("Contour Plot of Strain")
plt.show()

def inverse_transform(x1, x2, L, n):
    """Solves for a1 and a2 given x1 and x2 using the inverse transformation."""
    # Coefficients of quadratic equation in a1
    A = (2 * n**2) / L
    B = (1 - n) + (2 * n / L) * x2 - 2 * n**2
    C = -x1

    # Solve for a1 using quadratic formula
    discriminant = B**2 - 4 * A * C
    if discriminant < 0:
        return None, None  # No real solution
    a1 = (-B + np.sqrt(discriminant)) / (2 * A)  # Choose positive root

    # Solve for a2
    a2 = x2 + n * a1 - n * L
    return a1, a2

def equivalent_strain(x1, x2, L, n):
    """Computes equivalent strain in terms of x1 and x2."""
    a1, a2 = inverse_transform(x1, x2, L, n)
    if a1 is None or a2 is None:
        return np.nan  # Undefined for this point

    # Compute deviatoric strain components
    e11 = -n / 2 + (n / L) * a2
    e22 = n / 2 - (n / L) * a2
    e12 = 0.5 * ((2 * n / L) * a1 - n)

    # Compute von Mises equivalent strain
    epsilon_eq = np.sqrt((2/3) * (e11**2 + e22**2 + 2 * e12**2))
    return epsilon_eq

def density(x1, x2, L, n, rho_0):
    """Computes new density in terms of x1 and x2."""
    a1, a2 = inverse_transform(x1, x2, L, n)
    if a1 is None or a2 is None:
        return np.nan  # Undefined for this point

    rho_new = rho_0 / ((1 - n) + (2 * n / L) * a2 + (2 * n**2 / L) * a1)
    return rho_new
