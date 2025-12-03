class Graph:
    def __init__(self, directed=True, weighted=True):
        """
        Khởi tạo Graph là một Danh sách đỉnh liền kề.
        Format: Đỉnh: {Danh sách các đỉnh liền kề với đỉnh đó}
        """
        self.nodes = set()      
        self.adj_list = {}      
        self.directed = directed 
        self.weighted = weighted

    def set_directed(self, is_directed):
        """Thay đổi chế độ có hướng/vô hướng và cập nhật lại cạnh"""
        self.directed = is_directed
        if not is_directed:
            snapshot = []
            for u in self.adj_list:
                for v, w in self.adj_list[u].items():
                    snapshot.append((u, v, w))
            
            for u, v, w in snapshot:
                self.add_edge(v, u, w) # Thêm chiều ngược lại

    def add_node(self, node):
        """Thêm một đỉnh mới"""
        self.nodes.add(node)
        if node not in self.adj_list:
            self.adj_list[node] = {}

    def add_edge(self, u, v, weight=1.0):
        """Thêm cạnh (u, v) với trọng số w"""
        self.add_node(u)
        self.add_node(v)

        if weight is None or not self.weighted:
            w_val = 1.0
        else:
            w_val = float(weight)

        # 1. Thêm chiều thuận u -> v
        self.adj_list[u][v] = w_val # <-- Dùng w_val
        
        # 2. Nếu là đồ thị vô hướng, tự động thêm chiều ngược v -> u
        if not self.directed:
            self.adj_list[v][u] = w_val # <-- Dùng w_val

    def get_edges(self):
        """Trả về danh sách tất cả các cạnh [(u, v, w), ...]"""
        edges = []
        seen = set() 

        for u in self.adj_list:
            for v, w in self.adj_list[u].items():
                if self.directed:
                    edges.append((u, v, w))
                # Nếu đồ thị vô hướng, không thêm lại cạnh đó. Ví dụ, đã thêm AB thì không lấy BA
                else:
                    if (v, u) not in seen:
                        edges.append((u, v, w))
                        seen.add((u, v))
        return edges

    def get_adjacency_matrix(self):
        """
        Sinh ra ma trận kề và danh sách tên đỉnh tương ứng.
        Returns: (matrix_2d_array, sorted_node_names) 
        """
        sorted_nodes = sorted(list(self.nodes))
        n = len(sorted_nodes)
        
        idx_map = {node: i for i, node in enumerate(sorted_nodes)}
        
        matrix = [[0] * n for _ in range(n)]

        for u in self.adj_list:
            for v, w in self.adj_list[u].items():
                i, j = idx_map[u], idx_map[v]
                matrix[i][j] = w
        
        return matrix, sorted_nodes
    
    @classmethod
    def from_data(cls, nodes, edges, directed, weighted=True):
        """
        Tạo một đối tượng Graph mới từ dữ liệu đã đọc từ file.
        Được gọi bởi FileController.
        """
        # 1. Khởi tạo đối tượng Graph mới với các cờ (flags) đúng
        instance = cls(directed=directed, weighted=weighted)
        
        # 2. Thêm các đỉnh
        for node in nodes:
            instance.add_node(node)
            
        # 3. Thêm các cạnh (kèm trọng số)
        # edge có format: (u, v, {'weight': w})
        for u, v, attrs in edges:
            weight = attrs.get('weight', 1.0)
            instance.add_edge(u, v, weight)
            
        return instance