import networkx as nx
import matplotlib.pyplot as plt

def plt_graph(graph):
        colors = []
        ecolors = []
        pos = nx.spring_layout(graph)
        for node in graph.nodes:
            if 'color' in graph.nodes[node]:
                    colors.append(graph.nodes[node]['color'])
            else:
                    colors.append('w')
        for u,v in graph.edges:
            if 'color' in  graph.edges[u,v]:
                ecolors.append(graph.edges[u,v]['color'])
            else:
                ecolors.append('y')

        nx.draw_networkx(graph,pos=pos,
                         with_labels=True,
                         title="LAST",
                         edge_color=ecolors,
                         node_color=colors,
                         font_weight = 'bold')

        plt.show()
