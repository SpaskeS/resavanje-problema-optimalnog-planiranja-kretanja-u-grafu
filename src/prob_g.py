import problem as prbl

class ProblemGenerator:

    def __init__(self):
        self.testproblems  = {

        "p9": {
            "nodes": ['s', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 't'],
            "edges": [('a', 'b'), ('a', 'c'), ('b', 'd'), ('b', 'e'), ('c', 'f'), ('c', 'g'), ('f', 'k'), ('f', 'l'), ('g', 'm'), ('g', 't'), ('d', 'h'), ('d', 'i'), ('e', 's'), ('e', 'j')],
            "obstacles":['a', 'b', 'c', 'e', 'g', 'd', 'f'],
            "start":'s',
            "target":'t'
        },

        "p8": {
            "nodes": ['s', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 't'],
            "edges": [('a', 's'), ('s', 'c'), ('t', 'd'), ('d', 'b'), ('c', 'b'), ('c', 'e'), ('c', 'f'), ('c', 'g'), ('f', 'i'), ('g', 'h')],
            "obstacles":['c', 'b', 'd', 't'],
            "start":'s',
            "target":'t'
        },

        "p7": {
            "nodes": ['s', 'a', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 't', 'b'],
            "edges": [('a','s'), ('s','b'), ('s','c'), ('c','f'), ('b','d'), ('b','e'), ('e','g'), ('g','h'), ('e','i'), ('i','j'), ('j','t')],
            "obstacles": ['b', 'd', 'e', 'g', 't'],
            "start": 's',
            "target": 't'
        },

        "p6" : {
            "nodes": ['s', 'a', 'b', 'c', 'd', 't', 'h', 'i', 'k'],
            "edges": [('s', 'a'), ('a', 'b'), ('b', 'c'), ('c', 't'), ('t', 'h'), ('b', 'd'),
                      ('b', 'f'), ('h', 'i'), ('c', 'k')],
            "obstacles": ['b', 'c', 't', 'k'],
            "start": 's',
            "target": 't'
        },

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
                       'i','j','z','k'],

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
