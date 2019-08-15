import networkx as nx
import matplotlib.pyplot as plt
import shortest as sh
from cvorKlasa import Cvor

from matplotlib import animation

def get_node_by_name(g, name):
    for node in list(g.nodes):
        if node.name == name:
            return node
    return None

def print_path(path):
    s = ""
    for node in path:
        s = s + node.name
    return s

def topt(g, path, n1):
    start = get_node_by_name(g, 't')
    print(start)
    results =  {}
    path.remove(start)
    # u queue ide cvor, path, broj prepreka i broj rupa
    visited, queue = path, [(start, [start], 0, 0)]
    print(visited)
    while queue:
        (node, search_path, obstacles, holes)  = queue.pop(0)
        if node not in visited:
            visited.append(node)
            adjacent = g.adj[node]
            for neighbor in adjacent:
                if neighbor not in visited:
                    if neighbor.obstacle:
                        queue.append((neighbor, search_path + [neighbor], obstacles+1, holes))
                    if neighbor.is_hole():
                        if (obstacles == 0):
                            holes = holes+1
                            results[holes] = search_path + [neighbor]
                        else:
                            obstacles = obstacles -1

                        queue.append((neighbor, search_path + [neighbor], obstacles, holes))

    return results

# kad se poziva, edge je poslednja grana iz path
#def minOpt(g, path, edge, n1, n2, n3):



#    return 0

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

obstacles = ['b','c','e','f','g','t']

g = nx.Graph()

for node in nodes:
    c = Cvor(node, node in obstacles, node == 's')
    g.add_node(c)

for edge in edges:
    source = get_node_by_name(g, edge[0])
    dest = get_node_by_name(g, edge[1])
    g.add_edge(source, dest)

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
    for node1 in g.nodes:
        colors.append(node1.color())
    return colors

pos=nx.spring_layout(g)
def init():
    nx.draw_networkx(g, pos=pos,  with_labels=True, node_color=set_colors(), font_weight='bold')
    return

def move(m):
    source = get_node_by_name(g, m[0])
    dest = get_node_by_name(g, m[1])
    dest.robot = source.robot
    dest.obstacle = source.obstacle
    source.robot = False
    source.obstacle = False



def animate(i):
    move(moves[i])
    ax.clear()
    nx.draw_networkx(g, pos=pos,  with_labels=True, node_color=set_colors(), font_weight='bold'   )

res = sh.dijekstra(g, get_node_by_name(g, 's'),get_node_by_name(g,'s'))

fig, ax = plt.subplots(figsize=(6,4))


ani = animation.FuncAnimation(fig, animate, frames=len(moves), init_func=init,
                              interval=400, repeat=False)

for path in nx.all_simple_paths(g,get_node_by_name(g, 's'),get_node_by_name(g,'t'),10000):
#    print(topt(g, path, 1))
#    for node in path:
    #   print(node)

    d = topt(g, path, 1)
    for k in d:
        print(str(k) + print_path(d[k]))



plt.show()
