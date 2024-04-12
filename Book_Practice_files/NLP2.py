from scipy.optimize import minimize
from numdifftools import Jacobian,Hessian
import time
# Objective function
fun = lambda x: 3*x[0]**2 - 2*x[1]**2 
# Jacobian
fun_Jac = lambda x: Jacobian(lambda x: fun(x))(x).ravel()
# Hessian
fun_Hess = lambda x: Hessian(lambda x: fun(x))(x) 
# constraints
cons = ({'type': 'ineq', 'fun': lambda x: 4*x[0]*x[0] - x[1]-3.},
        {'type': 'ineq', 'fun': lambda x: -x[0] - x[1]-2},        
        {'type': 'eq', 'fun': lambda x: 2*x[0] + 3*x[1]*x[1] - 2.},
        )
# bounds, if any, e.g. x1 and x2 have to be positive
bnds = ((4, 6), (2, None))
# initial guess
x0 = (10,10) # feasible initian point
# Method SLSQP uses Sequential Least SQuares Programming to minimize a function 
# of several variables with any combination of bounds, equality and inequality constraints. 
res = minimize(fun, x0, method='SLSQP', bounds=bnds, constraints=cons)
print(res)
print("optimal value p*", res.fun)
print("optimal var: x1 = ", res.x[0], " x2 = ", res.x[1])
# Using Jacobian
res2 = minimize(fun, x0, bounds=bnds, constraints=cons,jac=fun_Jac)
print('\n',res2)
print("JAC: optimal value p*", res2.fun)
print("JAC: optimal var: x1 = ", res2.x[0], " x2 = ", res2.x[1])
# Using Hessian
res = minimize(fun, x0, bounds=bnds, constraints=cons,  hess=fun_Hess)
print('\n',res)
print("HESS: optimal value p*", res.fun)
print("HESS: optimal var: x = ", res.x)
## Plots
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
fig = plt.figure()
f = lambda x: 3*x[0]**2 - 2*x[1]**2 
g = lambda x: 4*x[0]*x[0] - x[1]-3. 
t = lambda x: -x[0] - x[1]-2. 
w = lambda x: 2*x[0] + 3*x[1]*x[1] - 2. 
x = np.linspace(-100,100)
y = np.linspace(-100,100)
X, Y = np.meshgrid(x, y)
F = f([X,Y])
G = g([X,Y])
T = t([X,Y])
W = w([X,Y])
fig = plt.figure()
ax = plt.axes(projection='3d')
s1=ax.plot_surface(X, Y, F,  alpha=.8,color='green')
s2=ax.plot_surface(X, Y, G, color=(0.1, 0.2, 0.5, 0.5))
s2=ax.plot_surface(X, Y, T, color='blue')
s2=ax.plot_surface(X, Y, W, color='cyan')
ax.set_xlabel('x1')
ax.set_ylabel('x2')
ax.set_zlabel('f')
#ax.view_init(50, 135)
plt.plot(res2.x[0],res2.x[1], res2.fun, marker='o', markersize=15, color="Black")
#plt.plot( res2.fun, marker='o', markersize=10, color="red")
plt.show()
