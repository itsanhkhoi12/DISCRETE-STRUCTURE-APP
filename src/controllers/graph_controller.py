# src/controllers/graph_controller.py
import tkinter as tk
from tkinter import simpledialog, messagebox
from models.graph import Graph

class GraphController:
    def __init__(self, app_controller):
        self.app = app_controller
        self.graph = Graph(directed=True)
        self.weighted = self.graph.weighted
        self.directed = self.graph.directed

    def set_new_graph(self, graph, directed, weighted):
        """Cập nhật đồ thị mới từ file"""
        self.graph = graph
        self.directed = directed
        self.weighted = weighted
        self.graph.set_directed(directed)
        self.refresh_view()

    def refresh_view(self, highlight_edges=None):
        """
        Lấy dữ liệu từ Model và ép View vẽ lại.
        Hỗ trợ tham số highlight_edges để tô màu cạnh.
        """
        nodes = self.graph.nodes
        edges = self.graph.get_edges()
        is_directed = self.graph.directed
        
        self.app.view.refresh_graph(nodes, edges, is_directed, highlight_edges)


    def handle_add_edge(self, u, v, w_str):
        u, v = u.strip().upper(), v.strip().upper()
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
        self.graph.set_directed(is_directed)
        mode = "CÓ HƯỚNG" if is_directed else "VÔ HƯỚNG"
        self.app.view.log(f"Đã chuyển chế độ sang: {mode}")
        self.refresh_view()

    def delete_node(self, node_id):
        if messagebox.askyesno("Xác nhận", f"Xóa đỉnh {node_id}?"):
            self.graph.remove_node(node_id)
            self.app.view.log(f"Đã xóa đỉnh: {node_id}")
            self.refresh_view()

    def delete_edge(self, u, v):
        if messagebox.askyesno("Xác nhận", f"Xóa cạnh {u}-{v}?"):
            self.graph.remove_edge(u, v)
            self.app.view.log(f"Đã xóa cạnh: {u}-{v}")
            self.refresh_view()

    def edit_edge_weight(self, u, v):
        current_w = self.graph.adj_list[u].get(v, 1.0)
        new_w_str = simpledialog.askstring("Sửa trọng số", f"Trọng số mới cho {u}->{v}:", initialvalue=str(current_w), parent=self.app.root)
        if new_w_str is not None:
            try:
                new_w = float(new_w_str)
                self.graph.add_edge(u, v, new_w)
                self.app.view.log(f"Cập nhật {u}->{v}: {new_w}")
                self.refresh_view()
            except ValueError:
                self.app.view.log("Lỗi: Trọng số không hợp lệ!")
    
    def handle_reverse_edge(self,u,v):
        if self.graph.reverse_edge(u,v):
            self.app.view.log(f"Đã đảo chiều cạnh {u}-{v} thành cạnh {v}-{u}")
            self.refresh_view()
        else:
            self.app.view.log(f"Không thể đảo chiều! (Chỉ đảo chiều được với đồ thị có hướng)")

    def handle_rename_node(self, old_name):
        new_name = simpledialog.askstring("Đổi tên", f"Tên mới cho đỉnh '{old_name}':", parent=self.app.root)
        if new_name:
            new_name = new_name.strip().upper()
            if hasattr(self.graph, 'rename_node'):
                if self.graph.rename_node(old_name, new_name):
                    self.app.view.log(f"Đổi tên: {old_name} -> {new_name}")
                    self.refresh_view()
                else:
                    messagebox.showerror("Lỗi", "Tên mới không hợp lệ!")
            else:
                 self.app.view.log("Model chưa hỗ trợ đổi tên.")


    def apply_node_coloring(self, color_map):
        """Tô màu các node dựa trên color_map {node: color_code}"""
        visual_colors = {0: "#3498db", 1: "#e74c3c", 2: "#2ecc71"}
        canvas = self.app.view.canvas_view
        
        for node, color_code in color_map.items():
            if node in canvas.node_positions:
                fill_color = visual_colors.get(color_code, "#3498db")
                x, y = canvas.node_positions[node]
                canvas._draw_single_node(node, x, y, color=fill_color)

    def show_node_context_menu(self, event, node_id):
        menu = tk.Menu(self.app.root, tearoff=0)
        menu.add_command(label=f"Đỉnh: {node_id}", state="disabled")
        menu.add_separator()
        menu.add_command(label="Đổi tên", command=lambda: self.handle_rename_node(node_id))
        menu.add_command(label="Xóa Đỉnh", command=lambda: self.delete_node(node_id))
        menu.post(event.x_root, event.y_root)

    def show_edge_context_menu(self, event, u, v):
        menu = tk.Menu(self.app.root, tearoff=0)
        menu.add_command(label=f"Cạnh: {u} -> {v}", state="disabled")
        menu.add_separator()

        menu.add_command(label = "Đảo chiều mũi tên", command = lambda: self.handle_reverse_edge(u,v))
        menu.add_command(label="Sửa Trọng số", command=lambda: self.edit_edge_weight(u, v))
        menu.add_command(label="Xóa Cạnh", command=lambda: self.delete_edge(u, v))
        
        menu.post(event.x_root, event.y_root)


