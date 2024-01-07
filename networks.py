import networkx as nx
import pylab as P
import matplotlib.pyplot as plt
print("hello")
G=nx.Graph()
G=nx.DiGraph()
G=nx.MultiGraph()
G=nx.MultiDiGraph()
G.add_edge(1,2) # default edge data=1
G.add_edge(2,3,weight=0.9)
elist=[('a','b',5.0),('b','c',3.0),('a','c',10.0),('c','d',7.3)]
G.add_weighted_edges_from(elist)
print(G)
nx.draw(G)
#plt.draw()
plt.show()
print(nx.dijkstra_path(G,'a','d'))
import networkx as nx

from graphilp.imports import networkx as imp_nx
from graphilp.partitioning import min_vertex_coloring as vtx
G_init = nx.cycle_graph(n=5)
G = imp_nx.read(G_init)
m = vtx.create_model(G)
m.optimize()
color_to_node, node_to_color = vtx.extract_solution(G, m)