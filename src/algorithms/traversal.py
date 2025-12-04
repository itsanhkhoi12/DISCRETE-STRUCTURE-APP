from collections import deque
from models.graph import Graph

class Traversal:
    @staticmethod
    def bfs_traversal(graph: Graph, start_node):
        """Duyệt theo chiều rộng (Queue)"""
        if start_node not in graph.nodes:
            return []
        
        visited = set()
        queue = deque([start_node])
        visited.add(start_node)         
        traversal_path = []

        while queue:
            u = queue.popleft()
            traversal_path.append(u)

            neighbors = sorted(graph.adj_list.get(u, {}).keys())
            
            for v in neighbors:
                if v not in visited:
                    visited.add(v)
                    queue.append(v)

        return traversal_path

    @staticmethod
    def dfs_traversal(graph: Graph, start_node):
        """Duyệt theo chiều sâu (Stack)"""
        if start_node not in graph.nodes:
            return []

        visited = set()
        stack = [start_node]
        traversal_path = []

        while stack:
            u = stack.pop()
            
            if u not in visited:
                visited.add(u)
                traversal_path.append(u)
                
                neighbors = sorted(graph.adj_list.get(u, {}).keys(), reverse=True)
                
                for v in neighbors:
                    if v not in visited:
                        stack.append(v)
        
        return traversal_path