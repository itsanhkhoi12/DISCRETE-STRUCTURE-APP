from src.models.graph import Graph
import heapq


class MST:
    @staticmethod
    def prim(graph: Graph):
        """
        Trả về ds các cạnh MST, trọng số, none nếu không có trọng số
        """
        if not graph.nodes:
            return [], 0.0
        # Lấy đỉnh bất kì làm điểm bắt đầu
        start = next(iter(graph.nodes))
        # Tập thêm đỉnh vào cây khung
        in_mst = {start}
        # Danh sách cạnh của MST
        mst_edges = []
        total_weight = 0.0
        # Lặp khi tất cả đỉnh vào cây khung
        while len(in_mst) < len(graph.nodes):
            min_weight = float('inf')  # Tìm cạnh có trọng số nhỏ nhất.
            best_u = None
            best_v = None
            for u in in_mst:
                for v, w in graph.adj_list.get(u, {}).items():
                    if v not in in_mst and w < min_weight:
                        min_weight = w
                        best_u = u
                        best_v = v
            # Nếu không tìm được cạnh nào thì đồ thị không liên thông
            if best_v is None:
                return mst_edges, total_weight
            # Thêm cạnh vào MST
            mst_edges.append((best_u, best_v, min_weight))
            total_weight += min_weight
            in_mst.add(best_v)
        return mst_edges, total_weight

    @staticmethod
    def kruskal(graph: Graph):
        # Dùng Union-find
        if not graph.nodes:
            return [], 0.0
        # Sắp xếp các cạnh theo trọng số
        edges = []
        for u in graph.adj_list:
            for v, w in graph.adj_list[u].items():
                if u < v:
                    edges.append((w, u, v))
        edges.sort()  # Sắp xếp tăng dần trọng số
        parent = {node: node for node in graph.nodes}

        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def union(x, y):
            px = find(x)
            py = find(y)
            if px != py:
                parent[px] = py
                return True
            return False
        mst_edges = []
        total_weight = 0.0
        for w, u, v in edges:
            if union(u, v):
                mst_edges.append((u, v, w))
                total_weight += w
            if len(mst_edges) == len(graph.nodes)-1:
                break
        return mst_edges, total_weight

