import problem as prbl

class ProblemGenerator:

    def __init__(self):
        self.testproblems  = { "p1" : {
            "nodes":  ['a','s','x','y',
                'b','c','e','f',
                'd','g','h','t',
                'i', 'j', 'z', 'k'],
        "edges" : [     ('a','s'),
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
                      ('z', 'k')],
        "obstacles" : ['b','c','e','f','g','t', 'h'],
        "start" : 's',
        "target" : 't'
        },
                "p2": {
                    "nodes": ['s','a','t', 'z', 'k'],
                    "edges": [ ('s','a'),('a','t'), ('a', 'z'), ('z', 'k')],
                    "obstacles" : ['a'],
                    "start": 's',
                    "target": 't'}

        }

    def getByName(self, name):

        if(not name in self.testproblems ):
			raise RuntimeError("There is no problem with name " + name)
        p = self.testproblems[name]
        return prbl.Problem(nodes=p["nodes"],
                            edges=p["edges"],
                            start=p["start"],
                            target=p["target"],
                            obstacles=p["obstacles"]
        )
