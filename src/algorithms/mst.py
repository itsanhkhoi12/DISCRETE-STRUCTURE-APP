from models.graph import Graph
import heapq
from typing import Tuple, List

class MST:
    @staticmethod
    def kruskal(graph:Graph) -> Tuple[List[Tuple],int]:
        """
        Thực hiện thuật toán Kruskal để tìm cây khung nhỏ nhất (MST)
        Args:
            graph: Đồ thị được biểu diễn dưới dạng danh sách cạnh.
        Returns:
            mst_edges: Một đồ thị con biểu diễn cây khung nhỏ nhất được biểu diễn dưới dạng danh sách cạnh
            total_weight: Tổng trọng số nhỏ nhất của đồ thị
        """      
        if not graph.adj_list:
            return [],0
        
                
    @staticmethod
    def prim(graph:Graph) -> Tuple[List[Tuple],int]:
        """
        Thực hiện thuật toán Prim để tìm cây khung nhỏ nhất (MST)
        Args:
            graph: Đồ thị được biểu diễn dưới dạng danh sách kề.
        Returns:
            mst_edges: Một đồ thị con biểu diễn cây khung nhỏ nhất được biểu diễn dưới dạng danh sách cạnh
            total_weight: Tổng trọng số nhỏ nhất của đồ thị
        """       
        # Kiểm tra Nếu đồ thị rỗng
        if not graph.nodes:
            return [], 0

        # Chọn 1 đỉnh bất kỳ làm điểm bắt đầu
        start = next(iter(graph.nodes))
        visited = set([start])
        mst_edges = []
        total_weight = 0

        # Tạo heap các cạnh từ đỉnh start
        edge_heap = []
        for v, w in graph.adj_list[start].items():
            heapq.heappush(edge_heap, (w, start, v))

        # Lặp cho đến khi tất cả đỉnh được thăm
        while edge_heap and len(visited) < len(graph.nodes):
            w, u, v = heapq.heappop(edge_heap)
            if v not in visited:
                visited.add(v)
                mst_edges.append((u, v, w))
                total_weight += w

                # Thêm tất cả cạnh mới từ đỉnh v vào heap
                for to, weight in graph.adj_list[v].items():
                    if to not in visited:
                        heapq.heappush(edge_heap, (weight, v, to))

            return mst_edges, total_weight

    @staticmethod
    def kruskal(graph: Graph):
        """
        Trả về: (danh_sách_cạnh, tổng_trọng_số)
        danh_sách_cạnh = [(u, v, weight)]
        """
