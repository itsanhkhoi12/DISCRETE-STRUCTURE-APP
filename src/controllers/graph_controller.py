from models.graph import Graph

class GraphController:
    def __init__(self, app_controller):
        self.app = app_controller
        self.graph = Graph(directed=True)
        self.weighted = self.graph.weighted
        self.directed = self.graph.directed

    def handle_add_edge(self, u, v, w_str):
        """Xử lý khi user bấm nút 'Thêm'"""
        u = u.strip().upper()
        v = v.strip().upper()
        
        if not u or not v:
            self.app.view.log("Lỗi: Tên đỉnh không được để trống.")
            return

        try:
            w = float(w_str)
        except ValueError:
            self.app.view.log("Lỗi: Trọng số phải là số.")
            return

        self.graph.add_edge(u, v, w)
        self.app.view.log(f"Đã thêm cạnh: {u} -> {v} (w={w})")

        self.refresh_view()

    def handle_toggle_mode(self, is_directed):
        """Xử lý khi user tích vào checkbox Có hướng/Vô hướng"""
        self.graph.set_directed(is_directed)
        
        mode = "CÓ HƯỚNG" if is_directed else "VÔ HƯỚNG"
        self.app.view.log(f"Đã chuyển chế độ sang: {mode}")
        
        self.refresh_view()

    def set_new_graph(self, graph, directed, weighted):
        """
        Thay thế đồ thị hiện tại bằng dữ liệu mới được tải từ file.
        Hàm này được gọi từ AppController sau khi FileController đọc file thành công.
        """
        # Cập nhật đối tượng đồ thị
        self.graph = graph
        
        # Cập nhật các trạng thái điều khiển
        self.directed = directed
        self.weighted = weighted
        
        # Bắt buộc phải đồng bộ lại thuộc tính directed trong Model (nếu Graph class có set_directed)
        self.graph.set_directed(directed)

        self.refresh_view()

    def refresh_view(self):
        """Lấy dữ liệu từ Model và ép View vẽ lại"""
        # Lấy danh sách đỉnh và cạnh để vẽ
        nodes = self.graph.nodes
        edges = self.graph.get_edges()
        is_directed = self.graph.directed
        is_weighted = self.weighted

        # Gọi hàm vẽ trong Main Window
        self.app.view.refresh_graph(nodes, edges, is_directed, is_weighted)

    def get_matrix_info(self):
        """Hàm này dùng cho tính năng 'Xem Ma trận'"""
        return self.graph.get_adjacency_matrix()