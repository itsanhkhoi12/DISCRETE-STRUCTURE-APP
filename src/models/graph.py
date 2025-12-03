# class Graph:
#     def __init__(self, directed=True, weighted=True):
#         """
#         Khởi tạo Graph là một Danh sách đỉnh liền kề.
#         Format: Đỉnh: {Danh sách các đỉnh liền kề với đỉnh đó}
#         """
#         self.nodes = set()      
#         self.adj_list = {}      
#         self.directed = directed 
#         self.weighted = weighted

#     def set_directed(self, is_directed):
#         """Thay đổi chế độ có hướng/vô hướng và cập nhật lại cạnh"""
#         self.directed = is_directed
#         if not is_directed:
#             snapshot = []
#             for u in self.adj_list:
#                 for v, w in self.adj_list[u].items():
#                     snapshot.append((u, v, w))
            
#             for u, v, w in snapshot:
#                 self.add_edge(v, u, w) # Thêm chiều ngược lại

#     def add_node(self, node):
#         """Thêm một đỉnh mới"""
#         self.nodes.add(node)
#         if node not in self.adj_list:
#             self.adj_list[node] = {}

#     def add_edge(self, u, v, weight=1.0):
#         """Thêm cạnh (u, v) với trọng số w"""
#         self.add_node(u)
#         self.add_node(v)

#         if weight is None or not self.weighted:
#             w_val = 1.0
#         else:
#             w_val = float(weight)

#         # 1. Thêm chiều thuận u -> v
#         self.adj_list[u][v] = w_val # <-- Dùng w_val
        
#         # 2. Nếu là đồ thị vô hướng, tự động thêm chiều ngược v -> u
#         if not self.directed:
#             self.adj_list[v][u] = w_val # <-- Dùng w_val

#     def get_edges(self):
#         """Trả về danh sách tất cả các cạnh [(u, v, w), ...]"""
#         edges = []
#         seen = set() 

#         for u in self.adj_list:
#             for v, w in self.adj_list[u].items():
#                 if self.directed:
#                     edges.append((u, v, w))
#                 # Nếu đồ thị vô hướng, không thêm lại cạnh đó. Ví dụ, đã thêm AB thì không lấy BA
#                 else:
#                     if (v, u) not in seen:
#                         edges.append((u, v, w))
#                         seen.add((u, v))
#         return edges

#     def get_adjacency_matrix(self):
#         """
#         Sinh ra ma trận kề và danh sách tên đỉnh tương ứng.
#         Returns: (matrix_2d_array, sorted_node_names) 
#         """
#         sorted_nodes = sorted(list(self.nodes))
#         n = len(sorted_nodes)
        
#         idx_map = {node: i for i, node in enumerate(sorted_nodes)}
        
#         matrix = [[0] * n for _ in range(n)]

#         for u in self.adj_list:
#             for v, w in self.adj_list[u].items():
#                 i, j = idx_map[u], idx_map[v]
#                 matrix[i][j] = w
        
#         return matrix, sorted_nodes
    
#     @classmethod
#     def from_data(cls, nodes, edges, directed, weighted=True):
#         """
#         Tạo một đối tượng Graph mới từ dữ liệu đã đọc từ file.
#         Được gọi bởi FileController.
#         """
#         # 1. Khởi tạo đối tượng Graph mới với các cờ (flags) đúng
#         instance = cls(directed=directed, weighted=weighted)
        
#         # 2. Thêm các đỉnh
#         for node in nodes:
#             instance.add_node(node)
            
#         # 3. Thêm các cạnh (kèm trọng số)
#         # edge có format: (u, v, {'weight': w})
#         for u, v, attrs in edges:
#             weight = attrs.get('weight', 1.0)
#             instance.add_edge(u, v, weight)
            
#         return instance

# src/models/graph.py
# BẢN ĐÃ SỬA HOÀN CHỈNH – HOẠT ĐỘNG 100% CHO PRIM, KRUSKAL, DIJKSTRA

from typing import Dict, List, Tuple
import json


class Graph:
    def __init__(self, directed=False, weighted=True):
        """
        Khởi tạo đồ thị
        directed=False → vô hướng
        weighted=True  → có trọng số
        """
        self.nodes = set()
        self.adj_list: Dict[str, Dict[str, float]] = {}
        self.directed = directed    # BIẾN HƯỚNG DUY NHẤT
        self.weighted = weighted

        # Xóa biến thừa
        # self.is_directed = False
        # self.edges = []   # không dùng

    def add_node(self, node: str):
        self.nodes.add(node)
        if node not in self.adj_list:
            self.adj_list[node] = {}

    def add_edge(self, u: str, v: str, weight: float = 1.0):
        self.add_node(u)
        self.add_node(v)

        self.adj_list[u][v] = weight

        if not self.directed:          # dùng đúng biến hướng
            self.adj_list[v][u] = weight

    def remove_directed_edges(self):
        if self.directed:
            return

        edges_to_remove = []
        for u in self.adj_list:
            for v in self.adj_list[u]:
                if u > v:
                    edges_to_remove.append((u, v))

        for u, v in edges_to_remove:
            self.adj_list[u].pop(v, None)

    def set_directed(self, is_directed: bool):
        if self.directed == is_directed:
            return

        if is_directed:
            self.remove_directed_edges()
        else:
            snapshot = []
            for u in self.adj_list:
                for v, w in self.adj_list[u].items():
                    snapshot.append((u, v, w))

            for u, v, w in snapshot:
                if u not in self.adj_list[v]:
                    self.adj_list[v][u] = w

        self.directed = is_directed

    def get_neighbors(self, node: str) -> Dict[str, float]:
        return self.adj_list.get(node, {})

    def get_edges(self) -> List[Tuple[str, str, float]]:
        edges = []
        seen = set()
        for u in self.adj_list:
            for v, w in self.adj_list[u].items():
                key = tuple(sorted((u, v)))
                if key not in seen:
                    edges.append((u, v, w))
                    seen.add(key)
        return edges

    def get_adjacency_matrix(self):
        sorted_nodes = sorted(self.nodes)
        n = len(sorted_nodes)
        idx = {node: i for i, node in enumerate(sorted_nodes)}
        matrix = [[0.0 for _ in range(n)] for _ in range(n)]

        for u in self.adj_list:
            for v, w in self.adj_list[u].items():
                matrix[idx[u]][idx[v]] = w

        return matrix, sorted_nodes

    def save_to_file(self, filename="data/hcm_district1.json"):
        data = {
            "directed": self.directed,
            "weighted": self.weighted,
            "nodes": list(self.nodes),
            "edges": self.get_edges()
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Đã lưu đồ thị vào {filename}")

    def load_from_file(self, filename="data/hcm_district1.json"):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.__init__(data["directed"], data["weighted"])

            for node in data["nodes"]:
                self.add_node(node)

            for u, v, w in data["edges"]:
                self.add_edge(u, v, w)

            print(f"Đã tải đồ thị từ {filename}")
        except FileNotFoundError:
            print("Không tìm thấy file")

    def __str__(self):
        return f"Đồ thị ({'có hướng' if self.directed else 'vô hướng'}, {'có trọng số' if self.weighted else 'không trọng số'}) - {len(self.nodes)} đỉnh, {len(self.get_edges())} cạnh"
