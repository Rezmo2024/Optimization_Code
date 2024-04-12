import cvxpy as cp
# Create two scalar optimization variables.
x = cp.Variable(3, name='x')
# Objective Function
f0 = x[0]**2 - 3*x[1]+2*x[2]
obj = cp.Minimize(f0)
# Constraints
f1 = x[0]+x[2]
f2 = x[0]-x[1]
f3 = 2*x[1]+3*x[2]
constraints = [f1<=3.,f2>=2.,f3==12.]
# Form and solve problem.
prob = cp.Problem(obj, constraints)
print("solve", prob.solve())  # Returns the optimal value.
print("status:", prob.status)
print("optimal value p* = ", prob.value)
print("optimal var: x = ", x.value)
print("optimal dual variables lambda = ", constraints[0].dual_value, constraints[1].dual_value, constraints[1].dual_value)

