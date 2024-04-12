import pulp
import Show_Graph
# Define the graph as a dictionary of dictionaries
Graph_Capacity = {
    'A': {'B': 4, 'C': 1, 'D': 2},
    'B': {'C': 2, 'E': 1},
    'C': {'D': 3, 'F': 2},
    'D': {'G': 7},
    'E': {'H': 3, 'F': 7},
    'F': {'H': 6, 'G': 2},
    'G': {'H': 4 },
    'H': {}
}
Graph_Cost = {
    'A': {'B': 20, 'C': 15, 'D': 30},
    'B': {'C': 14, 'E': 18},
    'C': {'D': 25, 'F': 32},
    'D': {'G': 40},
    'E': {'H': 25, 'F': 17},
    'F': {'H': 18, 'G': 22},
    'G': {'H': 14 },
    'H': {}
}
graph=Graph_Capacity
# Define the source and Destination nodes
source = 'A'
Destination = 'H'
# Create a PuLP model
model = pulp.LpProblem('Min Cost Flow', pulp.LpMinimize)
# Define the decision variables
v = 6
variables = {}
for node in graph:
    for neighbor in graph[node]:
        variables[f'x_{node}_{neighbor}'] = pulp.LpVariable(f'x_{node}_{neighbor}',lowBound=0,upBound= graph[node][neighbor])
# Define the objective function
model +=sum(Graph_Cost[node][neighbor] * variables[f'x_{node}_{neighbor}'] for node in Graph_Cost for neighbor in Graph_Cost[node] )
# Define Constraints
model +=((sum( variables[f'x_{node}_{neighbor}'] for node in graph for neighbor in graph[node] if node==source)-sum( variables[f'x_{neighbor}_{node}'] for neighbor in graph for node in graph[neighbor] if node==source))==v,"Source Constarint")

for node in graph:
    if node != source and node!=Destination:
        model += ((sum(variables[f'x_{prev_node}_{node}'] for prev_node in graph if node in graph[prev_node]) - sum(variables[f'x_{node}_{next_node}'] for next_node in graph[node] ))==0,"Intermediate Nodes Constraint_"+str(node))

print(model)
# Solve the model
model.solve()
sol_graph={}
e_labels1={}
e_labels2={}
cost=0
print(f'Status: {pulp.LpStatus[model.status]}')
for var in model.variables():
     print(f"{var.name}: {var.value()}")
for node in graph:
     sol_graph[node]={}
for node in graph:    
    for neighbor in graph[node]:
            e_labels1[(node, neighbor)]=str(Graph_Cost[node][neighbor])+','+str(Graph_Capacity[node][neighbor])
            if variables[f'x_{node}_{neighbor}'].varValue >0:
                sol_graph[node][neighbor]=int(variables[f'x_{node}_{neighbor}'].varValue)
                cost=cost+int(variables[f'x_{node}_{neighbor}'].varValue)*Graph_Cost[node][neighbor]
                e_labels2[(node, neighbor)]=str(Graph_Cost[node][neighbor])+','+str((variables[f'x_{node}_{neighbor}'].varValue))
print(sol_graph)           
print("Cost=",cost, " Volume=",v , "Is Optimal=",f'Status: {pulp.LpStatus[model.status]}')     
Show_Graph.Show(graph,sol_graph,"Calculating Max Flow","Primary Graph","Max Flow Graph",e_labels1,e_labels2)     

