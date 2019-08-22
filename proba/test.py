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
#    print('topt start: {}'.format(start))
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
    #print('Preflow start: {}'.format(start))
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
    #print('\nPostflow path: {}'.format(path_str(path)))

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
                    #print('Neighbor: {}'.format(neighbor))
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

                if neighbor not in visited and level <= 2:
                    queue.append((neighbor, search_path + [neighbor], level))

    return results

# vraca bipartitan graf
def bipartitive_graph(g, source, destination):

    bi_graph = nx.Graph()

    for source_node in source:
        if source_node.obstacle == True:
            for dest_node in destination:
                if dest_node.is_hole() or dest_node.robot:
                    shortest = nx.shortest_path(g, source_node, dest_node)
                    bi_graph.add_edge(source_node, dest_node, weight = 1000-len(shortest), shortest_path = shortest)

    return bi_graph

# vrace deo grafa kad se odsece grana (node1, node2), bez node2
def tree_from_edge(g, node1, node2):

    result = [node1]
    start = node1

    visited, queue = [node2], [start]

    while queue:
        node  = queue.pop(0)
        if node not in visited:
            visited.append(node)
            adjacent = g.adj[node]
            for neighbor in adjacent:
                if neighbor not in visited:
                    queue.append(neighbor)
                    result.append(neighbor)
    return result

def match_n(g,source,destination,max_n):
    bi_graph = nx.Graph()
    for dest_node in destination:
        if dest_node != source and (dest_node.is_hole() or dest_node.robot) :
            shortest = nx.shortest_path(g, source, dest_node)
            for i in range(max_n):
                c = Cvor('t',True,False)
                bi_graph.add_edge(c, dest_node, weight = 1000-len(shortest), shortest_path = shortest)

    return nx.max_weight_matching(bi_graph), bi_graph


nodes = {'a','s','x','y',
            'b','c','e','f',
            'd','g','h','t',
            'i', 'j', 'z', 'k'}

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
          ('x', 'z'),
          ('z', 'k')
 ]

obstacles = ['b','c','e','f','g','t', 'h']

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


def topt_1(g, path):

    plans = []
    len_path = len(path)

    right = tree_from_edge(g,path[-1], path[-2])
    match, topt_graph = match_n(g, path[-1], right, len_path)

    # prvi slucaj
    plans.append(([], 0, 0, 0))

    print(match)
    for i in range(len_path):
        moves = []
        for m in match:
            weight = 999 - topt_graph.edges[m[0], m[1]]['weight']
            print(weight)
            if weight <= i:
                shortest = topt_graph.edges[m[0], m[1]]['shortest_path']
                shortest = shortest.reverse()
                print(shortest)
                for i in len(shortest):
                    if path[i].obstacle:
                        moves.append((path[i], path[i-1]))

        plans.append((moves, i, 0, 0))

    return plans

for path in nx.all_simple_paths(g,get_node_by_name(g, 's'),get_node_by_name(g,'t'),10000):
#    print(topt(g, path, 1))

#    print('topt:')
#    for k in d:
#        print(str(k) + path_str(d[k]))

#    print('\npath:')
#    print(path_str(path))

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
    print('B-------S:')
    print(path_str(tree_from_edge(g, get_node_by_name(g, 'b'), get_node_by_name(g, 's'))))

    print("S-------B:")
    print(path_str(tree_from_edge(g, get_node_by_name(g, 's'), get_node_by_name(g, 'b'))))

    b_paths = backup_paths(g, path)
#    for b in b_paths:
#        print(path_str(b))

    left = tree_from_edge(g, get_node_by_name(g, 's'), get_node_by_name(g, 'b'))
    right = tree_from_edge(g, get_node_by_name(g, 'b'), get_node_by_name(g, 's'))

    bi = bipartitive_graph(g, right, left)
#    nx.draw_networkx(bi, with_labels=True, font_weight='bold')
    match = nx.max_weight_matching(bi)
    for m in match:
        weight = bi.edges[m[0], m[1]]['weight']-1
        shortest_path_edge_bi = bi.edges[m[0], m[1]]['shortest_path']
        print(1000 - weight)
        print(path_str(shortest_path_edge_bi))
        print(m[0].name + '---->' + m[1].name)

    print(topt_1(g, path))

plt.show()
