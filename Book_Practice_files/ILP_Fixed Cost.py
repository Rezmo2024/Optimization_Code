from pulp import LpMinimize, LpProblem, LpVariable, lpSum, value,LpStatus
# Define the coefficients for the objective function
costs_x = [20, 15, 12, 30]
costs_y = [500, 800, 1500, 450]
constraint_xy = [800, 400, 700, 600]
# Create the PuLP minimization problem
prob = LpProblem("Fixed Cost Problem", LpMinimize)
# Define the decision variables
x = [LpVariable(name=f"x_{i}", lowBound=0, cat='Continuous') for i in range(1, 5)]
y = [LpVariable(name=f"y_{i}", cat='Binary') for i in range(1, 5)]
# Define the objective function
prob += lpSum(costs_x[i-1] * x[i-1] + costs_y[i-1] * y[i-1] for i in range(1, 5)), "Total Cost"
# Add the constraints
prob += lpSum(x) >= 600, "Constraint_1"
for i in range(4):
    prob += x[i] <= constraint_xy[i] * y[i], f"Constraint_{i+2}"
# Define the relationship between x and y variables
for i in range(4):
    prob += x[i] >= 0, f"Non-Negative_x_{i+1}"
    prob += y[i] >= 0, f"Non-Negative_y_{i+1}"
    prob += x[i] <= constraint_xy[i] * y[i], f"Relationship_{i+1}"
# Solve the problem
prob.solve()
print(prob)
# Print the results
print(f'Status: {LpStatus[prob.status]}')
print(f"Optimal value of Z (Total Cost): {value(prob.objective)}")
print("Optimal Values:")
for i in range(4):
    print(f"x_{i+1}: {value(x[i])},    y_{i+1}: {value(y[i])}")