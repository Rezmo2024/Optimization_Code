import networkx as nx
import matplotlib.pyplot as plt
# Convert the given directed graph to a networkx graph
Directed_Graph = {
    'A': {'B': 4, 'C': 1, 'D': 2},
    'B': {'C': 2, 'E': 1},
    'C': {'D': 3, 'F': 2},
    'D': {'C': 3, 'G': 7},
    'E': {'H': 3, 'F': 7},
    'H': {'F': 5,'H': 5},
    'F': {'H': 6, 'G': 2},
    'G': {'H': 4 },
    'H': {}
}
G = nx.DiGraph()
fig, axs = plt.subplots(ncols=2, figsize=(12, 5), gridspec_kw={'width_ratios': [8,  8]})
for node, edges in Directed_Graph.items():
    for neighbor, weight in edges.items():
        G.add_edge(node, neighbor, weight=weight)
# Set the edge labels to the weight attribute
edge_labels = {(u, v): G[u][v]['weight'] for u, v in G.edges()}
#pos = nx.spring_layout(G)
#Custom position of nodes
pos = { 'A': (0, 30), 'B': (10, 40), 'C': (10, 30),'D': (10, 20),'E': (20, 40),'F': (20, 30),'G': (20, 20),'H': (30, 30)} 
nx.draw_networkx_nodes(G, pos,node_color='white',linewidths=1,alpha=1, edgecolors='#000000',ax=axs[0])
nx.draw_networkx_edges(G, pos,edge_color='brown',ax=axs[0])
nx.draw_networkx_labels(G, pos,ax=axs[0])
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,label_pos=0.5,font_size=12,font_weight='bold',ax=axs[0])
fig.axes[0].set_title("Primary Graph")
print("Maximum Flow=",nx.maximum_flow(G,'A','H',capacity='weight'))
W=nx.Graph()
L=nx.maximum_flow(G,'A','H',capacity='weight')
print(L[1])
for node, edges in L[1].items():
    for neighbor, weight in edges.items():
        if weight>0:
            W.add_edge(node, neighbor, weight=weight)
print(W)
edge_labels = {(u, v): W[u][v]['weight'] for u, v in W.edges()}
print(edge_labels)
nx.draw_networkx_nodes(G, pos,node_color='white',linewidths=1,alpha=1, edgecolors='#000000',ax=axs[1])
nx.draw_networkx_edges(G, pos,edge_color='brown',ax=axs[1])
nx.draw_networkx_nodes(W, pos,node_color='white',linewidths=2,alpha=1, edgecolors='#000000',ax=axs[1])
nx.draw_networkx_edges(W, pos,edge_color='blue',ax=axs[1],width=3,arrowsize=15,arrows=True, arrowstyle='->')
nx.draw_networkx_labels(W, pos,ax=axs[1])
nx.draw_networkx_edge_labels(W, pos, edge_labels=edge_labels,label_pos=0.5,font_size=12,font_weight='bold',ax=axs[1])
fig.axes[1].set_title("Max Flow Graph")
plt.suptitle("Calculating Maximum Flow")
plt.show()
