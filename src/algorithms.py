class Algo(object):

    @staticmethod
    def dfs(root, last, graph, callback, status, size):
        stack = []
        visited = []
        # Step 1: Insert the root node or starting node of a tree or a graph in the stack.
        stack.append(root)

        while stack: # while stack is not empty
            #Step 2: Pop the top item from the stack and add it to the visited list.
            node_id = stack.pop()
            visited.append(node_id)
            callback((size*size-1)-node_id, status['VISITED'], 0.05, False)
            #Step 3: Find all the adjacent nodes of the node marked visited 
            #        and add the ones that are not yet visited, to the stack.
            for n in graph.nodes[node_id].children:
                if (n==last):
                    visited.append(n)
                    stack = []
                    break
                else:
                    if n not in visited:
                        if n not in stack:
                            # Visiting status
                            stack.append(n)
                            callback((size*size-1)-n, status['VISITING'], 0.05, False)
        for v in visited:
            callback((size*size-1)-v, status['RESULT'], 0.04)

    @staticmethod
    def bfs(root, last, graph, callback, status, size):
        pass

    @staticmethod
    def bfs(root, last, graph, callback, status, size):
        pass