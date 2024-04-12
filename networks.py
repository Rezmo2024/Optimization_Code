import networkx as nx
import matplotlib.pyplot as plt
import numpy

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
for node, edges in Directed_Graph.items():
    for neighbor, weight in edges.items():
        G.add_edge(node, neighbor, weight=weight)

# Set the edge labels to the weight attribute
edge_labels = {(u, v): G[u][v]['weight'] for u, v in G.edges()}

# Plot the graph
#pos = nx.spring_layout(G)
pos = { 'A': (0, 30), 'B': (10, 40), 'C': (10, 30),'D': (10, 20),'E': (20, 40),'F': (20, 30),'G': (20, 20),'H': (30, 30)} 

nx.draw_networkx_nodes(G, pos,node_color='white',linewidths=1,alpha=1, edgecolors='#000000')
nx.draw_networkx_edges(G, pos,edge_color='brown')
nx.draw_networkx_labels(G, pos)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,label_pos=0.5,font_size=12,font_weight='bold')
#nx.draw(G, pos, node_color='#FFFFFF', edgecolors='#000000')
plt.axis("off")
plt.show()