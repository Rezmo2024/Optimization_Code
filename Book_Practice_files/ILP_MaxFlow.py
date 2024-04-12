import pulp
import Show_Graph
Directed_Graph = {
    'A': {'B': 4, 'C': 1, 'D': 2},
    'B': {'C': 2, 'E': 1},
    'C': {'D': 3, 'F': 2},
    'D': {'G': 7},
    'E': {'H': 3, 'F': 7},
    'F': {'H': 6, 'G': 2},
    'G': {'H': 4 },
    'H': {}
}
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
graph=Directed_Graph
#graph=Undirected_Graph
source = 'A'
Destination = 'H'
model = pulp.LpProblem('Max Flow', pulp.LpMaximize)
v = pulp.LpVariable(name="V", lowBound=0)
variables = {}
for node in graph:
    for neighbor in graph[node]:
        variables[f'x_{node}_{neighbor}'] = pulp.LpVariable(f'x_{node}_{neighbor}',lowBound=0,upBound= graph[node][neighbor])
model +=v
model +=((sum( variables[f'x_{node}_{neighbor}'] for node in graph for neighbor in graph[node] if node==source)-sum( variables[f'x_{neighbor}_{node}'] for neighbor in graph for node in graph[neighbor] if node==source))==v,"Source Constarint")

for node in graph:
    if node != source and node!=Destination:
        model += ((sum(variables[f'x_{prev_node}_{node}'] for prev_node in graph if node in graph[prev_node]) - sum(variables[f'x_{node}_{next_node}'] for next_node in graph[node] ))==0,"Intermediate Nodes Constraint_"+str(node))
print(model)
model.solve()
sol_graph={}
e_labels1={}
e_labels2={}
print(f'Status: {pulp.LpStatus[model.status]}')
for var in model.variables():
     print(f"{var.name}: {var.value()}")
for node in graph:
     sol_graph[node]={}
for node in graph:    
    for neighbor in graph[node]:
            e_labels1[(node, neighbor)]=graph[node][neighbor]                        
            if variables[f'x_{node}_{neighbor}'].varValue >0:
                sol_graph[node][neighbor]=int(variables[f'x_{node}_{neighbor}'].varValue)
                e_labels2[(node, neighbor)]=int(variables[f'x_{node}_{neighbor}'].varValue)
print(sol_graph)               
Show_Graph.Show(graph,sol_graph,"Calculating Max Flow","Primary Graph","Max Flow Graph",e_labels1,e_labels2)