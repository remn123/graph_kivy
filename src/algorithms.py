import numpy as np

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
        queue = []
        visited = []
        # Step 1: Insert the root node or starting node of a tree or a graph in the queue.
        queue.append(root)

        while queue: # while queue is not empty
            #Step 2: Pop the first item from the queue and add it to the visited list.
            node_id = queue.pop(0)
            visited.append(node_id)
            callback((size*size-1)-node_id, status['VISITED'], 0.05, False)

            #Step 3: Find all the adjacent nodes of the node marked visited 
            #        and add the ones that are not yet visited, to the queue.
            for n in graph.nodes[node_id].children:
                if (n==last):
                    visited.append(n)
                    queue = []
                    break
                else:
                    if n not in visited:
                        if n not in queue:
                            # Visiting status
                            queue.append(n)
                            callback((size*size-1)-n, status['VISITING'], 0.05, False)
        for v in visited:
            callback((size*size-1)-v, status['RESULT'], 0.04)

    @staticmethod
    def dijsktra(root, last, graph, callback, status, size):
        distances = dict()
        for v in graph.nodes:
            distances.update({v.id: np.Inf})

        queue = []
        visited = []
        flg_break = 0
        # Step 1: Insert the root node or starting node of a tree or a graph in the queue.
        queue.append(root)
        distances.update({root: 0})

        while queue: # while queue is not empty
            #Step 2: Pop the top item from the stack and add it to the visited list.
            node_id = queue.pop(0)
            visited.append(node_id)
            callback((size*size-1)-node_id, status['VISITED'], 0.05, False)

            cur_dist = distances[node_id]
            #Step 3: Find all the adjacent nodes of the node marked visited 
            #        and add the ones that are not yet visited, to the queue.
            min_dist = [node_id, np.Inf]
            for idx, n in enumerate(graph.nodes[node_id].children):
                if (n==last):
                    visited.append(n)
                    queue = []
                    flg_break = 1
                    break
                else:
                    if n not in visited:
                        new_dist = graph.nodes[node_id].weights[idx]+cur_dist
                        if new_dist < min_dist[1]:
                            min_dist = [n, new_dist]
                            distances.update({n: new_dist})
                            #queue.append(n)
                        callback((size*size-1)-n, status['VISITING'], 0.05, False)    
            if flg_break == 0:
                n = min_dist[0]
                if n not in visited:
                    queue.append(min_dist[0])
                
        for v in visited:
            callback((size*size-1)-v, status['RESULT'], 0.04)

    @staticmethod
    def A_star(root, last, graph, callback, status, size):
        distances = dict()
        for v in graph.nodes:
            distances.update({v.id: np.Inf})
        
        distances.update({root: 0})

        J = last % size
        I = last-size*J

        heuristic = dict()
        for v in graph.nodes:
            j = v.id % size
            i = v.id-size*j
            heuristic.update({v.id: np.sqrt((i-I)**2+(j-J)**2)})
            # if i==I or j==J:
            #     heuristic.update({v.id: 0})
            # else:
            #     heuristic.update({v.id: 100})
            #print({v.id: i})

        queue = []
        visited = []
        flg_break = 0
        # Step 1: Insert the root node or starting node of a tree or a graph in the queue.
        queue.append(root)
        

        while queue: # while queue is not empty
            #Step 2: Pop the top item from the stack and add it to the visited list.
            node_id = queue.pop(0)
            visited.append(node_id)
            callback((size*size-1)-node_id, status['VISITED'], 0.05, False)
            #print(distances[node_id], heuristic[node_id])

            cur_dist = distances[node_id] 
            #Step 3: Find all the adjacent nodes of the node marked visited 
            #        and add the ones that are not yet visited, to the queue.
            min_dist = [node_id, np.Inf]
            for idx, n in enumerate(graph.nodes[node_id].children):
                if (n==last):
                    visited.append(n)
                    queue = []
                    flg_break = 1
                    break
                else:
                    if n not in visited:
                        new_dist = graph.nodes[node_id].weights[idx] + cur_dist + heuristic[n]
                        if new_dist < min_dist[1]:
                            min_dist = [n, new_dist]
                            distances.update({n: new_dist})
                            #queue.append(n)
                        callback((size*size-1)-n, status['VISITING'], 0.05, False)    
            if flg_break == 0:
                n = min_dist[0]
                if n not in visited:
                    queue.append(min_dist[0])
                
        for v in visited:
            callback((size*size-1)-v, status['RESULT'], 0.04)