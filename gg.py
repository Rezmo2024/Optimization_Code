import numpy as np
from scipy.optimize import minimize
import numpy as np

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

# Get the unique nodes
nodes = list(Undirected_Graph.keys())

# Create the constraint matrix A and the right-hand side vector b
A = np.zeros((len(nodes), len(nodes)))
b = np.zeros(len(nodes))

for i, node in enumerate(nodes):
    for neighbor, weight in Undirected_Graph[node].items():
        j = nodes.index(neighbor)
        A[i, j] = 1# weight
        A[j, i] = 1# weight
    b[i] =0# sum(Undirected_Graph[node].values())
print("Constraint matrix A:")
print(A)
print("\nRight-hand side vector b:")
print(b)
# Define the problem parameters
#A = np.array([[0, 5, 3], [0, 0, 4], [0, 0, 0]])  # Constraint matrix
#b = np.array([10, 20, 30])  # Constraint right-hand side
c = b  # Objective function coefficients
# Define the objective function
def objective(x):
    return np.sum(x)  # Non-linear objective function

# Define the constraints
def constraints(x):
    s=1
    d=7
    y=x[s*8:(s+1)*8]
    z=x[d*8:(d+1)*8]
    X = [item for i, item in enumerate(x) if i not in range(s*8, (s+1)*8) and i not in range(d*8, (d+1)*8)]
    #print(len(X))
    new_A = np.delete(A, [s, d], axis=0)
    one_dim_list = new_A.flatten().tolist()

    #print(len(one_dim_list))
    ss=A[s] @ y - 1
    dd=A[d] @ z + 1
    ii = np.array(one_dim_list) * np.array(X) - np.array(0)
    #ii=one_dim_list @ X - 0
    b[s]=1
    b[d]=-1
    arr = np.empty((0, len(A[s])))  # 0 rows, 4 columns
    arr = np.vstack((arr, A[s], A[d],new_A))
    #print("ss=",ss)
    #print("dd=",dd)
    #print("ii=",ii)

    #print(A[s]@x-1)
    return A @ y - b  # Linear constraints

# Define the bounds
bounds = [(0, 1) for _ in range(64)]

# Solve the optimization problem
initial_guess = np.ones(64)
#print(initial_guess)
result = minimize(objective, initial_guess, method='SLSQP', constraints=[{'type': 'eq', 'fun': constraints}], bounds=bounds)

# Print the results
print(f"Optimal value: {result.fun}")
#print(f"Optimal solution: {result.x}")
for i in range(len(result.x)):
    if result.x[i]>0.20:
        print(f"x({i//8},{i%8})",result.x[i])
