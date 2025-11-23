class Graph:
    def __init__(self, directed=False):
        self.nodes = set()
        self.adj_list = {}  # Danh sách kề: {'A': [('B', 5)], 'B': []}
        self.directed = directed

    def add_edge(self, u, v, w=1):
        self.nodes.add(u)
        self.nodes.add(v)
        
        # Khởi tạo list nếu chưa có
        if u not in self.adj_list: self.adj_list[u] = []
        if v not in self.adj_list: self.adj_list[v] = []

        # 1. Luôn thêm chiều u -> v
        self.adj_list[u].append((v, w))

        # 2. Nếu là VÔ HƯỚNG, thêm chiều v -> u (Quan trọng!)
        if not self.directed:
            self.adj_list[v].append((u, w))