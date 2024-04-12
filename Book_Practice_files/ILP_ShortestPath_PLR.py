import numpy as np
from scipy.optimize import minimize
# Define the graph
Undirected_Graph = {
    'A': {'B': 4, 'C': 11, 'D': 2},
    'B': {'C': 2, 'E': 1, 'A': 4},
    'C': {'D': 3, 'F': 2, 'A': 1, 'B': 2},
    'D': {'G': 7, 'A': 2, 'C': 3},
    'E': {'H': 3, 'F': 7, 'B': 1},
    'H': {'F': 5, 'E': 3, 'G': 4},
    'F': {'H': 5, 'G': 2, 'C': 2, 'E': 7},
    'G': {'H': 4, 'D': 7, 'F': 2},
}
Directed_Graph = {
    'A': {'B': 4, 'C': 11, 'D': 2},
    'B': {'C': 2, 'E': 1},
    'C': {'D': 3, 'F': 2},
    'D': {'G': 7},
    'E': {'H': 3, 'F': 7},
    'F': {'H': 6, 'G': 2},
    'G': {'H': 4},
    'H': {}
}
nodes = sorted(Directed_Graph.keys())
num_nodes = len(nodes)
adjacency_matrix = np.zeros((num_nodes, num_nodes))
node_indices = {node: i for i, node in enumerate(nodes)}
for node, neighbors in Directed_Graph.items():
    i = node_indices[node]
    for neighbor, weight in neighbors.items():
        j = node_indices[neighbor]
        adjacency_matrix[i, j] = weight
print(adjacency_matrix)
n = 64
a = adjacency_matrix
start = 'B'
end = 'H'
source_index=node_indices[start]
dest_index=node_indices[end]
# Define the decision variables
graph_list = []
for node, neighbors in Undirected_Graph.items():
    for neighbor, weight in neighbors.items():
        graph_list.append((node, neighbor, weight))
print(graph_list)
# Convert the graph to a dictionary of edges and weights
edge_weights = {}
for node, neighbors in Undirected_Graph.items():
    for neighbor, weight in neighbors.items():
        edge = node + neighbor
        edge_weights[edge] = weight
print(edge_weights)
# Define the objective function (example: squared distance function)
def objective_function(x):
    path_distance=np.prod([a[i % len(a)][i // len(a)] * x[i] for i in range(n)])
    return path_distance
def source_constraint(x, s):
    cons =(sum(x[i] for i in range(n) if (i//8)==s)-sum((x[i] for i in range(n) if i%8==s)))-1
    return cons
def dest_constraint(x, d):
    cons =(sum(x[i] for i in range(n) if (i//8)==d)-sum((x[i] for i in range(n) if i%8==d)))+1
    return cons
def intermediate_constraint(x,s, d):
    for j in range(n):
        cons1=0
        cons2=0        
        if (j//8)!=s and (j%8)!=s and (j//8)!=d and (j%8)!=d:
            cons1 +=(sum(x[i] for i in range(n) if (i//8)==j ))
        if (j//8)!=s and (j%8)!=s and (j//8)!=d and (j%8)!=d:
            cons2 +=sum((x[i] for i in range(n) if  (i%8)==j))            
    return cons1-cons2

# Initial guess
x0 = np.zeros(64)
bounds = [(0, 1) for _ in range(64)]

# Define the constraints
constraints = ({'type': 'eq', 'fun':lambda x:source_constraint(x, source_index)},
               {'type': 'eq', 'fun':lambda x:intermediate_constraint(x,source_index,dest_index)},
              {'type': 'eq', 'fun':lambda x:dest_constraint(x, dest_index)}
              )

# Perform nonlinear optimization
result = minimize(objective_function, x0, constraints=constraints, method='SLSQP',bounds=bounds)  # Example using SLSQP algorithm
# Print the result
print("Optimal solution (weights of edges):", result.x)
print("Optimal path distance:", result.fun)
sum=0
c=0
for i in range(len(result.x)):
    if result.x[i]>0:
        sum+=result.x[i]
        c=c+1
        print(f"x({i//8},{i%8})",result.x[i])
print("sum=",sum," count=",c)