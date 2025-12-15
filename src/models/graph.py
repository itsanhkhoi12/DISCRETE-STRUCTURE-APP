class Graph:
    def __init__(self, directed=True, weighted=True):
        """
        Khởi tạo Graph là một Danh sách kề.
        Format: Đỉnh: {Danh sách các kề với đỉnh đó}
        """
        self.nodes = set()      
        self.adj_list = {}      
        self.directed = directed 
        self.weighted = weighted

    def nodes_sum(self):
        return len(self.adj_list)
    
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
        """Trả về danh sách tất cả các cạnh [(u, v, w), ...]
            - u,v: Hai đỉnh của một cạnh
            - w: Trọng số của cạnh đó"""
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

    def remove_node(self, node):
        """Xóa đỉnh và tất cả các cạnh liên quan"""
        if node in self.nodes:
            self.nodes.remove(node)
        
        # 1. Xóa trong adj_list (chiều đi)
        if node in self.adj_list:
            del self.adj_list[node]
        
        # 2. Xóa các cạnh chiều đến (chiều về từ đỉnh khác)
        for u in list(self.adj_list.keys()):
            if node in self.adj_list[u]:
                del self.adj_list[u][node]

    def remove_edge(self, u, v):
        """Xóa cạnh u -> v"""
        if u in self.adj_list and v in self.adj_list[u]:
            del self.adj_list[u][v]
        
        # Nếu vô hướng, xóa cả v -> u
        if not self.directed:
            if v in self.adj_list and u in self.adj_list[v]:
                del self.adj_list[v][u]

    def update_weight(self, u, v, new_w):
        """Cập nhật trọng số"""
        # Logic y hệt add_edge (ghi đè)
        self.add_edge(u, v, new_w)

    def rename_node(self, old_name, new_name):
        """
        Đổi tên một đỉnh trong đồ thị.
        Trả về True nếu thành công, False nếu thất bại (tên cũ không tồn tại hoặc tên mới bị trùng).
        """
        # 1. Kiểm tra tính hợp lệ
        if old_name not in self.nodes:
            return False # Đỉnh cũ không tồn tại
        if new_name in self.nodes:
            return False # Tên mới đã tồn tại (tránh gộp đỉnh)
        if old_name == new_name:
            return False

        # 2. Cập nhật tập đỉnh (Nodes Set)
        self.nodes.remove(old_name)
        self.nodes.add(new_name)

        # 3. Cập nhật Key trong Danh sách kề (Các cạnh đi ra từ old_name)
        # Ví dụ: old_name -> B, C đổi thành new_name -> B, C
        if old_name in self.adj_list:
            self.adj_list[new_name] = self.adj_list.pop(old_name)

        # 4. Cập nhật Value trong Danh sách kề (Các cạnh đi vào old_name)
        # Ví dụ: A -> old_name đổi thành A -> new_name
        for u in self.adj_list:
            if old_name in self.adj_list[u]:
                # Lấy trọng số cũ ra
                weight = self.adj_list[u].pop(old_name)
                # Tạo kết nối tới tên mới với trọng số y hệt
                self.adj_list[u][new_name] = weight

        return True
    
    def reverse_edge(self,u,v):
        """
        Đảo ngược chiều của một cạnh (u,v) đối với đồ thị có hướng.
        Cạnh (u,v) -> Cạnh (v,u)
        """

        if not self.directed:
            return False
        
        if u not in self.adj_list or v not in self.adj_list[u]:
            return False
        
        weight = self.adj_list[u][v]
        self.remove_edge(u,v)
        self.add_edge(v,u,weight)
       
        return True