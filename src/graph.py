class GraphNode(object):
    
    def __init__(self, id, children):
        self.id = id
        self.children = sorted(children)
        
    def __str__(self):
        return f'{self.id} : children={self.children}'
    
    def __repr__(self):
        return f'{self.id} : children={self.children}'

class Graph(object):
    
    def __init__(self, adjancency):
        self.nodes = []
        
        self.build(adjancency)
        
    def build(self, adjancency):
        for node, edges in adjancency:
            self.nodes.append(GraphNode(node, edges)) 
    
    def __repr__(self):
        return f'{self.nodes}'
    
    def __str__(self):
        return f'{self.nodes}'