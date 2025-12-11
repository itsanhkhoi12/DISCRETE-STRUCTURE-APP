import heapq
from src.models.graph import Graph


class MST:
    @staticmethod
    def prim(graph: Graph):
        """
        Trả về: (danh_sách_cạnh, tổng_trọng_số)
        danh_sách_cạnh = [(u, v, weight)]
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
        class UnionFind:
            def __init__(self, nodes):
                self.parent = {node: node for node in nodes}

            def find(self, u):
                if self.parent[u] != u:
                    self.parent[u] = self.find(self.parent[u])
                return self.parent[u]

            def union(self, u, v):
                pu, pv = self.find(u), self.find(v)
                if pu == pv:
                    return False
                self.parent[pu] = pv
                return True

        uf = UnionFind(graph.nodes)
        mst_edges = []
        total_weight = 0

        # Lấy danh sách các cạnh và sắp xếp theo trọng số
        edges = graph.get_edges()
        edges.sort(key=lambda x: x[2])  # x[2] = trọng số

        # Lặp qua các cạnh
        for u, v, w in edges:
            if uf.union(u, v):  # nếu u, v chưa cùng tập hợp
                mst_edges.append((u, v, w))
                total_weight += w

        return mst_edges, total_weight
