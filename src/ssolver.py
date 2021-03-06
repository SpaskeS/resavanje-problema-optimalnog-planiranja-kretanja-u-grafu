import heapq as heap
import networkx as nx
import copy
import random
def remove_jumps(moves):

    res = []

    for move in moves:
        if move[2] > 1:
            move[3].reverse()
            res.extend(make_moves_from_path(move[3]))
        else:
            res.append(move)

    return res


def make_moves_from_path(path):

    moves = []
    p = path[:]

    for i in range(len(p)-1):
        moves.append((p[i+1], p[i], 1, [p[i+1], p[i]]))
    return moves


def find_nearest_hole(o,r,graph, start):
    visited, queue = [], [(start, [start])]
    results = []

    while queue:
        (node, search_path) = queue.pop(0)

        if node not in visited:
            visited.append(node)

            adjacent = graph.adj[node]

            for neighbor in adjacent:
                if neighbor in o:
                    if neighbor not in visited:
                        queue.append((neighbor, search_path + [neighbor]))
                else:
                    if neighbor != r:
                        results.append(search_path + [neighbor])

    moves = []
    for res in results:

        moves.append((res[0], res[-1], len(res)-1, res))
    return moves

def move_robot(o,r,graph,node_from,node_to):
    obstacles = o[:]
    robot = r
    if not node_from == r:
        raise RuntimeError('node_from is not robot ' + node_from)

        if node_to in obstacles:
            raise RuntimeError('node_to is obstacle ' + node_to)
    robot = node_to
    return (obstacles,robot)

def move_obstacle(o,r,graph,node_from,node_to):
    obstacles = o[:]
    robot  = r
    if node_from not in obstacles:
        raise RuntimeError('node_from is not obstacle ' + node_from)
    if node_to in obstacles:
        raise RuntimeError('node_to is obstacle ' + node_to)

    if node_to == robot:
        raise RuntimeError('node_to is robot' + node_to)

    obstacles.append(node_to)
    obstacles.remove(node_from)

    return(obstacles,robot)

def make_move(o,r,graph,node_from,node_to):

    if node_from == None:
        return (o, r)

    if( r == node_from):
        return move_robot(o,r,graph,node_from,node_to)
    if ( node_from in o):
        return move_obstacle(o,r,graph,node_from,node_to)

    raise RuntimeError('Cant move from ' + node_from)

def make_moves(o,r,graph,moves):
    obstacles= o[:]
    robot = r
    for move in moves:
        obstacles,robot = make_move(obstacles,robot,graph,move[0],move[1])
    return (obstacles,robot)

def is_hole(o, r, node):
    if (node not in o):
        return True
    return False

def possible_robot_moves(o, r, graph):
    moves=[]
    robot_node = r
    robot_neighbors = graph.adj[r]

    for neighbor in robot_neighbors:
        if is_hole(o,r,neighbor):
            moves.append((robot_node, neighbor, 1, [robot_node, neighbor]))
    return moves

def possible_obstacle_moves(o,r,graph,obstacle):
    obstacle_neighbors =  graph.adj[obstacle]
    moves = []

    for neighbor in obstacle_neighbors:
        if is_hole(o,r,neighbor) and neighbor != r:
            moves.append((obstacle, neighbor, 1, [obstacle, neighbor]))
        else:
            if neighbor != r:
                nh = find_nearest_hole(o, r, graph, neighbor)
                if len(nh) > 0:
                    moves.extend(find_nearest_hole(o,r,graph, neighbor))

    return moves

def possible_obstacles_moves(o,r,graph):
    moves = []
    for obstacle in o:
        moves.extend(possible_obstacle_moves(o,r,graph,obstacle))
    return moves

def possible_moves(o,r,graph):
    moves = []
    moves.extend(possible_robot_moves(o,r,graph))
    moves.extend(possible_obstacles_moves(o,r,graph))
    return moves


def color(o,r,graph,node,target,start):
        if (node in o and node == target):
            return 'c'
        if node in o:
            return 'r'
        if node == r:
            return 'b'
        if node == start:
            return 'y'
        if node == target:
            return 'g'
        return 'w'


def create_state(o, r):

    o.sort()
    return '-'.join(o) + ' ___ R = ' + r

#__________________________________________________________________________________

def fitness_fun_heap(graph, obstacles, robot, target, num_of_moves):
    shortest = nx.shortest_path(graph,robot,target)
    score = -len(shortest) - num_of_moves

    for obstacle in obstacles:
        if obstacle in shortest:
            score = score - 1

    return -score



def solve_heap(o,r,graph,t):
    round = 0
    visited = set([])
    queue= [(-1000,[],o,r)]
    while queue:
        score,moves,obstacles,robot = heap.heappop(queue)
        obstacles.sort()
        st = ('#'.join(obstacles),robot)
        if ( st not in visited ):
            visited.add(st)
            score = fitness_fun_heap(graph,obstacles,robot,t,len(moves))
            pm = possible_moves(obstacles,robot,graph)

            for move in pm:
                new_moves = moves[:]
                new_moves.append(move)
                newobstacles,newrobot = make_moves(obstacles,robot,graph,[move])
                if t == newrobot:
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    return new_moves

                round = round+1
                if (round % 100000 == 0):
                    print ("Visited = " + str(len(visited)))
                heap.heappush(queue,(score,new_moves,newobstacles,newrobot))





def solve_brute_force(o,r,graph,t):
    num_of_solutions = 0
    all_solutions = []

    round = 0
    visited = set([])
    queue = [([],o,r)]
    while queue:
        moves,obstacles,robot = queue.pop(0)
        obstacles.sort()
        st = ('#'.join(obstacles),robot)
        if ( st not in visited ):
            visited.add(st)

            pm = possible_moves(obstacles,robot,graph)
            for move in pm:
                new_moves = moves[:]
                new_moves.append(move)
                newobstacles,newrobot = make_moves(obstacles,robot,graph,[move])
                if t == newrobot:
                    all_solutions.append(new_moves)

                round = round+1

                if (round % 100000 == 0):
                    print ("Visited = " + str(len(visited)))
                queue.append((new_moves,newobstacles,newrobot))


    print('Number of solutions: ' + str(len(all_solutions)))

    best = min(all_solutions, key = lambda x : len(x))

    return best
