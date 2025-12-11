import heapq
from src.models.graph import Graph


class MSTAlgorithms:
    def __init__(self, graph):
        self.graph = graph

    def prim_mst(self, start_node=None):
        if not self.graph.nodes:
            return [], 0.0
        if start_node is None:
            start_node = next(iter(self.graph.nodes))
        visited = set([start_node])
        pq = []  # (weight, u, v)
        # Thêm cạnh kề với start_node
        for v, w in self.graph.adj_list.get(start_node, {}).items():
            heapq.heappush(pq, (w, start_node, v))
        mst_edges = []
        total_weight = 0.0
        while pq:
            w, u, v = heapq.heappop(pq)
            if v not in visited:
                visited.add(v)
                mst_edges.append((u, v, w))
                total_weight += w
                for neighbor, weight in self.graph.adj_list.get(v, {}).items():
                    if neighbor not in visited:
                        heapq.heappush(pq, (weight, v, neighbor))
        return mst_edges, total_weight

    def kruskal_mst(self):
        if not self.graph.nodes:
            return [], 0.0
        # Lấy danh sách cạnh
        edges = []
        seen = set()
        for u in self.graph.adj_list:
            for v, w in self.graph.adj_list[u].items():
                edge_key = tuple(sorted([u, v]))
                if edge_key not in seen:
                    edges.append((w, u, v))
                    seen.add(edge_key)
        edges.sort()  # Sắp xếp theo trọng số tăng dần
        # Union-Find
        parent = {node: node for node in self.graph.nodes}
        rank = {node: 0 for node in self.graph.nodes}

        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def union(x, y):
            px, py = find(x), find(y)
            if px == py:
                return False
            if rank[px] < rank[py]:
                parent[px] = py
            elif rank[px] > rank[py]:
                parent[py] = px
            else:
                parent[py] = px
                rank[px] += 1
            return True
        mst_edges = []
        total_weight = 0.0
        for w, u, v in edges:
            if union(u, v):
                mst_edges.append((u, v, w))
                total_weight += w
            if len(mst_edges) == len(self.graph.nodes)-1:
                break
        return mst_edges, total_weight
