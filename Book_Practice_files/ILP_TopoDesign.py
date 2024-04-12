import pulp
import itertools
import random
import networkx as nx
import matplotlib.pyplot as plt
def Draw_Solution(topo):
    G = nx.Graph()
    G.add_nodes_from(topo.keys())
    G.add_edges_from([(topo[n][i], n) for n in topo for i in range(len(topo[n]))])
    pos = nx.spring_layout(G)  # Positions for all nodes
    nx.draw(G, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=10, font_color='black', font_weight='bold', edge_color='gray', width=2.0)
    plt.title("Design Topology Problem")
    plt.show()
# Define the problem
prob = pulp.LpProblem("Topology Design Problem", pulp.LpMinimize)
# Define the data
N = 5
E = {(i, j) for i in range(1,N+1) for j in range(1,N+1) if i != j}
D = {('h1','h2'):6,('h3','h1'):2,('h2','h4'):4,('h3','h2'):5,('h4','h5'):5}
Connect_to = {'h1': 1, 'h2': 5, 'h3': 4, 'h4': 3, 'h5': 2} #connected node
X = {(i, j,d) for i in range(1,N+1) for j in range(1,N+1) for d in D if i != j}
C = {(i, j): 0 for (i, j) in E}
C={(0, 0): 0, (0, 1): 2, (0, 2): 1, (0, 3): 1, (0, 4): 2,
   (1, 0): 2, (1, 1): 0, (1, 2): 1, (1, 3): 3, (1, 4): 1,
   (2, 0): 1, (2, 1): 1, (2, 2): 0, (2, 3): 2, (2, 4): 1,
   (3, 0): 1, (3, 1): 3, (3, 2): 2, (3, 3): 0, (3, 4): 2,
   (4, 0): 2, (4, 1): 1, (4, 2): 1, (4, 3): 2, (4, 4): 0}
# Define the decision variables
y = pulp.LpVariable.dicts("y", E, cat='Binary')
u = pulp.LpVariable.dicts("u", E, lowBound=0)
x = pulp.LpVariable.dicts("x", X, lowBound=0)
# Define the objective function
prob += pulp.lpSum((C[i-1, j-1]*y[i, j] + C[i-1, j-1]*u[i,j]) for i in range(1,N+1) for j in range(1,N+1)  if i != j)
T = pulp.lpSum(D[d] for d in D)
# Define the constraints
for (i, j) in E:
    prob += u[i, j] <= T*y[i, j]
for d in D:
    for i in range(1,N+1):
        if i == Connect_to[d[0]]:
            prob += (pulp.lpSum(x[i, j, d] for j in range(1,N+1) if (i, j) in E)-pulp.lpSum(x[j, i, d] for j in range(1,N+1) if (j, i) in E)) == D[d]
        elif i == Connect_to[d[1]]:
            prob += (pulp.lpSum(x[i, j, d] for j in range(1,N+1) if (i, j) in E)-pulp.lpSum(x[j, i, d] for j in range(1,N+1) if (j, i) in E)) == -D[d]
for (i, j, d) in X:
    prob += x[i, j, d] <= u[i, j]
# Solve the problem
prob.solve()
print(prob)
# Print the solution
print("Status:", pulp.LpStatus[prob.status])
print("Objective value:", prob.objective.value())
topo={}
for i in Connect_to:
    topo[Connect_to[i]]=[i]
for (i, j) in E:
    if y[i, j].varValue == 1:
        print(f"Link {i} -> {j} is used u=",u[i,j].varValue)
        topo[i].append(j)#=[topo[i],j]
print(topo)
Draw_Solution(topo)


