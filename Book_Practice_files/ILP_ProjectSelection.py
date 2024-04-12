from pulp import LpMaximize, LpProblem, LpVariable, lpSum, value,LpStatus
# Define the coefficients for the objective function
costs = [250, 300, 160, 500]
# Define the coefficients for the constraints
constraints = [[10, 14, 18, 12],
               [18, 15, 20, 14],
               [21, 17, 25, 17]]
# Define the RHS values for the constraints
rhs_values = [40, 60, 65]
# Create the PuLP maximization problem
prob = LpProblem("Project_Selection", LpMaximize)
# Define the decision variables
x = [LpVariable(name=f"x_{i}", cat='Binary') for i in range(1, 5)]
# Define the objective function
prob += lpSum(costs[i] * x[i] for i in range(4)), "Total Cost"
# Add the constraints
for j in range(3):
    prob += lpSum(constraints[j][i] * x[i] for i in range(4)) <= rhs_values[j], f"Constraint_{j+1}"
# Solve the problem
prob.solve()
# Print the results
print(prob)
print(f'Status: {LpStatus[prob.status]}')
print(f"Optimal value of Z (Total Cost): {value(prob.objective)}")
print("Project Selection:")
for i in range(4):
    print(f"Project {i+1}: {value(x[i])}")