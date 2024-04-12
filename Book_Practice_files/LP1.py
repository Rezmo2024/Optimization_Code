from pulp import *
# Create the model
model = LpProblem(name="sample1", sense=LpMinimize)
# Initialize the decision variables
x1 = LpVariable(name="x1", lowBound=0)
x2 = LpVariable(name="x2", lowBound=0)
# Add the constraints to the model
model += (x1 + 2*x2 <= 40, "first_constraint")
model += (2*x1 - x2 >= 30, "second_constraint")
# Add the objective function to the model
obj_func = 3*x1 + 4*x2
model += obj_func
#print(model)
# Solve the problem
status = model.solve()
print(f"status: {model.status}, {LpStatus[model.status]}")
print(f"objective: {model.objective.value()}")
for var in model.variables():
     print(f"{var.name}: {var.value()}")
for name, constraint in model.constraints.items():
     print(f"{name}: {constraint.value()}")