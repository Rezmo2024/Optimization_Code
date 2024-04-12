import pulp
import Show_Graph
# Define the graph as a dictionary of dictionaries
Cost_Graph = {
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
# Define the source and Destination nodes
source = 'A'
Destination = 'H'
# Create a PuLP model
model = pulp.LpProblem('Weighted Multiobjetive', pulp.LpMinimize)
# Define the decision variables
variables = {}
for node in Cost_Graph:
    for neighbor in Cost_Graph[node]:
        variables[f'x_{node}_{neighbor}'] = pulp.LpVariable(f'x_{node}_{neighbor}', cat='Binary')
# Define the objective function
w1=0.999
w2=1-w1
first_objective=w1*sum(Cost_Graph[node][neighbor] * variables[f'x_{node}_{neighbor}'] for node in Cost_Graph for neighbor in Cost_Graph[node] )
second_objective=w2*sum(Delay_Graph[node][neighbor] * variables[f'x_{node}_{neighbor}'] for node in Delay_Graph for neighbor in Delay_Graph[node] )
model +=first_objective+second_objective
# Define Constraints
model +=((sum( variables[f'x_{node}_{neighbor}'] for node in Cost_Graph for neighbor in Cost_Graph[node] if node==source)-sum( variables[f'x_{neighbor}_{node}'] for neighbor in Cost_Graph for node in Cost_Graph[neighbor] if node==source))==1,"Source Constarint")
for node in Cost_Graph:
    if node != source and node!=Destination:
        model += ((sum(variables[f'x_{prev_node}_{node}'] for prev_node in Cost_Graph if node in Cost_Graph[prev_node]) - sum(variables[f'x_{node}_{next_node}'] for next_node in Cost_Graph[node] ))==0,"Intermediate Nodes Constraint_"+str(node))
print(model)
# Solve the model
model.solve()
print(model.variables)
sol_graph={}
print(f'Status: {pulp.LpStatus[model.status]}')
e_labels1={}
e_labels2={}
for node in Cost_Graph:
    for neighbor in Cost_Graph[node]:
            e_labels1[(node, neighbor)]=str(Cost_Graph[node][neighbor])+','+str(Delay_Graph[node][neighbor])
            if variables[f'x_{node}_{neighbor}'].varValue == 1:
                print(f'({node}, {neighbor})',end="")
                e_labels2[(node, neighbor)]=w1*Cost_Graph[node][neighbor]+w2*Delay_Graph[node][neighbor]
                sol_graph.update({node:{neighbor:(Cost_Graph[node][neighbor] *variables[f'x_{node}_{neighbor}'].varValue)}})
print("\n Optimal Cost(W1="+str("{:.3f}".format(w1))+", W2="+str("{:.3f}".format(w2))+")=", pulp.value(model.objective))
Show_Graph.Show(Cost_Graph,sol_graph,"Calculating Weighted Multiobjetive","Primary Graph","Solution for Weighted Multiobjetive(W1="+str("{:.3f}".format(w1))+", W2="+str("{:.3f}".format(w2))+")",e_labels1,e_labels2)