import problem as prbl

class ProblemGenerator:

    def __init__(self):
        self.testproblems  = {

        "p0" : {
            "nodes":  ['a','s','x','y',
                'b','c','e','f',
                'd','g','h','t',
                'i'],
            "edges" : [('a','s'),
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
                      ],

        "obstacles" : ['b','c','e','f','g','t'],

        "start" : 's',

        "target" : 't'
        },



        "p1" : {
            "nodes":  ['a','s','x','y',
                'b','c','e','f',
                'd','g','h','t',
                'i', 'j', 'z', 'k'],

            "edges" : [('a','s'),
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
                    "target": 't'
              },

        "p3": {
                "nodes": ['s', 'a', 'b', 'c', 'd', 't'],
                "edges": [('s', 'a'), ('a', 'b'), ('a', 'c'), ('b', 'd'),('b', 't')],
                "obstacles": ['a', 'b'],
                "start": 's',
                "target": 't'
        },

        "p4": {
            "nodes": ['s','a','b','c','t','a1','b1','c1'],
            "edges": [('s','a'),('a','b'),('b','c'),('c','t'),('a','a1'),('b','b1'),('c','c1')],
            "obstacles": ['a','b','c'],
            "start": 's',
            "target": 't'
            }

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
