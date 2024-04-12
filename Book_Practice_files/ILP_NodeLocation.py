from pulp import LpMinimize, LpProblem, LpVariable, lpSum, value,LpStatus
import networkx as nx
import matplotlib.pyplot as plt
def Draw_Solution(connection_dict):
    # Create a directed graph
    G = nx.DiGraph()
    # Add nodes and edges from the nested dictionary
    for source, targets in connection_dict.items():
        for target, cost in targets.items():
            G.add_edge(source, target, weight=cost)
    # Draw the graph with labels
    pos = nx.spring_layout(G)  # Positions for all nodes
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color="white", edgecolors='#000000',linewidths=1,font_size=10, font_weight="bold", edge_color='black')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='blue',font_weight="bold")
    plt.title("NetworkX Graph with Labels")
    plt.axis('off')
    plt.show()
# Sample numbers for the coefficients c_ij and d_j
edge_nodes_Location = ['H1','H2','H3','H4','H5','H6','H7','H8','H9','H10']
Core_nodes_Location = ['S1','S2','S3']
Connection_Cost ={('H1', 'S1'): 4, ('H2', 'S1'): 5, ('H3', 'S1'): 8, ('H4', 'S1'): 6, ('H5', 'S1'): 3, ('H6', 'S1'): 7,
 ('H7', 'S1'): 2, ('H8', 'S1'): 6, ('H9', 'S1'): 5, ('H10', 'S1'): 7, ('H1', 'S2'): 4, ('H2', 'S2'): 3,
 ('H3', 'S2'): 5, ('H4', 'S2'): 2, ('H5', 'S2'): 3, ('H6', 'S2'): 9, ('H7', 'S2'): 8, ('H8', 'S2'): 1,
 ('H9', 'S2'): 6, ('H10', 'S2'): 9}

en_traffic={'H1':4,'H2':5,'H3':6,'H4':8,'H5':5,'H6':7,'H7':8,'H8':2,'H9':4,'H10':4}
cost_Core = {'S1':20,'S2':10}
k = 5
M=2
Core_nodes_Tr_capaciry = 30
# Create the LP problem
model = LpProblem("Optimization Problem", LpMinimize)
# Define decision variables
x = {(i, j): LpVariable(f'x_{i}_{j}', cat='Binary') for i in edge_nodes_Location for j in  cost_Core}
y = {j: LpVariable(f'y_{j}', cat='Binary') for j in  cost_Core}
# Objective function
model += lpSum(Connection_Cost[(i,j)] * x[i, j] for i in  edge_nodes_Location for j in  cost_Core) + lpSum(cost_Core[j] * y[j] for j in  cost_Core )
# Constraint 1
for i in  edge_nodes_Location:
    model += lpSum(x[i, j] for j in  cost_Core) == 1
# Constraint 2,3
for j in cost_Core:
    model += lpSum(x[i, j] for i in edge_nodes_Location) <= k * y[j]
    model += lpSum(x[i, j] * en_traffic[i] for i in  edge_nodes_Location) <= Core_nodes_Tr_capaciry* y[j]
# Constraint 4
model += lpSum(y[j] for j in  cost_Core ) <= M
# Solve the model
model.solve()
# Print Results
print(model)
print(f'Status: {LpStatus[model.status]}')
print("Optimal Objective Value:", value(model.objective))
topo={}
for j in  cost_Core:
     topo[j]={}
     for i in  edge_nodes_Location:
        if value(x[i, j])==1:
            topo[j][i]=Connection_Cost[(i,j)]
print(topo)
Draw_Solution(topo)