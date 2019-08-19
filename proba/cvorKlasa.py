class Cvor:

    def __init__(self, name, obstacle, robot):
        self.name = name
        self.obstacle = obstacle
        self.robot = robot
        self.fork = False

    def color(self):
        if self.obstacle == True:
            return 'r'
        if self.robot == True:
            return 'g'
        if self.is_hole():
            return 'w'
        if self.name == 't':
            return 'y'

    def is_hole(self):
        return not self.obstacle and not self.robot

    def __str__(self):
        return self.name
