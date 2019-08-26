import copy
import problem as prbl
import networkx as nx
import heapq as heap
import random as rnd
class Solver:

    def __init__(self, problem):
        self.problem = copy.deepcopy(problem)
        self.graph = problem.graph

    def possible_robot_moves(self):
        robot_node = self.problem.robot
        robot_neighbors = self.graph.adj[robot_node]
        moves = []
        for neighbor in robot_neighbors:
            if self.problem.is_hole(neighbor):
                    moves.append((robot_node, neighbor, 1))
        return moves

    def possible_obstacle_moves(self, obstacle):

        obstacle_neighbors =  self.graph.adj[obstacle]
        moves = []
        for neighbor in obstacle_neighbors:
            if self.problem.is_hole(neighbor) and neighbor != self.problem.robot:
                moves.append((obstacle, neighbor, 1))
            else:
                if neighbor != self.problem.robot:
                    moves.extend(self.find_nearest_hole(self.graph, neighbor))

        return moves

    def possible_obstacles_moves(self):
        moves = []
        for obstacle in self.problem.obstacles:
            moves.extend(self.possible_obstacle_moves(obstacle))
        return moves

    def possible_moves(self):
        moves = []
        moves.extend(self.possible_robot_moves())
        moves.extend(self.possible_obstacles_moves())

        return moves


    def state(self,p):
        ob = p.obstacles[:]
        ob.sort()
        st = "#".join(ob)
        return ( st , p.robot)

    def fitnes_fun(self, graph, obstacles, robot, target, moves):
        shortest = nx.shortest_path(graph,robot,target)
        score = -len(shortest)- moves
        for obstacle in obstacles:
            if obstacle in shortest:
                score = score - 3
        return -score

    pop_size = 150
    elite= 5
    best=0.85
    mutation_probs = [0.01,0.05]
    def mutation(self,mutation_type,moves,graph,obstacles,r):
        newmoves =moves[0:rnd.randint(0,len(moves))]
        return newmoves


    def do_genetic(self,queue,graph,obstacles,r,visited):
        newqueue = []
        for i in range(self.pop_size+1):
            if (rnd.random()>self.best):
                score,moves,round = queue.pop(rnd.randint(0, len(queue)-1))
            else:
                score,moves,round = queue.pop(0)
            newqueue.append((score,moves,round))

        if(rnd.random()<=self.mutation_probs[0]):
            oldscore,oldmoves,oldround = newqueue.pop(rnd.randint(0,self.pop_size-1))
            newmoves = self.mutation(0,moves,graph,obstacles,r)
            heap.heappush(newqueue,(-100000,newmoves,oldround))
        queue=[]
        for e in newqueue:
            if (("#".join(obstacles),r) not in visited ): # zbog mutacija je moguce
                heap.heappush(queue,e)
            else:
                print("Have this one ...and random")
                score,moves,round = queue.pop(rnd.randint(0, len(queue)-1))
                heap.heappush(queue,(-score,moves,round))
        return queue

    def solve_genetic(self,problem):
        r = 0
        visited = set([])
        queue =  [(-10000,[],r)]
        graph = problem.graph.copy()
        while True:
            if ( len(queue)>2*self.pop_size):
                queue=self.do_genetic(queue,graph,self.problem.obstacles,self.problem.robot,visited)
            score,moves,round = heap.heappop(queue)
            if (round % 10000 == 0):
                print ("Round = "  + str(round))
                print ("Visited = " + str(len(visited)))
                print("Score = " + str(score))
            p = prbl.Problem(nodes=graph.nodes,
                             edges=graph.edges,
                             obstacles = [])
            p.graph = problem.graph.copy()
            p.start = problem.start
            p.target = problem.target
            p.robot = problem.robot
            for o in problem.obstacles:
                p.obstacles.append(o)
            p.moves(moves)
            st = self.state(p)

            if ( st not in visited):
                visited.add(st)
                if p.target == p.robot:
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    return moves
                score = self.fitnes_fun(self.graph,p.obstacles,p.robot,p.target,len(moves))
                sol = Solver(p)
                possible_moves = sol.possible_moves()
                for move in possible_moves:
                    new_moves  = copy.copy(moves)
                    new_moves.append(move)
                    r = r + 1
                    heap.heappush(queue,(score,new_moves,r ))
                    #queue.append((score,new_moves,r ) )

    def solve_heap(self,problem):
        r = 0
        visited = set([])
        queue =  [(-10000,[],r)]
        graph = problem.graph.copy()
        while queue:
            score,moves,round = heap.heappop(queue)
            if (round % 10000 == 0):
                print ("Round = "  + str(round))
                print ("Visited = " + str(len(visited)))
                print("Score = " + str(score))
            p = prbl.Problem(nodes=graph.nodes,
                             edges=graph.edges,
                             obstacles = [])
            p.graph = problem.graph.copy()
            p.start = problem.start
            p.target = problem.target
            p.robot = problem.robot
            for o in problem.obstacles:
                p.obstacles.append(o)
            p.moves(moves)
            st = self.state(p)

            if ( st not in visited):
                visited.add(st)
                if p.target == p.robot:
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    return moves
                score = self.fitnes_fun(self.graph,p.obstacles,p.robot,p.target,len(moves))
                sol = Solver(p)
                possible_moves = sol.possible_moves()
                for move in possible_moves:
                    new_moves  = copy.copy(moves)
                    new_moves.append(move)
                    r = r + 1
                    heap.heappush(queue,(score,new_moves,r ))
                    #queue.append((score,new_moves,r ) )

    def solve_brute_force(self, problem):
        r = 0
        visited = set([])
        queue = [([],r)]
        graph = problem.graph.copy()
        while queue:
            moves,round = queue.pop(0)
            if (round % 10000 == 0):
                print ("Round = "  + str(round))
                print ("Visited = " + str(len(visited)))

            p = prbl.Problem(nodes=graph.nodes,
                             edges=graph.edges,
                             obstacles = [])
            p.graph = problem.graph.copy()
            p.start = problem.start
            p.target = problem.target
            p.robot = problem.robot
            for o in problem.obstacles:
                p.obstacles.append(o)
            p.moves(moves)
            st = self.state(p)
            if ( st not in visited):
                visited.add(st)
                if p.target == p.robot:
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    return moves
                sol = Solver(p)
                possible_moves = sol.possible_moves()
                for move in possible_moves:
                    new_moves  = copy.copy(moves)
                    new_moves.append(move)
                    r = r + 1
                    queue.append((new_moves,r ) )

    def find_nearest_hole(self, graph, start):

        visited, queue = [], [(start, [start])]
        results = []

        while queue:
            (node, search_path) = queue.pop(0)

            if node not in visited:

                visited.append(node)
                adjacent = graph.adj[node]

                for neighbor in adjacent:
                    if neighbor in self.problem.obstacles:
                        if neighbor not in visited:
                            queue.append((neighbor, search_path + [neighbor]))
                    else:
                        if neighbor != self.problem.robot:
                            results.append(search_path + [neighbor])

        moves = []
        for res in results:
            moves.append((res[0], res[-1], len(res)-1))

        return moves
