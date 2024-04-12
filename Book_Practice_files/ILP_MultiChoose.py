from pulp import LpMinimize, LpProblem, LpVariable, lpSum, value,LpStatus
# Define the coefficients for the objective function
c = [[5, 2, 4, 2], [4, 8, 6, 5], [2, 5, 9, 8]]  # Coefficients for x_ij
h = [10, 14, 12]  # Coefficients for y_i
# Create the PuLP minimization problem
prob = LpProblem("Model", LpMinimize)
# Define the decision variables
x = {(i, j): LpVariable(name=f"x_{i}_{j}", cat='Binary') for i in range(1, 4) for j in range(1, 5)}
y = {i: LpVariable(name=f"y_{i}", cat='Binary') for i in range(1, 4)}
# Define the objective function
prob += lpSum(c[i-1][j-1] * x[i,j] for i in range(1, 4) for j in range(1, 5)) + lpSum(h[i-1] * y[i] for i in range(1, 4)), "Total Cost"
# Add constraints
for j in range(1, 5):
    prob += lpSum(x[i, j] for i in range(1, 4)) == 1, f"Constraint_1_{j}"
for i in range(1, 4):
    prob += lpSum(x[i, j] for j in range(1, 5)) <= 4 * y[i], f"Constraint_3_{i}"
# Define the relationship between x_ij and y_i variables
for i in range(1, 4):
    for j in range(1, 5):
        prob += y[i] >= x[i, j], f"Relationship_{i}_{j}"
# Solve the problem
prob.solve()
print(prob)
# Print the results
print(f'Status: {LpStatus[prob.status]}')
print(f"Optimal value of Z (Total Cost): {value(prob.objective)}")
print("Optimal Values:")
for i in range(1, 4):
    print(f"y_{i}: {value(y[i])} | ",end="")
    for j in range(1, 5):
        print(f"x_{i}_{j}= {value(x[i, j])} : ",end="")
    print("\n")