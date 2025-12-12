from collections import deque
from models.graph import Graph
from typing import List, Union
class Traversal:
    @staticmethod
    def bfs_traversal(graph: Graph, start_node: Union[str,int]) -> List[Union[str,int]]:
        """Duyệt theo chiều rộng (Queue)
        Args:
            graph: Đồ thị được biểu diễn dưới dạng danh sách kề
            start_node: Nút bắt đầu để duyệt theo chiến lược BFS
        Returns:
            traversal_path: Đường đi của nút được duyệt từ đồ thị đầu vào theo chiến lược BFS"""
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
    def dfs_traversal(graph: Graph, start_node: Union[str,int]) -> List[Union[str,int]]:
        """Duyệt theo chiều sâu (Stack)
        Args:
            graph: Đồ thị được biểu diễn dưới dạng danh sách kề
            start_node: Nút bắt đầu để duyệt theo chiến lược DFS
        Returns:
            traversal_path: Đường đi của nút được duyệt từ đồ thị đầu vào theo chiến lược DFS
        """
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