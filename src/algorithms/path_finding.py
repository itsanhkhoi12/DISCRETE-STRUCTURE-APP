from models.graph import Graph
import math, heapq
from typing import Optional, List, Dict, Tuple
class PathFinding():
    @staticmethod
    def dijkstra(graph: Graph, start_node) -> Tuple[List[int],List[Dict[str,str]]]:
        """
        Thực hiện thuật toán Dijkstra để tìm đường đi ngắn nhất đến các đỉnh trong đồ thị với đỉnh cho trước
        Args:
            graph: Đồ thị được biểu diễn dưới dạng danh sách kề
            start_node: Đỉnh bắt đầu
        Returns:
            distances,previous: Danh sách khoảng cách nhỏ nhất và các đỉnh đi qua đến các đỉnh có trong đồ thị từ đỉnh cho trước.
        """
        distances = {node: math.inf for node in graph.nodes}
        previous = {node: None for node in graph.nodes} 
    
        distances[start_node] = 0
    
        pq = [(0, start_node)]

        while pq:
            current_d, u = heapq.heappop(pq)

            if current_d > distances[u]:
                continue

            for v, weight in graph.adj_list[u].items(): 
                if distances[v] > distances[u] + weight:
                    distances[v] = distances[u] + weight 
                    previous[v] = u 
                    heapq.heappush(pq, (distances[v], v))

        return distances, previous

    @staticmethod
    def bellman_ford(graph: Graph, start_node) -> Optional[Dict[str,Dict]]:
        """
        Thực hiện thuật toán Bellman Ford để tìm đường đi ngắn nhất đến các đỉnh trong đồ thị với đỉnh cho trước.
        Args:
            graph: Đồ thị được biểu diễn dưới dạng danh sách kề
            start_node: Đỉnh bắt đầu
        Returns:
            table: Một dictionary bao gồm: {Tên đỉnh: {Khoảng cách ngắn nhất, Đỉnh trước đó}}

        """   
        edges = graph.get_edges()
        # Table: Bao gồm thông tin về đỉnh - khoảng cách ngắn nhất - đỉnh trước đó (start = None)
        table = {node: {'distance': math.inf,'previous': None} for node in graph.nodes}
        table[start_node]['distance'] = 0
        relaxation = False

        for i in range(graph.nodes_sum()-1):
            for edge in edges:
                u, v, weight = edge
                if table[u]['distance'] != math.inf and table[u]['distance'] + weight < table[v]['distance']:
                    table[v]['distance'] = table[u]['distance'] + weight
                    table[v]['previous'] = u
                    relaxation = True
            if not relaxation:
                break
        
        if relaxation:
            # Kiểm tra chu trình âm
            for u,v,weight in edges:
                if table[u]['distance'] != math.inf and table[u]['distance'] + weight < table[v]['distance']:
                    return None
        
        return table

