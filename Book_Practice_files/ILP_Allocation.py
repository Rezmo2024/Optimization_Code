from pulp import LpMinimize, LpProblem, LpVariable, lpSum, value,LpStatus
# Define the coefficients for the objective function
c = [[4, 5, 9], [3, 2, 4], [7, 5, 6]]  # Coefficients for x_ij
# Create the PuLP minimization problem
prob = LpProblem("Allocation", LpMinimize)
# Define the decision variables
x = {(i, j): LpVariable(name=f"x_{i}_{j}", cat='Binary') for i in range(1, 4) for j in range(1, 4)}
# Define the objective function
prob += lpSum(c[i-1][j-1] * x[i, j] for i in range(1, 4) for j in range(1, 4)), "Total Cost"
for i in range(1, 4):
    prob += lpSum(x[i, j] for j in range(1, 4)) == 1, f"Constraint_{i}"
for j in range(1,4):
    prob += lpSum(x[i, j] for i in range(1, 4)) == 1, f"_Constraint_{j}"
# Solve the problem
prob.solve()
# Print the results
print(prob)
print(f'Status: {LpStatus[prob.status]}')
print(f"Optimal value of Z (Total Cost): {value(prob.objective)}")
print("Optimal Values:")
for i in range(1, 4):
    for j in range(1, 4):
        print(f"x_{i}_{j}= {value(x[i, j])} |",end="")
    print("\n")