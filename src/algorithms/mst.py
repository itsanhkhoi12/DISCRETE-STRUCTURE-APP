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

        def find(parent,u):
            """
            Tìm kiếm một đỉnh của đồ thị có thể tạo ra một chu trình            
            Args:
                parent: Danh sách các đỉnh đã duyệt qua
                u: Tên đỉnh cần tìm
            """
            if parent[u] != u:
                parent[u] = find(parent, parent[u])
            return parent[u]
        
        def union(parent,rank,u_root,v_root):
            """
            Hợp tập hợp chứa đỉnh u và tập hợp chứa đỉnh v lại thành một cây khung
            Args:
                parent: Tập hợp các đỉnh gốc 
                rank: Bậc của cây khung
                u_root: Đỉnh cha của đỉnh u của đồ thị
                v_root: Đinh cha của đỉnh v của đồ thị            
            """

            if rank[u_root] < rank[v_root]:
                parent[u_root] = v_root
            elif rank[v_root] < rank[u_root]:
                parent[v_root] = u_root
            else:
                parent[v_root] = u_root
                rank[u_root] += 1

        edges = graph.get_edges()
        # Kiểm tra danh sách cạnh rỗng 
        if not edges:
            return [],0
        
        # Sắp xếp lại cạnh theo trọng số weight
        edges = sorted(edges,key=lambda item: item[2])
        # Số đỉnh trong đồ thị
        graph_sizes = graph.nodes_sum()

        # Kết quả, parent, rank
        mst_weights = 0
        mst_edges = []
        parent = list(range(graph_sizes))
        rank = [0] * graph_sizes

        for u, v, weight in edges:
            if len(mst_edges) == graph_sizes - 1:
                break

            u_root = find(parent,u)
            v_root = find(parent,v)
            if u_root!=v_root:
                mst_edges.append((u,v,weight))
                mst_weights += weight
                union(parent,rank,u_root,v_root)

        return mst_edges,mst_weights
    
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
