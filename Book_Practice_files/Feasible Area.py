import numpy as np
import matplotlib.pyplot as plt

# Define the constraints
x = np.linspace(0, 200, 800)
y1 = (40 - x) / 2
y2 = (2 * x - 30) / 1

# Create a meshgrid for filling the feasible region
X, Y = np.meshgrid(x, x)
Z = np.zeros_like(X)
Z[(x + 2*Y <= 40) & (2*x - Y <= 30)] = 1

# Plot the lines defined by the constraints
plt.plot(x, y1, label='x1 + 2x2 <= 40')
plt.plot(x, y2, label='2x1 - x2 <= 30')

# Fill the feasible region with green color
#plt.contourf(X, Y, Z, colors=['green'], alpha=0.5)

# Set labels and legend
plt.xlabel('x1')
plt.ylabel('x2')
plt.title('Feasible Region of Linear Inequalities')
plt.legend()

# Set limits and display the plot
plt.xlim(0, 30)
plt.ylim(0, 30)
plt.xlabel('x1', fontsize=12)
plt.ylabel('x2', fontsize=12)
plt.grid(True)
plt.show()