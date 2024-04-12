import numpy as np
import matplotlib.pyplot as plt

# Define the constraints
x = np.linspace(-5, 200, 800)
y1 = (12 - 2*x)/3
y2 = (5 - x )


 

# Create a meshgrid for filling the feasible region
X, Y = np.meshgrid(x, x)
Z = np.zeros_like(X)

# Plot the lines defined by the constraints
plt.plot(x, y1, label='2x1 + 3x2 <= 12')
plt.plot(x, y2, label='X1 + x2 <= 5')
plt.plot(x, y2, label=' x2 <= 3')


# Fill the feasible region with green color
#plt.contourf(X, Y, Z, colors=['green'], alpha=0.5)

# Set labels and legend
plt.xlabel('x1')
plt.ylabel('x2')
plt.title('Feasible Region of Linear Inequalities')
plt.legend()

# Set limits and display the plot
plt.xlim(0, 6.5)
plt.ylim(0, 5.5)
plt.xlabel('x1', fontsize=12)
plt.ylabel('x2', fontsize=12)
plt.grid(True)
plt.show()