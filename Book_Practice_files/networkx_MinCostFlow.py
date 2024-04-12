import networkx as nx
import matplotlib.pyplot as plt
# Convert the given directed graph to a networkx graph
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
G = nx.DiGraph()
fig, axs = plt.subplots(ncols=2, figsize=(12, 5), gridspec_kw={'width_ratios': [8,  8]})
for node, edges in Graph_Capacity.items():
    for neighbor, capacity in edges.items():
        G.add_edge(node, neighbor, capacity=capacity)
for node, edges in Graph_Cost.items():
    for neighbor, weight in edges.items():
        nx.set_edge_attributes(G, {(node, neighbor): {"weight": weight}})        
# Set the edge labels to the weight attribute
edge_labels = {(u, v): str(G[u][v]['weight'])+","+str(G[u][v]['capacity']) for u, v in G.edges()}
#pos = nx.spring_layout(G)
#Custom position of nodes
pos = { 'A': (0, 30), 'B': (10, 40), 'C': (10, 30),'D': (10, 20),'E': (20, 40),'F': (20, 30),'G': (20, 20),'H': (30, 30)} 
nx.draw_networkx_nodes(G, pos,node_color='white',linewidths=1,alpha=1, edgecolors='#000000',ax=axs[0])
nx.draw_networkx_edges(G, pos,edge_color='brown',ax=axs[0])
nx.draw_networkx_labels(G, pos,ax=axs[0])
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,label_pos=0.5,font_size=12,font_weight='bold',ax=axs[0])
fig.axes[0].set_title("Primary Graph")
W=nx.Graph()
G.add_node("A", demand=-6)
G.add_node("H", demand=6)
L=nx.min_cost_flow(G)
print(L)
for node, edges in L.items():
    for neighbor, capacity in edges.items():
        if capacity>0:
            W.add_edge(node, neighbor, capacity=capacity)
print(W)
print(nx.min_cost_flow_cost(G))
edge_labels = {(u, v): str(G[u][v]['weight'])+","+str(W[u][v]['capacity']) for u, v in W.edges()}
nx.draw_networkx_nodes(G, pos,node_color='white',linewidths=1,alpha=1, edgecolors='#000000',ax=axs[1])
nx.draw_networkx_edges(G, pos,edge_color='brown',ax=axs[1])
nx.draw_networkx_nodes(W, pos,node_color='white',linewidths=2,alpha=1, edgecolors='#000000',ax=axs[1])
nx.draw_networkx_edges(W, pos,edge_color='blue',ax=axs[1],width=3,arrowsize=15,arrows=True, arrowstyle='->')
nx.draw_networkx_labels(W, pos,ax=axs[1])
nx.draw_networkx_edge_labels(W, pos, edge_labels=edge_labels,label_pos=0.5,font_size=12,font_weight='bold',ax=axs[1])
fig.axes[1].set_title("Min Cost Graph")
plt.suptitle("Calculating Minimum Cost Flow")
plt.show()
