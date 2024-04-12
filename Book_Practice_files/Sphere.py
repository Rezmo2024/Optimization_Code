import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# Define the sphere function
def sphere(x, y):
    return x**2 + y**2
    

# Generate a grid of points to plot
x = np.linspace(-5, 5, 101)
X, Y = np.meshgrid(x, x)
Z = sphere(X, Y)

# Plot the function in 3D
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='CMRmap')

# Set labels and title
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Sphere Function')

plt.show()