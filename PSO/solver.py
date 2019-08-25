import copy
import problem as prbl

class Solver:

    def __init__(self, problem, path):
        self.problem = copy.deepcopy(problem)
        self.graph = problem.graph
        self.path = path
        self.t = 0


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

    def solve_brute_force(self, problem,path):
        r = 0
        visited = set([])
        queue = [([],r)]
        graph = problem.graph.copy()
        while queue:
            moves,round = queue.pop(0)
            if (round % 1000 == 0):
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
                sol = Solver(p,path)
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
