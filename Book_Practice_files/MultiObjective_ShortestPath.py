import networkx as nx
import matplotlib.pyplot as plt
import Show_Graph
from collections import OrderedDict
cost = {
  'A': {'B': 4, 'C': 11, 'D': 10},
  'B': {'C': 20, 'E': 1, 'A': 4},
  'C': {'D': 3, 'F': 15, 'A': 11, 'B': 20},
  'D': {'G': 7, 'A': 10, 'C': 3},
  'E': {'H': 30, 'F': 7, 'B': 1},
  'H': {'F': 5, 'E': 30, 'G': 40},
  'F': {'H': 5, 'G': 2, 'C': 15, 'E': 7},
  'G': {'H': 40, 'D': 7, 'F': 2},
}
delay = {
  'A': {'B': 5, 'C': 11, 'D': 2},
  'B': {'C': 20, 'E': 1, 'A': 5},
  'C': {'D': 13, 'F': 25, 'A': 11, 'B': 20},
  'D': {'G': 17, 'A': 2, 'C': 13},
  'E': {'H': 3, 'F': 17, 'B': 1},
  'H': {'F': 5, 'E': 3, 'G': 4},
  'F': {'H': 3, 'G': 2, 'C': 25, 'E': 17},
  'G': {'H': 4, 'D': 17, 'F': 2},
}
# Create a directed graph from cost dictionary
G = nx.DiGraph()
for node, neighbors in cost.items():
  for neighbor, edge_cost in neighbors.items():
    G.add_edge(node, neighbor, weight=1)
def find_all_paths(start, end):
  """Finds all simple paths from start to end in the graph"""
  paths = []
  for path in nx.all_simple_paths(G, start, end):
    paths.append(path)
  return paths
def calculate_total_cost(path):
  """Calculates the total cost of a path"""
  total_cost = 0
  for i in range(len(path) - 1):
    total_cost += cost[path[i]][path[i+1]]
  return total_cost
def calculate_total_delay(path):
  """Calculates the total delay of a path"""
  total_delay = 0
  for i in range(len(path) - 1):
    total_delay += delay[path[i]][path[i+1]]
  return total_delay
# Find all paths from A to H
source='A'
destination='G'
all_paths = find_all_paths(source,destination)
best_path=""
print(f"Total number of paths between {source} and {destination} is=",len(all_paths))
# Evaluate each path based on cost and delay (multi-objective)
pareto_front = []
pareto_front_path = []
paths_score = []
path_dic={}
i=1
for path in all_paths:
    total_cost = calculate_total_cost(path)
    total_delay = calculate_total_delay(path)
    path_dic[(total_cost,total_delay)]=path
    i=i+1
# Sort the dictionary by the second number(Delay value) 
sorted_dict = OrderedDict(sorted(path_dic.items(), key=lambda x: x[0][1]))
for key, path in sorted_dict.items():
  total_cost = key[0]
  total_delay = key[1]
  paths_score.append((key[0],key[1]))  
  # Domination check for Pareto front (minimize both cost and delay)
  dominated = False
  for p in pareto_front:
    if p[0] <= total_cost and p[1] <= total_delay and (p[0] < total_cost or p[1] < total_delay):
        dominated = True
        break
  if not dominated:
      pareto_front.append((total_cost, total_delay))
      pareto_front_path.append(path)
# Print the Pareto front (possible solutions with minimal cost-delay trade-off)
print("Pareto Front (Cost, Delay):")
co=[]
de=[]
p_co=[]
p_de=[]
label={}
min_score=99999
min_index=-1
for solution in range(len(paths_score)):
    p_co.append(paths_score[solution][0])
    p_de.append(paths_score[solution][1])
for solution in range(len(pareto_front)):  
  print(f"\tCost: {pareto_front[solution][0]}, Delay: {pareto_front[solution][1]} , Path=",pareto_front_path[solution])
  co.append(pareto_front[solution][0])
  de.append(pareto_front[solution][1])
  if pareto_front[solution][0]<min_score: #cost
    min_score=pareto_front[solution][0]
    min_index=solution
  label[(pareto_front[solution][0],pareto_front[solution][1])]=pareto_front_path[solution]
plt.figure(figsize=(8, 6))
plt.scatter(p_co, p_de,linewidths=5,edgecolors='gray')
plt.scatter(co, de,linewidths=5,edgecolors='black')
[plt.text(i, j, f'({i}, {j},{label[(i,j)]})',fontsize=10,) for (i, j) in zip(co, de)]
[plt.text(i, j, f'({i}, {j})',fontsize=10,) for (i, j) in zip(p_co, p_de)]
plt.xlabel('Cost')
plt.xlim(0, 125)
plt.ylabel('Delay')
plt.title('Pareto Front')
plt.show()
best_path=pareto_front_path[min_index]
best_sol={}
e_labels1={}
e_labels2={}
for i in range(1,len(best_path)):
  best_sol.update({best_path[i-1]:{best_path[i]:cost[best_path[i-1]][best_path[i]]}})
  e_labels2[(best_path[i-1],best_path[i])]={}
  e_labels2[(best_path[i-1],best_path[i])]=str(cost[best_path[i-1]][best_path[i]])+","+str(delay[best_path[i-1]][best_path[i]])
print("Best Solution=",best_sol)
for node in cost:
    for neighbor in cost[node]:
                e_labels1[(node, neighbor)]=str(cost[node][neighbor] )+","+str(delay[node][neighbor])
Show_Graph.Show(cost,best_sol,"Calculating Shortest Path","Primary Graph","Shortest Path Graph",e_labels1,e_labels2)