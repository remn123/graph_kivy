import numpy as np
from utils import uniquecolors

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
        
        distances = []
        visited = []
        for v in range(len(graph.nodes)):
            distances.append(np.inf)
            visited.append([])

        import heapq 

        flg_print = 1
        
        # creating Priority Queue (based on minHeap)
        PQueue = []
        distances[root] = 0
        heapq.heappush(PQueue, (distances[root], root, root))
        while PQueue: # while queue is not empty
            #Step 2: Pop the top item from the PQueue and add it to the visited list.
            cur_dist, node_id, last_node = heapq.heappop(PQueue)
            visited[node_id] = [cur_dist, last_node]
            if flg_print !=0:
                callback((size*size-1)-node_id, status['VISITED'], 0.05, False)

            #Step 3: Find all the adjacent nodes of the node marked visited 
            #        and add the ones that are not yet visited, to the queue.
            for idx, n in enumerate(graph.nodes[node_id].children):
                if not visited[n]: # not visited yet
                    new_dist = graph.nodes[node_id].weights[idx]+cur_dist
                    if new_dist < distances[n]:
                        distances[n] = new_dist
                        heapq.heappush(PQueue, (new_dist, n, node_id))
                    if n == last:
                        flg_print = 0
                    if flg_print !=0:
                        callback((size*size-1)-n, status['VISITING'], 0.05, False)

        target = last
        path = []
        path.append(target)
        sum_dist=0
        while target != root:
            dist, last_node = visited[target]
            path.append(last_node)
            sum_dist += dist
            target = last_node

        path.reverse()
        for v in path:
            callback((size*size-1)-v, status['RESULT'], 0.04)
    
    @staticmethod
    def A_star(root, last, graph, callback, status, size):    
        distances = []
        visited = []
        J = last % size
        I = last-size*J
        heuristic = dict()
        for v in range(len(graph.nodes)):
            distances.append(np.inf)
            visited.append([])
            j = v % size
            i = v-size*j
            heuristic.update({v: np.sqrt((i-I)**2+(j-J)**2)})

        import heapq 
        
        flg_print = 1
        
        # creating Priority Queue (based on minHeap)
        PQueue = []
        distances[root] = 0
        heapq.heappush(PQueue, (distances[root], root, root))
        while PQueue: # while queue is not empty
            #Step 2: Pop the top item from the PQueue and add it to the visited list.
            cur_dist, node_id, last_node = heapq.heappop(PQueue)
            visited[node_id] = [cur_dist, last_node]
            if flg_print !=0:
                callback((size*size-1)-node_id, status['VISITED'], 0.05, False)

            #Step 3: Find all the adjacent nodes of the node marked visited 
            #        and add the ones that are not yet visited, to the queue.
            for idx, n in enumerate(graph.nodes[node_id].children):
                if not visited[n]: # not visited yet
                    new_dist = graph.nodes[node_id].weights[idx]+cur_dist+heuristic[n]
                    if new_dist < distances[n]:
                        distances[n] = new_dist
                        heapq.heappush(PQueue, (new_dist, n, node_id))
                    if n == last:
                        flg_print = 0
                    if flg_print !=0:
                        callback((size*size-1)-n, status['VISITING'], 0.05, False)

        target = last
        path = []
        path.append(target)
        sum_dist=0
        while target != root:
            dist, last_node = visited[target]
            path.append(last_node)
            sum_dist += dist
            target = last_node

        path.reverse()
        for v in path:
            callback((size*size-1)-v, status['RESULT'], 0.04)


    @staticmethod
    def flood_fill(ones, matrix, callback, callback2, status, size):
        if ones:
            for i in range(size):
                for j in range(size):
                    n = j + i*size
                    if n in ones:
                        matrix[i][j] = 1

            visited = dict()
            groups = dict()
            group = 0
            for i in range(size):
                for j in range(size):
                    n = j + i*size
                    queue = []
                    
                    if matrix[i][j] == 1 and visited.get(j+i*size, True):
                        queue.append(n)

                    while queue:
                        node_id = queue.pop(0)
                        visited.update({node_id: False})
                        #print(visited)
                        callback((size*size-1)-node_id, status['VISITED'], 0.05, False)
                        callback2((size*size-1)-node_id, str(group), 0.01)
                        groups.update({node_id: group})
                        J = node_id % size
                        I = node_id // size
                        for tpl in [(min(I+1, size-1), J), (I, min(J+1, size-1)), (max(I-1, 0), J), (I, max(J-1, 0))]: # children
                            k, l = tpl
                            #print(k, l, size-1, I, J, node_id)
                            if matrix[k][l] == 1 and visited.get(l+k*size, True):
                                callback((size*size-1)-l-k*size, status['VISITING'], 0.05, False)
                                queue.append(l+k*size)
                        if not queue:
                            group+=1

            new_status=uniquecolors(len(groups))
            for v in visited.keys():
                callback((size*size-1)-v, new_status[groups.get(v)], 0.04)