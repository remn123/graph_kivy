class GraphNode(object):
    
    def __init__(self, id, children, weights):
        self.id = id
        #self.children = sorted(children)
        self.children = sorted(children, reverse=True)
        self.weights = [x for _, x in sorted(zip(children, weights), reverse=True)]
        
    def __str__(self):
        return f'{self.id} : children={self.children}'
    
    def __repr__(self):
        return f'{self.id} : children={self.children}'

class Graph(object):
    
    def __init__(self, adjancency):
        self.nodes = []
        self.build(adjancency)
        
    def build(self, adjancency):
        # for node, edges, weight in zip(adjancency, weights):
        #     self.nodes.append(GraphNode(node, edges, weight)) 
        for node, edges, weights in adjancency:
            self.nodes.append(GraphNode(node, edges, weights)) 
    
    def __repr__(self):
        return f'{self.nodes}'
    
    def __str__(self):
        return f'{self.nodes}'