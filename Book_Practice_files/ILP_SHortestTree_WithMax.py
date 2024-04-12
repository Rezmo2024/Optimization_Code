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
    'H': {},
    'F': {'H': 5, 'G': 2,'C': 2, 'E': 7},
    'G': {'H': 4, 'D': 7, 'F': 2 },
}
graph=Directed_Graph
graph=Undirected_Graph
# Define the source and Destination nodes
source = 'A'
Destination = [ 'H', 'G','E']
# Create a PuLP model
model = pulp.LpProblem('Shoretst Path Tree', pulp.LpMinimize)
# Define the decision variables
variables = {}
for node in graph:
    for neighbor in graph[node]:
        variables[f'Z_{node}_{neighbor}'] = pulp.LpVariable(f'Z_{node}_{neighbor}', cat='Binary')
for node in graph:
    for neighbor in graph[node]:
      for i in Destination:
        variables[f'x_{node}_{neighbor}_{i}'] = pulp.LpVariable(f'x_{node}_{neighbor}_{i}', cat='Binary')
# Define the objective function
model +=sum(graph[node][neighbor] * variables[f'Z_{node}_{neighbor}'] for node in graph for neighbor in graph[node])
# Define Constraints
for i in Destination:
    model +=((sum( variables[f'x_{node}_{neighbor}_{i}'] for node in graph for neighbor in graph[node] if node==source)-sum( variables[f'x_{neighbor}_{node}_{i}']   for neighbor in graph for node in graph[neighbor] if node==source))==1,str(i)+" Source Constarint")
for node in graph:
    if node != source and node not in Destination:
        for i in Destination:
                 model += ((sum(variables[f'x_{prev_node}_{node}_{i}'] for prev_node in graph if node in graph[prev_node]) - sum(variables[f'x_{node}_{next_node}_{i}'] for next_node in graph[node] ))==0,"Intermediate Nodes Constraint_"+str(node)+"_"+str(i))
for i in Destination:
            model +=((sum( variables[f'x_{node}_{neighbor}_{i}'] for node in graph for neighbor in graph[node] if node==i)-sum( variables[f'x_{neighbor}_{node}_{i}'] for neighbor in graph for node in graph[neighbor] if node==i))==-1,str(i)+" Destination Constraint")
for node in graph:
    for neighbor in graph[node]:
        for i in Destination:
           model+=((variables[f'Z_{node}_{neighbor}'] )- (variables[f'x_{node}_{neighbor}_{i}']  )>=0)
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
     sol_graph[node]={}
for node in graph:
    for neighbor in graph[node]:
            e_labels1[(node, neighbor)]=graph[node][neighbor]
            for i in Destination:            
             if variables[f'x_{node}_{neighbor}_{i}'].varValue >0:
                print(f'({node}, {neighbor},{i})',end="")
                e_labels2[(node, neighbor)]=str(graph[node][neighbor])
                sol_graph[node][neighbor]=int(graph[node][neighbor] *variables[f'x_{node}_{neighbor}_{i}'].varValue)
            cost=cost+graph[node][neighbor] * variables[f'Z_{node}_{neighbor}'].varValue
print("\nCalculated cost=",cost, "  Optimal Cost=", pulp.value(model.objective))
Show_Graph.Show(graph,sol_graph,"Calculating Shoretst Path Tree","Primary Graph","Shoretst Path Tree",e_labels1,e_labels2)
