import pulp
import Show_Graph
# Define the graph as a dictionary of dictionaries
BW_Graph = {
    'A': {'B': 4, 'C': 1, 'D': 2},
    'B': {'C': 2, 'E': 1,'A': 4},
    'C': {'D': 3, 'F': 2, 'A': 1,'B': 2},
    'D': {'G': 7, 'A': 2,'C': 3},
    'E': {'H': 3, 'F': 7, 'B': 1},
    'H': {'F': 5, 'E': 3, 'G': 4},
    'F': {'H': 5, 'G': 2,'C': 2, 'E': 7},
    'G': {'H': 4, 'D': 7, 'F': 2 },
}
Delay_Graph = {
    'A': {'B': 40, 'C': 10, 'D': 20},
    'B': {'C': 20, 'E': 10,'A': 40},
    'C': {'D': 30, 'F': 20, 'A': 10,'B': 20},
    'D': {'G': 70, 'A': 20,'C': 30},
    'E': {'H': 30, 'F': 70, 'B': 10},
    'H': {'F': 15, 'E': 30, 'G': 40},
    'F': {'H': 15, 'G': 20,'C': 20, 'E': 70},
    'G': {'H': 40, 'D': 70, 'F': 20 },
}
def find_max_value(graph):
    max_value = 0
    for node, neighbors in graph.items():
        for neighbor, value in neighbors.items():
            if value > max_value:
                max_value = value
    return max_value

def add_dicts(dict1, dict2,Max_bw,Max_delay, alpha):
    result = {}
    for key1, value1 in dict1.items():
        if key1 in dict2:
            result[key1] = {}
            for key2, value2 in value1.items():
                if key2 in dict2[key1]:
                    result[key1][key2] = alpha*(value1[key2]/Max_bw) + (1-alpha)*(dict2[key1][key2]/Max_delay)
                else:
                    result[key1][key2] = value1[key2]
        else:
            result[key1] = value1
    for key2 in dict2:
        if key2 not in result:
            result[key2] = dict2[key2]
    return result

Max_Delay=find_max_value(Delay_Graph)
Max_Bw=find_max_value(BW_Graph)
print("max=",Max_Bw,Max_Delay)
graph=add_dicts(BW_Graph,Delay_Graph,Max_Bw,Max_Delay,0.5)
# Define the source and Destination nodes
source = 'A'
Destination = 'H'
T=50
# Create a PuLP model
model = pulp.LpProblem('Constraint Shortest Path', pulp.LpMinimize)
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
model +=(sum(Delay_Graph[node][neighbor] * variables[f'x_{node}_{neighbor}'] for node in graph for neighbor in graph[node] )<=T,"Delay Constraint")

print(model)
# Solve the model
model.solve()
print(model.variables)
sol_graph={}
print(f'Status: {pulp.LpStatus[model.status]}')
cost=0
delay=0
e_labels1={}
e_labels2={}
for node in graph:
    for neighbor in graph[node]:
            e_labels1[(node, neighbor)]=str(BW_Graph[node][neighbor])+','+str(Delay_Graph[node][neighbor])
            if variables[f'x_{node}_{neighbor}'].varValue == 1:
                print(f'({node}, {neighbor})',end="")
                e_labels2[(node, neighbor)]="{:.2f}".format(round(graph[node][neighbor] , 2)) 
                sol_graph.update({node:{neighbor:(graph[node][neighbor] *variables[f'x_{node}_{neighbor}'].varValue)}})
                cost=cost+graph[node][neighbor] * variables[f'x_{node}_{neighbor}'].varValue
                delay=delay+Delay_Graph[node][neighbor] * variables[f'x_{node}_{neighbor}'].varValue
print("\nCalculated cost=",cost, "  Optimal Cost=", pulp.value(model.objective),"  Delay=",delay)
Show_Graph.Show(graph,sol_graph,"Calculating Constraint Shortest Path","Primary Graph","Constraint Shortest Path Graph",e_labels1,e_labels2)