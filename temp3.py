import numpy as np
from scipy.optimize import LinearConstraint, minimize

Undirected_Graph = {
    'A': {'B': 4, 'C': 1, 'D': 2},
    'B': {'C': 2, 'E': 1, 'A': 4},
    'C': {'D': 3, 'F': 2, 'A': 1, 'B': 2},
    'D': {'G': 7, 'A': 2, 'C': 3},
    'E': {'H': 3, 'F': 7, 'B': 1},
    'H': {'F': 5, 'E': 3, 'G': 4},
    'F': {'H': 5, 'G': 2, 'C': 2, 'E': 7},
    'G': {'H': 4, 'D': 7, 'F': 2},
}

source = 'A'
destination = 'G'

nodes = sorted(Undirected_Graph.keys())
num_nodes = len(nodes)
adjacency_matrix = np.zeros((num_nodes, num_nodes))

node_indices = {node: i for i, node in enumerate(nodes)}

for node, neighbors in Undirected_Graph.items():
    i = node_indices[node]
    for neighbor, weight in neighbors.items():
        j = node_indices[neighbor]
        adjacency_matrix[i, j] = weight

# Objective function
def objective_function(x):
    return sum(adjacency_matrix[i][j] * x[i * num_nodes + j] for i in range(num_nodes) for j in range(num_nodes))

# Constraints
constraints = []
coef = np.zeros((num_nodes, num_nodes))

# Linear constraint for source node
source_index = node_indices[source]
for j in range(num_nodes):
    if adjacency_matrix[source_index, j]>0:
        coef[source_index, j] = 1
    if adjacency_matrix[j, source_index]>0:
        coef[j, source_index] = -1
constraints.append(LinearConstraint(coef.flatten(), 1, 1))

print(coef)
# Linear constraints for other nodes
coef = np.zeros((num_nodes, num_nodes))
for i in range(num_nodes):
    if i != source_index and nodes[i] != destination:
        for j in range(num_nodes):
            #if adjacency_matrix[i, j]>0:
                  coef[i, j] = 1
            #if adjacency_matrix[j, i]>0:
                  coef[j, i] = -1
        constraints.append(LinearConstraint(coef.flatten(), 0, 0))
print(coef)
"""
# Linear constraint for dest node
dest_index = node_indices[destination]
coef = np.zeros((num_nodes, num_nodes))
for j in range(num_nodes):
    coef[dest_index, j] = -1
    coef[j, dest_index] = 1
constraints.append(LinearConstraint(coef.flatten(), -1, -1))      
"""
# Bounds for the decision variables
bounds = [(0, 1)] * (num_nodes**2)

# Initial guess
initial_solution = np.random.randn(num_nodes**2) * 0.5 +1

# Solve the optimization problem
res = minimize(objective_function, initial_solution, constraints=constraints, bounds=bounds, method='trust-constr', options={'verbose': 1})
degreep = [0] * len(nodes)
degreen=[0] * len(nodes)
c=0
for j in range(0,len(res.x)):
        if res.x[j]>0.5:
            #print("x_",j//len(a),"_",j%len(a),"   ",j,"  ",nodes[j//len(a)],"_",nodes[j%len(a)])
             t=j//num_nodes+j%num_nodes
             print("j=",j,"(",nodes[j//num_nodes],"_",nodes[j%num_nodes],")",end="")
             degreen[j//num_nodes]=degreen[j//num_nodes]+1
             degreep[j%num_nodes]=degreep[j%num_nodes]+1
             c=c+1
print("\nc=",c)
for i in range(len(nodes)):
    print(nodes[i],"=",degreen[i],",",degreep[i])
# Extract the shortest path from the optimal solution
shortest_path = []
current_node = source
while current_node != destination:
    for i in range(num_nodes):
        if res.x[node_indices[current_node] * num_nodes + i] > 0.5:
            shortest_path.append(current_node)
            #print(node_indices[current_node] * num_nodes + i   )
            current_node = nodes[i]
            break
shortest_path.append(destination)

print("Shortest path from", source, "to", destination, ":", " -> ".join(shortest_path))

