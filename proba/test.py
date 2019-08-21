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

def path_str(path):
    s = ''
    for node in path:
        s = s + node.name
    return s

def topt(g, path):
    start = get_node_by_name(g, 't')
    print('topt start: {}'.format(start))
    results =  {}
    path.remove(start)
    # u queue ide cvor, path, broj prepreka i broj rupa
    visited, queue = path, [(start, [start], 0, 0)]
    #print(visited)
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

def preflow(g, path):
    start = path[-1]
    print('Preflow start: {}'.format(start))
    results =  {}
    path.remove(start)
    deep = 0
    # u queue ide cvor, path, broj prepreka i broj rupa
    visited, queue = path, [(start, [start], 0, 0)]
    #print(visited)
    while queue:
        (node, search_path, obstacles, holes)  = queue.pop(0)
        deep += 1
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
                                results[holes] = (search_path + [neighbor], deep)
                            else:
                                obstacles = obstacles -1

                            queue.append((neighbor, search_path + [neighbor], obstacles, holes))

    return results

def postflow(g, path):
    start = path[-1]
    print('\nPostflow path: {}'.format(path_str(path)))

    results =  {}
    path.remove(start)
    deep = 0
    # u queue ide cvor, path, broj prepreka i broj rupa
    visited, queue = [], [(start, [start], 0, 0)]
    #print(visited)

    while queue:
        (node, search_path, obstacles, holes)  = queue.pop(0)
        deep += 1
        if node not in visited:
            visited.append(node)
            adjacent = g.adj[node]

            for neighbor in adjacent:
                if neighbor not in visited and neighbor in path:
                    print('Neighbor: {}'.format(neighbor))
                    if neighbor.obstacle:
                        queue.append((neighbor, search_path + [neighbor], obstacles+1, holes))
                    if neighbor.is_hole() or neighbor.robot:
                        if (obstacles == 0):
                            holes = holes+1
                            results[holes] = (search_path + [neighbor], deep)
                        else:
                            obstacles = obstacles -1

                        queue.append((neighbor, search_path + [neighbor], obstacles, holes))
    return results

# kad se poziva, edge je poslednja grana iz path
def minOpt(g, path, edge, n1, n2, n3):

    edge_index = path.index(edge)

    start = path[0]
    pflow = preflow(g, path)

    plan = (0,edge,[[],[],[]])    # (cost, edge, [[n1] [n2] [n3]])

    for node in path:
        if len(g.adj[node]) > 2:
            node.fork = True


    if path[edge_index-1].fork == True:
        plan2 = minOpt(g, list(path).remove(edge), path[edge_index-1],n1,n2,n3)
    else:
        if pflow.contains(n1):
            cost, edge, n1, n2, n3 = plan
            plan = (cost+pflow[n1][1], edge, n1, n2, n3)
        if path[edge_index].fork == True:
            return 1

    return 0

def backup_paths(g, path):
    start = path[0]

    results = [[]]
    deep = 0

    if len(g.adj[start]) > 2:
        fork = True
    else:
        fork = False

    path.remove(start)
    visited, queue = path, [(start, [start], deep)]

    while queue:
        (node, search_path, level) = queue.pop(0)
        results.append(search_path)

        if node not in visited:
            visited.append(node)
            adjacent = g.adj[node]

            if fork == True:
                level += 1

            if len(adjacent) > 2:
                fork = True

            for neighbor in adjacent:
                print('ajdacents: {}, level {}'.format(str(neighbor), level))

                if neighbor not in visited and level <= 2:
                    queue.append((neighbor, search_path + [neighbor], level))

    return results


def backup(g, path):
    start = path[0]
    print('backup start: {}'.format(start))
    results = []
    deep = 0

    if len(g.adj[start]) > 2:
        fork = True
    else:
        fork = False

    path.remove(start)
    visited, queue = path, [(start, [start], deep)]

    while queue:
        (node, search_path, level) = queue.pop(0)

        if node not in visited:
            visited.append(node)
        #    results = search_path
            adjacent = g.adj[node]

            if fork == True:
                level += 1

            if len(adjacent) > 2:
                fork = True

            for neighbor in adjacent:
                print('ajdacents: {}, level {}'.format(str(neighbor), level))

                if neighbor not in visited and level <= 2:
                    results.append(neighbor)
                    queue.append((neighbor, search_path + [neighbor], level))

    results.reverse()

    return results

nodes = {'a','s','x','y',
            'b','c','e','f',
            'd','g','h','t',
            'i', 'j', 'z'}

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
          ('h','i'),
          ('i', 'j'),
          ('x', 'z')
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

fig, ax = plt.subplots(figsize=(6,4))


ani = animation.FuncAnimation(fig, animate, frames=len(moves), init_func=init,
                              interval=400, repeat=False)

for path in nx.all_simple_paths(g,get_node_by_name(g, 's'),get_node_by_name(g,'t'),10000):
#    print(topt(g, path, 1))

    d = topt(g, list(path))
    print('topt:')
    for k in d:
        print(str(k) + path_str(d[k]))

    print('\npath:')
    print(path_str(path))

    #opt = minOpt(g, list(path), 0,0,0)
    #print(opt)

#    print('\nbackup:')
#    print(path_str(backup(g, list(path))))
#    print('\n')




#    bs = backup(g, list(path))
    #pstflow = postflow(g, list(bs) + list(path))

    #print('\npostflow:')
#    for k in pstflow:
    #    print(str(k) + path_str(pstflow[k]))

    b_paths = backup_paths(g, path)
    for b in b_paths:
        print(path_str(b))


plt.show()
