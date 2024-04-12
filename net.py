import networkx as nx
import matplotlib.pyplot as plt

# Create a sample graph
G = nx.Graph()
G.add_edges_from([(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (5, 9)])

# Calculate the Shortest Paths using Dijkstra's algorithm
shortest_paths = nx.single_source_dijkstra_path(G, source=5)

# Create a new graph for the Shortest Path Tree
shortest_path_tree = nx.Graph()
for node, path in shortest_paths.items():
    for i in range(len(path) - 1):
        shortest_path_tree.add_edge(path[i], path[i + 1])

# Draw the graph and the Shortest Path Tree
pos = nx.spring_layout(G)  # Layout for the nodes
nx.draw(G, pos, with_labels=True, node_size=1000, node_color='lightblue', font_size=10, font_weight='bold')
nx.draw_networkx_edges(shortest_path_tree, pos, edge_color='r', width=2)

# Display the graph with the Shortest Path Tree
plt.title('Shortest Path Tree for Sample Graph')
plt.axis('off')
plt.show()