import sys
import os
from algorithms.traversal import Traversal
from algorithms.properties import Bipartite
from models.graph import Graph
from tkinter import messagebox

current_dir = os.path.dirname(os.path.abspath(__file__)) 
parent_dir = os.path.dirname(current_dir) 
sys.path.append(parent_dir)



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
        # Đồng bộ lại thuộc tính directed trong Model Graph
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

    def handle_traversal(self,method,start_node):
        start_node = start_node.strip().upper()
        if not start_node:
            messagebox.showwarning("Cảnh báo", "Cần nhập đỉnh bắt đầu!")
            return
        
        path = []
        if method == 'BFS':
            path = Traversal.bfs_traversal(self.graph, start_node)
        elif method == 'DFS':
            path = Traversal.dfs_traversal(self.graph, start_node)

        if not path:
            self.app.view.log(f"Không tìm thấy đường đi hoặc đỉnh bắt đầu {start_node} không tồn tại!")
            return
        
        result = '->'.join(path)
        self.app.view.log(f"Kết quả {method} từ đỉnh {start_node}: ")
        self.app.view.log(result)

        # Highlight màu đỏ đường đi của các đỉnh đã duyệt trong path
        path_map = {node: 1 for node in path}
        self.apply_coloring(path_map)

    # Kiểm tra đồ thị hai phía
    def handle_check_bipartite(self):
        if not self.graph.nodes:
            messagebox.showwarning("Cảnh báo", "Đồ thị trống!")
            return

        is_bipartite, color_map = Bipartite.check_bipartite(self.graph)

        if is_bipartite:
            msg = "KẾT LUẬN: Đây là đồ thị 2 phía."
            self.app.view.log(msg)
            messagebox.showinfo("Kết quả", msg)
            
            v1 = [n for n, c in color_map.items() if c == 1]
            v2 = [n for n, c in color_map.items() if c == 2]
            self.app.view.log(f"-> Tập 1 (Đỏ): {v1}")
            self.app.view.log(f"-> Tập 2 (Xanh lá): {v2}")

            self.apply_coloring(color_map)
        else:
            msg = "KẾT LUẬN: Không phải đồ thị 2 phía."
            self.app.view.log(msg)
            messagebox.showerror("Kết quả", msg)
            self.refresh_view()

    def apply_coloring(self, color_map):
        visual_colors = {
            0: "#3498db",
            1: "#e74c3c",
            2: "#2ecc71"
        }

        canvas = self.app.view.canvas_view
        
        for node, color_code in color_map.items():
            if node in canvas.node_positions:
                fill_color = visual_colors.get(color_code, "#3498db")
                x, y = canvas.node_positions[node]
                canvas._draw_single_node(node, x, y, color=fill_color)