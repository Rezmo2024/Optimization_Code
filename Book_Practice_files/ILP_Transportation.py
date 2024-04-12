from pulp import LpMinimize, LpProblem, LpVariable, lpSum, value,LpStatus
# Define the coefficients for the objective function
c = [[3, 5, 0], [7, 2, 0], [4, 3, 0], [9, 2, 0]]  # Coefficients for x_ij
# Create the PuLP minimization problem
prob = LpProblem("Model", LpMinimize)
# Define the decision variables
x = {(i, j): LpVariable(name=f"x_{i}_{j}", lowBound=0, cat='Continuous') for i in range(1, 5) for j in range(1, 4)}
# Define the objective function
prob += lpSum(c[i-1][j-1] * x[i, j] for i in range(1, 5) for j in range(1, 4)), "Total Cost"
# Add constraints
constraints_m = {
    1: 40,
    2: 30,
    3: 80,
    4: 50
}
constraints_n = {
    1: 70,
    2: 90,
    3: 40
}
for i in range(1, 5):
    prob += lpSum(x[i, j] for j in range(1, 4)) == constraints_m[i], f"Constraint_{i}"
for j in range(1,4):
    prob += lpSum(x[i, j] for i in range(1, 5)) == constraints_n[j], f"_Constraint_{j}"
# Solve the problem
prob.solve()
print(prob)
# Print the results
print(f'Status: {LpStatus[prob.status]}')
print(f"Optimal value of Z (Total Cost): {value(prob.objective)}")
print("Optimal Values:")
for i in range(1, 5):
    for j in range(1, 4):
        print(f"x_{i}_{j}= {value(x[i, j])} | ",end="")
    print("\n")