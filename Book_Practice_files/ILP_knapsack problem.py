from pulp import LpMaximize, LpProblem, LpVariable, lpSum, value,LpStatus

# Define the coefficients for the objective function
costs = [2000, 2500, 1500, 400, 800]

# Define the coefficients for the constraints
constraints = [[500, 800, 950, 700, 320]]

# Define the RHS values for the constraints
rhs_values = [3000]

# Create the PuLP maximization problem
prob = LpProblem("knapsack problem", LpMaximize)

# Define the decision variables
x = [LpVariable(name=f"x_{i}", cat='Binary') for i in range(1, 6)]

# Define the objective function
prob += lpSum(costs[i] * x[i] for i in range(5)), "Total Profit"

# Add the constraints
for j in range(1):
    prob += lpSum(constraints[j][i] * x[i] for i in range(5)) <= rhs_values[j], f"Constraint_{j+1}"

# Solve the problem
prob.solve()
print(prob)
# Print the results
print(f'Status: {LpStatus[prob.status]}')
print(f"Optimal value of Z (Total Profit): {value(prob.objective)}")
print("Organization Selection:")
for i in range(5):
    print(f"Organization {i+1}: {value(x[i])}")