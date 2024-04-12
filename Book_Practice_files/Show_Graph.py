# Show_Graph.py  module
def Show(Primary_Graph,Solution_Graph,main_title,sub_title1,sub_title2,edgeval1,edgeval2):
    import networkx as nx
    import matplotlib.pyplot as plt
    G = nx.DiGraph()
    fig, axs = plt.subplots(ncols=2, figsize=(12, 5), gridspec_kw={'width_ratios': [8,  8]})
    for node, edges in Primary_Graph.items():
        for neighbor, weight in edges.items():
            G.add_edge(node, neighbor, weight=weight)
    pos = { 'A': (0, 30), 'B': (10, 40), 'C': (10, 30),'D': (10, 20),'E': (20, 40),'F': (20, 30),'G': (20, 20),'H': (30, 30)} 
    nx.draw_networkx_nodes(G, pos,node_color='white',linewidths=1,alpha=1, edgecolors='#000000',ax=axs[0])
    nx.draw_networkx_edges(G, pos,edge_color='brown',ax=axs[0])
    nx.draw_networkx_labels(G, pos,ax=axs[0])
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edgeval1,label_pos=0.5,font_size=12,font_weight='bold',ax=axs[0])
    fig.axes[0].set_title(sub_title1)
    Q=nx.Graph()
    for node, edges in Solution_Graph.items():
        for neighbor, weight in edges.items():
            if weight>0:
                Q.add_edge(node, neighbor, weight=weight)    
    nx.draw_networkx_nodes(G, pos,node_color='white',linewidths=1,alpha=1, edgecolors='#000000',ax=axs[1])
    nx.draw_networkx_edges(G, pos,edge_color='brown',ax=axs[1])
    nx.draw_networkx_labels(G, pos,ax=axs[1])
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edgeval1,label_pos=0.5,font_size=12,font_weight='bold',ax=axs[0])
    nx.draw_networkx_nodes(Q, pos,node_color='white',linewidths=2,alpha=1, edgecolors='#000000',ax=axs[1])
    nx.draw_networkx_edges(Q, pos,edge_color='blue',ax=axs[1],width=3,arrowsize=15,arrows=True, arrowstyle='->')
    nx.draw_networkx_labels(Q, pos,ax=axs[1])
    nx.draw_networkx_edge_labels(Q, pos, edge_labels=edgeval2,label_pos=0.5,font_size=12,font_weight='bold',ax=axs[1])
    fig.axes[1].set_title(sub_title2)
    plt.suptitle(main_title)
    plt.show()