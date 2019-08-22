import networkx as nx
import matplotlib.pyplot as plt
from cvorKlasa import Cvor
import fje as f
import graph as gr

from matplotlib import animation

nodes = {'a','s','x','y',
             'b','c','e','f',
             'd','g','h','t',
             'i', 'j', 'z', 'k'}

edges = [     ('a','s'),
              ('s','b'),
              ('x','y'),
              ('y','s'),
              ('f','d'),
              ('b','c'),
              ('c','e'),
              ('e','f'),
              ('f','g'),
              ('g','t'),
              ('t','h'),
              ('h','i'),
              ('i', 'j'),
              ('x', 'z'),
              ('z', 'k')]

obstacles = ['b','c','e','f','g','t', 'h']

moves = [('s','a'),('b','s'),('s','y'),
             ('y','x'),('c','b'),('b','s'),
             ('s','y'),('t','h'),('h','i'),
             ('g','t'),('t','h'),('a','s'),
             ('s','b'),('b','c'),('f','g'),
             ('g','t'),('e','f'),('f','g'),
             ('c','e'),('e','f'),('f','d'),
             ('g','f'),('f','e'),('e','c'),
             ('t','g'),('g','f'),('f','e'),
             ('d','f'),('f','g'),('g','t')]

g = gr.makeGraph(nodes, edges, obstacles)
pos = nx.spring_layout(g)

fig, ax = plt.subplots(figsize=(6,4))

def init():
    nx.draw_networkx(g, pos=pos,  with_labels=True, node_color= gr.set_colors(g), font_weight='bold')
    return

def animate(i):
    gr.move(moves[i],g)
    ax.clear()
    nx.draw_networkx(g, pos=pos,  with_labels=True, node_color = gr.set_colors(g), font_weight='bold')

ani = animation.FuncAnimation(fig, animate, frames=len(moves), init_func = init, interval=400, repeat=False)


def main():

    s = gr.get_node_by_name(g, 's')
    t = gr.get_node_by_name(g, 't')

    all_paths = nx.all_simple_paths(g, s, t, 10000)

    for path in all_paths:

        b_paths = f.backup_paths(g, path)
#        for b in b_paths:
#        print(path_str(b))

        left = f.tree_from_edge(g, gr.get_node_by_name(g, 's'), gr.get_node_by_name(g, 'b'))
        right = f.tree_from_edge(g, gr.get_node_by_name(g, 'b'), gr.get_node_by_name(g, 's'))

        print('tree B----->S:')
        print(gr.path_str(right))

        print('tree S----->B:')
        print(gr.path_str(left))
        print('\n')

        bi = f.bipartitive_graph(g, right, left)

        #nx.draw_networkx(bi, with_labels=True, font_weight='bold')

        match = nx.max_weight_matching(bi)

        for m in match:
            (path_name, weight, shortest_path_edge_bi) = f.get_match_data(bi, m)
            print(path_name + ' : ' + gr.path_str(shortest_path_edge_bi) + ', weight: ' + str(weight))


        print('\n')
        print('topt: ')
        #print(f.topt_1(g, path))

        plt.show()


if __name__ == '__main__':
    main()
