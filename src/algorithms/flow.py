from typing import Any
from models.graph import Graph
from collections import deque
import math

class Flow():
    @staticmethod
    def ford_fulkerson(graph: Graph, source: Any, sink: Any) -> float:
        """
        Tính luồng cực đại từ nguồn (source) đến đích (sink) 
        sử dụng Ford-Fulkerson (phiên bản Edmonds-Karp với BFS).

        Args:
            graph (Graph): Đối tượng đồ thị.
            source: Nút nguồn.
            sink: Nút đích.

        Returns:
            int: Giá trị của luồng cực đại.
        """
        # Khởi tạo đồ thị còn dư (residual capacity)
        # capacity_residual[u][v] là sức chứa còn dư từ u đến v
        capacity_residual = {u: graph.adj_list[u].copy() for u in graph.adj_list}
        max_flow = 0
        
        # Lấy danh sách tất cả các nút
        try:
            all_nodes = set(graph.nodes)
        except AttributeError:
            # Trường hợp graph.nodes không tồn tại, tự xây dựng all_nodes
            all_nodes = set(graph.adj_list.keys())
            for u in graph.adj_list:
                all_nodes.update(graph.adj_list[u].keys())
            
        # Đảm bảo tất cả các nút đều có khóa trong capacity_residual (cho các cạnh ngược)
        for u in all_nodes:
            if u not in capacity_residual:
                capacity_residual[u] = {}

        while True:
            # 1. Tìm đường tăng luồng (augmenting path) bằng BFS
            parent = {node: None for node in all_nodes}
            queue = deque([source])
            parent[source] = source 
            path_found = False

            while queue:
                u = queue.popleft()
                
                if u == sink:
                    path_found = True
                    break
                
                # Duyệt qua tất cả các nút có thể có luồng còn dư đi tới
                for v in all_nodes:
                    # Lấy sức chứa còn dư (capacity_residual[u][v]), mặc định là 0
                    residual_cap = capacity_residual[u].get(v, 0)
                    
                    if residual_cap > 0 and parent[v] is None:
                        parent[v] = u
                        queue.append(v)
                
            if not path_found:
                # Dừng nếu không tìm thấy đường tăng luồng
                break

            # 2. Tìm luồng cực đại có thể đẩy qua đường
            path_flow = math.inf
            s = sink
            while s != source:
                u = parent[s]
                path_flow = min(path_flow, capacity_residual[u].get(s, 0))
                s = u

            # 3. Cập nhật luồng trên đường đi và đồ thị còn dư
            max_flow += path_flow
            
            v = sink
            while v != source:
                u = parent[v]
                
                # Cạnh thuận: Giảm sức chứa còn dư
                capacity_residual[u][v] = capacity_residual[u].get(v, 0) - path_flow
                
                # Cạnh ngược: Tăng sức chứa còn dư
                capacity_residual[v][u] = capacity_residual[v].get(u, 0) + path_flow
                
                v = u

        return max_flow