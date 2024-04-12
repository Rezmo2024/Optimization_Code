import numpy as np
from scipy.optimize import minimize
import numpy as np

Undirected_Graph = {
    'A': {'B': 4, 'C': 1, 'D': 2},
    'B': {'C': 2, 'E': 1,'A': 4},
    'C': {'D': 3, 'F': 2, 'A': 1,'B': 2},
    'D': {'G': 7, 'A': 2,'C': 3},
    'E': {'H': 3, 'F': 7, 'B': 1},
    'H': {'F': 5, 'E': 3, 'G': 4},
    'F': {'H': 5, 'G': 2,'C': 2, 'E': 7},
    'G': {'H': 4, 'D': 7, 'F': 2 },
}
source = 'A'
Destination = 'H'
nodes = sorted(Undirected_Graph.keys())
num_nodes = len(nodes)
adjacency_matrix = np.zeros((num_nodes, num_nodes))

node_indices = {node: i for i, node in enumerate(nodes)}

for node, neighbors in Undirected_Graph.items():
    i = node_indices[node]
    for neighbor, weight in neighbors.items():
        j = node_indices[neighbor]
        adjacency_matrix[i, j] = weight

print(adjacency_matrix)
source_index=node_indices[source]
dest_index=node_indices[Destination]
print(source_index,"::",dest_index)
a=adjacency_matrix
# Objective function
def objective_function(x):
    return sum(a[i][j] * x[i*len(a) + j] for i in range(len(a)) for j in range(len(a)) )

# Equality constraint function
def source_constraint(x, s):
    sum1=0
    sum2=0
    for i in range(len(a)):
         for j in range(len(a)):
            if i!=j and i==s and a[i,j]>0:
                sum1 = sum1+x[i*len(a) + j] 
    for j in range(len(a)):
        for i in range(len(a)):
            if i!=j and i==s and a[i,j]>0:
                sum2 = sum2+x[j*len(a) + i] 
    print("*sum1-sum2=",sum1-sum2)
    return sum1 - sum2 - 1
def intermediate_constraint(x, s,d):
    sum1=0
    sum2=0
    for i in range(len(a)):
         for j in range(len(a)):
            if i!=j and i!=s and j!=d and a[i,j]>0:
                sum1 = sum1+x[i*len(a) + j] 
    for j in range(len(a)):
        for i in range(len(a)):
            if i!=j and i!=s and j!=d and a[i,j]>0:
                sum2 = sum2+x[j*len(a) + i] 
    print("**sum1-sum2=",sum1-sum2)
    #sum1 = sum(x[i*len(a) + j] for i in range(len(a)) for j in range(len(a)) if i!=s and j!=d and i!=j)
    #sum2 = sum(x[j*len(a) + i] for i in range(len(a)) for j in range(len(a)) if i!=s and j!=d and i!=j)
    return sum1 - sum2 
    
def dest_constraint(x, d):
    sum1=0
    sum2=0
    for i in range(len(a)):
         for j in range(len(a)):
            if i!=j and i==d and a[i,j]>0:
                sum1 = sum1+x[i*len(a) + j] 
    for j in range(len(a)):
        for i in range(len(a)):
            if i!=j and i==d and a[i,j]>0:
                sum2 = sum2+x[j*len(a) + i] 
    print("sum1-sum2=",sum1-sum2)
    return sum1 - sum2 + 1 
def binary_constraint(x):
    return x % 1
# Initial guess
n = 64 #8row*8column
initial_solution=np.random.randint(0,2, n)

print(initial_solution)
# Constraints
#constraints = [{'type': 'eq', 'fun': lambda x, i=source_index: source_constraint(x, i)} for i in range(len(a))]
#constraints = [{'type': 'eq', 'fun': lambda x, i=source_index,j=dest_index: source_constraint(x, i,j)} for i in range(len(a))]
constraints = [{'type': 'ineq', 'fun':  lambda x:source_constraint(x, source_index)} ,
               {'type': 'ineq', 'fun':  lambda x:dest_constraint(x, dest_index)} ,
               #{'type': 'eq', 'fun':  lambda x:binary_constraint(x)} ,
               {'type': 'eq', 'fun': lambda x: intermediate_constraint(x, source_index,dest_index)} ]

# Bounds for the decision variables
bounds = [(0, 1)] * n

# Solve the optimization problem
res = minimize(objective_function, initial_solution, method='SLSQP',constraints=constraints,  bounds=bounds)

print("Optimal solution:")
print(res.x)
print("Optimal cost:")
print(res.fun)
print(res)
c=0

degreep = [0] * len(nodes)
degreen=[0] * len(nodes)
for j in range(0,len(res.x)):
        if res.x[j]==1:
            #print("x_",j//len(a),"_",j%len(a),"   ",j,"  ",nodes[j//len(a)],"_",nodes[j%len(a)])
             t=j//len(a)+j%len(a)
             print("(",nodes[j//len(a)],"_",nodes[j%len(a)],")",end="")
             degreen[j//len(a)]=degreen[j//len(a)]+1
             degreep[j%len(a)]=degreep[j%len(a)]+1
             c=c+1
print("\nc=",c)
for i in range(len(nodes)):
    print(nodes[i],"=",degreen[i],",",degreep[i])

