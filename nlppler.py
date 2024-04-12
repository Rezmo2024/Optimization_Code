import numpy as np
from scipy.optimize import minimize, LinearConstraint

# Define the graph
Graph = {
    'A': {'B': 4, 'C': 1, 'D': 2},
    'B': {'C': 2, 'E': 1,'A': 4},
    'C': {'D': 3, 'F': 2, 'A': 1,'B': 2},
    'D': {'G': 7, 'A': 2,'C': 3},
    'E': {'H': 3, 'F': 7, 'B': 1},
    'H': {'F': 5, 'E': 3, 'G': 4},
    'F': {'H': 5, 'G': 2,'C': 2, 'E': 7},
    'G': {'H': 4, 'D': 7, 'F': 2 },
}

# Define the source and destination
source = 'A'
destination = 'H'

# Create the adjacency matrix
nodes = list(Graph.keys())
n = len(nodes)
a = np.zeros((n, n))
for i, node_i in enumerate(nodes):
    for j, node_j in enumerate(nodes):
        if node_j in Graph[node_i]:
            a[i, j] = Graph[node_i][node_j]

# Define the objective function
def objective(x):
    return np.sum(a * x.reshape(n, n))

# Define the linear constraints
source_idx = nodes.index(source)
A_source = np.zeros((1, n * n))
A_source[0, source_idx * n:(source_idx + 1) * n] = 1
A_source[0, (n - 1) * n] = 0
lb_source = np.array([1])
ub_source = np.array([1])
source_constraint = LinearConstraint(A_source, lb_source, ub_source)

A_other = np.zeros((n - 2, n * n))
for i, node_i in enumerate(nodes):
    if node_i != source and node_i != destination:
        A_other[i - 1, i * n:(i + 1) * n] = 1
        A_other[i - 1, (n - 1) * n + i] = -1
lb_other = np.zeros(n - 2)
ub_other = np.zeros(n - 2)
other_constraint = LinearConstraint(A_other, lb_other, ub_other)

# Solve the optimization problem
x0 = np.zeros(n * n)
res = minimize(objective, x0, method='SLSQP', constraints=[source_constraint, other_constraint], bounds=[(0, 1)] * (n * n))

# Print the results
print(f"Optimal value of z: {res.fun}")
print("Optimal values of x:")
for i, node_i in enumerate(nodes):
    for j, node_j in enumerate(nodes):
        print(f"x[{node_i}, {node_j}] = {res.x[i * n + j]}")