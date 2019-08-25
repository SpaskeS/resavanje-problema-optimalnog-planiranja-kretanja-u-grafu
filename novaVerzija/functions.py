import networkx as nx
import matplotlib.pyplot as plt
from cvorKlasa import Cvor
import graph as gr

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

def match_n(g, source, destination, max_n):

    bi_graph = nx.Graph()
    for dest_node in destination:
        if dest_node != source and (dest_node.is_hole() or dest_node.robot) :
            shortest = nx.shortest_path(g, source, dest_node)
            for i in range(max_n):
                c = Cvor('t', True, False)
                bi_graph.add_edge(c, dest_node, weight = 1000-len(shortest), shortest_path = shortest)

    return nx.max_weight_matching(bi_graph), bi_graph


def topt_1(g, path):

    plans = []
    len_path = len(path)

    right = tree_from_edge(g, path[-1], path[-2])
    match, topt_graph = match_n(g, path[-1], right, len_path)

    print('match size: ' + str(len(match)) + '\n')

    # prvi slucaj
    plans.append(([], 0, 0, 0, 0))

    for m1 in match:
        cost = 0
        i = 0
        moves = []
        (path_m1, weight_m1, shortest_m1) = get_match_data(topt_graph, m1)
        for m in match:
            (path_name, weight, shortest) = get_match_data(topt_graph, m)

            if weight <= weight_m1:
                i += 1
                cost += weight

                print(path_name + ' ' + gr.path_str(shortest) + ' ' + str(weight))
                moves.append((path[-1], shortest[-1]))

        plans.append((moves, i, 0, 0, cost))

    print('\n')
    return plans

def print_plans(plans):

    print('TOPT plans: ')

    for plan in plans:
        moves, n1, n2, n3, cost = plan
        print('PLAN: ')
        s = '['
        for pair in moves:
            s = s + ' (' + pair[0].name + ', ' + pair[1].name + ') '

        print(s + ']')
        print('ns: ' + str(n1) + ' ' + str(n2) + ' ' + str(n3))
        print('cost: ' + str(cost) + '\n')

def get_match_data(bi, m):
    path_name = ''
    path_name = path_name.join(m[0].name + ' --> ' + m[1].name)

    weight = 999 - bi.edges[m[0], m[1]]['weight']

    shortest_path = bi.edges[m[0], m[1]]['shortest_path']

    return(path_name, weight, shortest_path)



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

    (node1, node2) = edge



    return 0
