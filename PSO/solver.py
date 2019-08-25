import copy
import problem as prbl

class Solver:

    def __init__(self, problem, path):
        self.problem = copy.deepcopy(problem)
        self.graph = problem.graph
        self.path = path
        self.obstacles_on_path = []
        self.t = 0

        for node in path:
            if node in problem.obstacles:
                self.obstacles_on_path.append(node)


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

        for obstacle in self.obstacles_on_path:
            moves.extend(self.possible_obstacle_moves(obstacle))

        return moves

    def possible_moves(self):
        moves = []
        moves.extend(self.possible_robot_moves())
        moves.extend(self.possible_obstacles_moves())

        return moves

    def solve(self, problem,path):

        queue = [[]]
        graph = problem.graph.copy()
        while queue:
            moves = queue.pop(0)
            #print(moves)
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
            if p.target == p.robot:
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                return moves
            sol = Solver(p,path)
            possible_moves = sol.possible_moves()


            for move in possible_moves:
                new_moves  = copy.copy(moves)
                new_moves.append(move)
                queue.append(new_moves)

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
