import networkx as nx
import matplotlib.pyplot as plt

# Create a directed graph
Directed_Graph = {
    '1': {'2': '22,25', '3': '24,10'},
    '2': {'3': '30,15', '4':'4,50', '5':'120,20'},
    '3': {'4': '31,5'},
    '4': {'5': '18,10'},    
}

# Create a DiGraph object
G = nx.DiGraph()

# Add nodes and edges from the Directed_Graph
for node in Directed_Graph:
    G.add_node(node)
    for edge, weight in Directed_Graph[node].items():
        G.add_edge(node, edge)

# Define the layout for the graph
pos = nx.spring_layout(G)
pos = { '1': (0, 30), '2': (3, 40), '3': (3, 20),'4': (6, 30),'5': (9, 30),'F': (20, 30),'G': (20, 20),'H': (30, 30)} 
# Draw the graph
nx.draw(G, pos, with_labels=True, node_size=1000,edge_color='black', node_color='white',arrowstyle="->",linewidths=2, edgecolors='#000000', font_size=20,font_weight='bold', font_color='black',  width=2, arrowsize=20)

# Add edge labels
#edge_labels = {(n1, n2): d['weight'] for n1, n2, d in G.edges(data=True)}
nx.draw_networkx_edges(G, pos,edge_color='black',style='solid',width=3,arrowsize=15,arrowstyle="->")
#nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.5,font_size=20,font_weight='bold')

# Display the graph
plt.show()