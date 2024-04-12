import numpy as np
import matplotlib.pyplot as plt

# Define the constraints
x = np.linspace(0, 200, 800)
y1 = (2 - x)/2
y2 = -( 3-x )/2 
y3 = (5- 2*x)/3
y4 = ( 2-x) 
y5 = (3 - 3*x)
 

# Create a meshgrid for filling the feasible region
X, Y = np.meshgrid(x, x)
Z = np.zeros_like(X)

# Plot the lines defined by the constraints
plt.plot(x, y1, label='y1 + 2y2 <= 2')
plt.plot(x, y2, label='y1 - 2y2 <= 3')
plt.plot(x, y3, label='2y1 + 3y2 <= 5')
plt.plot(x, y4, label='y1 + y2 <= 2')
plt.plot(x, y5, label='3y1 + y2 <= 3')

# Fill the feasible region with green color
#plt.contourf(X, Y, Z, colors=['green'], alpha=0.5)

# Set labels and legend
plt.xlabel('y1')
plt.ylabel('y2')
plt.title('Feasible Region of Linear Inequalities')
plt.legend()

# Set limits and display the plot
plt.xlim(-1, 5)
plt.ylim(-1, 5)
plt.xlabel('y1', fontsize=12)
plt.ylabel('y2', fontsize=12)
plt.grid(True)
plt.show()