import networkx as nx
from pulp import *
# Create an undirected graph from the dictionary
G = nx.Graph()
graph=[
    ('A', 'B', 40),('A', 'C', 10),('A', 'D', 20),('B', 'C', 20),('B', 'E', 10),
    ('B', 'A', 40),('C', 'D', 30),('C', 'F', 20),('C', 'A', 10),('C', 'B', 20),
    ('D', 'G', 70),('D', 'A', 20),('D', 'C', 30),('E', 'H', 30),('E', 'F', 70),
    ('E', 'B', 10),('H', 'F', 50),('H', 'E', 30),('H', 'G', 40),('F', 'H', 50),
    ('F', 'G', 20),('F', 'C', 20),('F', 'E', 70),('G', 'H', 40),('G', 'D', 70),
    ('G', 'F', 20)
]
G.add_weighted_edges_from(graph)
u={(graph[i][0],graph[i][1]): graph[i][2] for i in range(len(graph))}
D = {('h1','h2'):8,('h3','h1'):3,('h2','h4'):4,('h3','h4'):8,('h1','h5'):5}#source and destination and their traffic rate
Connect_to = {'h1': 'A', 'h2': 'E', 'h3': 'H', 'h4': 'F', 'h5': 'F'} #connected node
c={('h1', 'h2'): 15, ('h3', 'h1'): 150, ('h2', 'h4'): 150, ('h3', 'h4'): 150, ('h1', 'h5'): 76}#utility coefficeint
pairs={}
for h in D:
    src=h[0]
    dst=h[1]
    pairs[(src,dst)]=[]
for s,d  in pairs:
    p=nx.dijkstra_path(G,Connect_to[s],Connect_to[d])
    for i in range(1,len(p)):
        pairs[(s,d)].append((p[i-1],p[i]))
paths_links={}
for (s,d) in pairs: 
    for i in range(0,len(pairs[(s,d)])):
        paths_links[pairs[(s,d)][i]]=0
for (s,d) in pairs: 
    for i in range(0,len(pairs[(s,d)])):
        paths_links[pairs[(s,d)][i]]=paths_links[pairs[(s,d)][i]]+D[(s,d)]        
prob = LpProblem("Congestion_Problem", LpMaximize)
tau  = {(i): LpVariable(name=f"tau_{i}",lowBound=0) for i in D}
p  = {(i,j): pairs[(i,j)] for (i,j) in pairs}
U = {(i): LpVariable(name=f"u_{i}") for i in D}
alpha = 0  # Alpha values
# Define the objective function
#Obj = [c[d] * tau[d] if alpha == 0 else c[d] * log(tau[d]) if alpha == 1 else c[d] * (tau[d] ** (1 - alpha)) / (1 - alpha) for d in D]
Obj = [(c[d] * tau[d] if alpha == 0 else 0)for d in D ]
prob += sum(Obj)
# Define the constraints
for link in paths_links:
    prob+=sum(paths_links[link]*tau[(src,dst)]for (src,dst) in pairs if link in pairs[(src,dst)] )<=u[link]
prob.solve()
#print results
print(prob)
print("Status:", LpStatus[prob.status])
print("Objective value:", prob.objective.value())
for (src,dst) in pairs:
        print(f"Traffic Flow {src} -> {dst} is used tau=",tau[(src,dst)].varValue)