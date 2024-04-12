from pulp import LpMaximize, LpProblem, LpVariable, lpSum, value,LpStatus
Needs = [250, 100, 220, 400]
Capacity=[800, 500, 2000]
# Create the LP problem
model = LpProblem("Optimization Problem", LpMaximize)
# Define decision variables
x = {(i, j): LpVariable(f'x_{i}{j}', cat='Binary') for i in range(1, 5) for j in range(1, 4)}
# Objective function
model += lpSum(x[i, j] for i in range(1, 5) for j in range(1, 4))
# Constraints
for i in range(1, 5):
        model += lpSum(x[i, j] for j in range(1, 4)) <= 1
for j in range(1, 4):
    model += lpSum(Needs[i-1] * x[i, j] for i in range(1, 5)) <= Capacity[j-1]
# Solve the model
model.solve()
# Print Results
print(model)
print(f'Status: {LpStatus[model.status]}')
print(f"Optimal value of Z (Total Cost): {value(model.objective)}")
print("Optimal Values:")
for i in range(1, 5):
    for j in range(1, 4):
        if value(x[i, j])==1:
            print(f"x_{i}{j}:", value(x[i, j]))