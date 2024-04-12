import pulp
import Show_Graph
# Define the graph as a dictionary of dictionaries
BW_Graph = {
    'A': {'B': 4, 'C': 1, 'D': 2},
    'B': {'C': 2, 'E': 1,'A': 4},
    'C': {'D': 3, 'F': 2, 'A': 1,'B': 2},
    'D': {'G': 7, 'A': 2,'C': 3},
    'E': {'H': 3, 'F': 7, 'B': 1},
    'H': {},
    'F': {'H': 5, 'G': 2,'C': 2, 'E': 7},
    'G': {'H': 4, 'D': 7, 'F': 2 },
}
Delay_Graph = {
    'A': {'B': 40, 'C': 10, 'D': 20},
    'B': {'C': 20, 'E': 10,'A': 40},
    'C': {'D': 30, 'F': 20, 'A': 10,'B': 20},
    'D': {'G': 6, 'A': 20,'C': 30},
    'E': {'H': 30, 'F': 70, 'B': 10},
    'H': {},
    'F': {'H': 15, 'G': 20,'C': 20, 'E': 70},
    'G': {'H': 40, 'D': 6, 'F': 20 },
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
Destination = [ 'H', 'G','E']
T=45
# Create a PuLP model
model = pulp.LpProblem('Constraint Shoretst Path Tree', pulp.LpMinimize)
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

for i in Destination:
    model +=(sum(Delay_Graph[node][neighbor] * variables[f'x_{node}_{neighbor}_{i}'] for node in graph for neighbor in graph[node])<=T,str(i)+" Delay Constarint")

print(model)
# Solve the model
model.solve()
print(model.variables)
sol_graph={}
print(f'Status: {pulp.LpStatus[model.status]}')
cost=0
delay=0
del_dest={}
for x in Destination:
    del_dest[x]=0
e_labels1={}
e_labels2={}
for node in graph:
     sol_graph[node]={}
for node in graph:
    for neighbor in graph[node]:
            e_labels1[(node, neighbor)]=str(BW_Graph[node][neighbor])+','+str(Delay_Graph[node][neighbor])
            for i in Destination:            
             if variables[f'x_{node}_{neighbor}_{i}'].varValue >0:
                print(f'({node}, {neighbor},{i})',end="")
                e_labels2[(node, neighbor)]="{:.2f}".format(round(graph[node][neighbor] , 2)) 
                sol_graph[node][neighbor]=(graph[node][neighbor] *variables[f'x_{node}_{neighbor}_{i}'].varValue)
                del_dest[i]=del_dest[i]+Delay_Graph[node][neighbor] * variables[f'x_{node}_{neighbor}_{i}'].varValue
            cost=cost+graph[node][neighbor] * variables[f'Z_{node}_{neighbor}'].varValue
            delay=delay+Delay_Graph[node][neighbor] * variables[f'Z_{node}_{neighbor}'].varValue
print("\nDelay Destination=",del_dest)
print("Calculated cost=",cost, "  Optimal Cost=", pulp.value(model.objective)," Delay Tree=",delay)
Show_Graph.Show(graph,sol_graph,"Calculating Constraint Shoretst Path Tree","Primary Graph","Constraint Shoretst Path Tree",e_labels1,e_labels2)
