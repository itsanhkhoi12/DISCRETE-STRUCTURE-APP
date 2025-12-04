from collections import deque
class Traversal:
    def bfs_traversal(graph_adj: Graph, start_node):
        if start_node not in graph_adj:
            return []
        
        visited = set()
        queue = deque([start_node])
        traversal_path = []

        while queue:
            u = queue.popleft()
            if u not in visited:
                visited.add(u)
                traversal_path.append(u)
            
            # Thêm tất cả các đỉnh kề chưa thăm vào hàng đợi
                for v in graph_adj.get(u, []):
                    if v not in visited:
                        queue.append(v)

        return traversal_path