import pulp
import Show_Graph
# Define the graph as a dictionary of dictionaries
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
graph=Undirected_Graph
# Define the source and Destination nodes
source = 'A'
Destination = 'H'
# Create a PuLP model
model = pulp.LpProblem('Shortest Path', pulp.LpMinimize)
# Define the decision variables
variables = {}
for node in graph:
    for neighbor in graph[node]:
        variables[f'x_{node}_{neighbor}'] = pulp.LpVariable(f'x_{node}_{neighbor}', cat='Binary')
# Define the objective function
model +=sum(graph[node][neighbor] * variables[f'x_{node}_{neighbor}'] for node in graph for neighbor in graph[node] )
# Define Constraints
model +=((sum( variables[f'x_{node}_{neighbor}'] for node in graph for neighbor in graph[node] if node==source)-sum( variables[f'x_{neighbor}_{node}'] for neighbor in graph for node in graph[neighbor] if node==source))==1,"Source Constarint")
#model +=((sum( variables[f'x_{node}_{neighbor}'] for node in graph for neighbor in graph[node] if node==Destination)-sum( variables[f'x_{neighbor}_{node}'] for neighbor in graph for node in graph[neighbor] if node==Destination))==-1,"Destination Constraint")
for node in graph:
    if node != source and node!=Destination:
        model += ((sum(variables[f'x_{prev_node}_{node}'] for prev_node in graph if node in graph[prev_node]) - sum(variables[f'x_{node}_{next_node}'] for next_node in graph[node] ))==0,"Intermediate Nodes Constraint_"+str(node))
print(model)
# Solve the model
model.solve()
print(model.variables)
sol_graph={}
print(f'Status: {pulp.LpStatus[model.status]}')
cost=0
e_labels1={}
e_labels2={}
for node in graph:
    for neighbor in graph[node]:
            e_labels1[(node, neighbor)]=graph[node][neighbor]            
            if variables[f'x_{node}_{neighbor}'].varValue == 1:
                print(f'({node}, {neighbor})',end="")
                e_labels2[(node, neighbor)]=graph[node][neighbor]
                sol_graph.update({node:{neighbor:int(graph[node][neighbor] *variables[f'x_{node}_{neighbor}'].varValue)}})
                cost=cost+graph[node][neighbor] * variables[f'x_{node}_{neighbor}'].varValue
print("\ncost=",cost)                
Show_Graph.Show(graph,sol_graph,"Calculating Shortest Path","Primary Graph","Shortest Path Graph",e_labels1,e_labels2)