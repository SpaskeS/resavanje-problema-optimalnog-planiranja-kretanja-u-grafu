import networkx as nx
import matplotlib.pyplot as plt
import shortest as sh

from matplotlib import animation

nodes = {'a','s','x','y',
            'b','c','e','f',
            'd','g','h','t',
            'i'}

edges = [ ('a','s'),
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
          ('h','i')
 ]

nodes_dict = {}

obstacles = ['b','c','e','f','g','t']


g = nx.Graph()

for node in nodes:
    nodes_dict[node] = None
    g.add_node(node)


for obstacle in obstacles:
    nodes_dict[obstacle] = 'O'

nodes_dict['s'] = 'R'

g.add_edges_from(edges)


moves = [('s','a'),('b','s'),('s','y'),
         ('y','x'),('c','b'),('b','s'),
         ('s','y'),('t','h'),('h','i'),
         ('g','t'),('t','h'),('a','s'),
         ('s','b'),('b','c'),('f','g'),
         ('g','t'),('e','f'),('f','g'),
         ('c','e'),('e','f'),('f','d'),
         ('g','f'),('f','e'),('e','c'),
         ('t','g'),('g','f'),('f','e'),
         ('d','f'),('f','g'),('g','t')
]


def set_colors():
    colors = []
    for node in g:
        if nodes_dict[node] == 'O':
            colors.append('r')
        if nodes_dict[node] == 'R':
            colors.append('g')
        if nodes_dict[node] == None:
            colors.append('w')
        if nodes_dict[node] == 'T':
            colors.append('y')
    
    return colors

pos=nx.spring_layout(g)
def init():
    nx.draw_networkx(g, pos=pos,  with_labels=True, node_color=set_colors(), font_weight='bold')
    return

def move(m):
    nodes_dict[m[1]] = nodes_dict[m[0]]
    nodes_dict[m[0]] = None
    

def animate(i):
    move(moves[i])
    ax.clear()
    nx.draw_networkx(g, pos=pos,  with_labels=True, node_color=set_colors(), font_weight='bold'   )
   

    

res = sh.dijekstra(g,'s','t')



fig, ax = plt.subplots(figsize=(6,4))


ani = animation.FuncAnimation(fig, animate, frames=len(moves), init_func=init,
                              interval=400, repeat=False)



for path in nx.all_simple_paths(g,'s','t',10000):
    print(path)


    

    
plt.show()
