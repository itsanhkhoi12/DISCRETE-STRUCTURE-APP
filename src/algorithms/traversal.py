from collections import deque
class Traversal:
    def __init__(self):
      pass
    
    @staticmethod
    def bfs_traversal(graph_adj: Graph, start_node):
        if start_node not in graph_adj:
            return []
        
        visited = set()
        queue = deque([start_node])
        visited.add(start_node)         
        traversal_path = []

        while queue:
            u = queue.popleft()
            traversal_path.append(u)

        # duyệt các đỉnh kề
            for v in graph_adj.get(u, []):
                if v not in visited:
                    visited.add(v)
                    queue.append(v)

        return traversal_path

    @staticmethod
    def dfs_traversal(graph, start_node):
        visited = set()
        components = []

        if start_node in graph:
            stack = [start_node]
            comp = []
            while stack:
                node = stack.pop()
                if node not in visited:
                    visited.add(node)
                    comp.append(node)

                    for neighbor in reversed(graph[node]):
                        if neighbor not in visited:
                            stack.append(neighbor)
            components.append(comp)

        for node in graph:
            if node not in visited:
                stack = [node]
                comp = []

                while stack:
                    curr = stack.pop()
                    if curr not in visited:
                        visited.add(curr)
                        comp.append(curr)

                        for neighbor in reversed(graph[curr]):
                            if neighbor not in visited:
                                stack.append(neighbor)

                components.append(comp)
        return components
