from pulp import *
# Create the model
model = LpProblem(name="sample", sense=LpMaximize)
# Initialize the decision variables
x1 = LpVariable(name="x1", lowBound=8 , cat=LpInteger)
x2 = LpVariable(name="x2", lowBound=5, upBound=10 ,cat=LpContinuous)
x3 = LpVariable(name="x3", cat=LpBinary) #x3 = LpVariable(name="x3", lowBound=0, upBound=1,cat=LpInteger )
# Add the constraints to the model
model += (x1 + x2 >= 40, "first_constraint")
model += (2*x1 + x3 <= 80, "second_constraint")
model += (2*x1 - 3*x2+x3 == 31, "third_constraint")
# Add the objective function to the model
obj_func = 3*x1 + 4*x2+ 5*x3
model += obj_func
# Solve the problem
status = model.solve()
print(f"status: {model.status}, {LpStatus[model.status]}")
print(f"objective: {model.objective.value()}")
for var in model.variables():
     print(f"{var.name}: {var.value()}")
for name, constraint in model.constraints.items():
     print(f"{name}: {constraint.value()}")