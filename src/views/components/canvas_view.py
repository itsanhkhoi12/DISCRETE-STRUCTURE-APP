import tkinter as tk
import math
from utils.layout_math import LayoutMath 

class CanvasView(tk.Canvas):
    def __init__(self, master, controller = None, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.configure(bg="white")
        self.node_positions = {}
        
        # Màu sắc cấu hình riêng cho Canvas
        self.COLOR_NODE = "#3498db"
        self.COLOR_TEXT = "white"
        self.COLOR_EDGE = "#2c3e50"
        self.bind("<Button-3>", self.on_right_click)

    def draw_graph(self, nodes, edges, is_directed):
        """
        Hàm chính để vẽ đồ thị.
        - nodes: Set hoặc list các đỉnh
        - edges: List các tuple (u, v, w)
        - is_directed: Boolean
        """
        self.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()
        
        # Fix lỗi hiển thị khi mới mở app (width/height chưa kịp load)
        if w < 10: w, h = 800, 600
        
        # 1. Tính toán vị trí
        self.node_positions = LayoutMath.calculate_circular_positions(nodes, w, h)

        # 2. Vẽ Cạnh (Edges)
        for u, v, weight in edges:
            if u in self.node_positions and v in self.node_positions:
                self._draw_single_edge(u, v, weight, is_directed)

        # 3. Vẽ Đỉnh (Nodes)
        for node, (x, y) in self.node_positions.items():
            self._draw_single_node(node, x, y)

    def on_right_click(self, event):
        """Xử lý khi click chuột phải lên Canvas"""
        # Tìm vật thể gần vị trí click nhất
        item = self.find_closest(event.x, event.y)
        tags = self.gettags(item)
        if not tags: return

        # tags có dạng ('current', 'node', 'node_A') hoặc ('edge', 'edge_A_B')
        if "node" in tags:
            # Lấy tag chứa ID (vd: node_A -> lấy A)
            node_tag = [t for t in tags if t.startswith("node_")][0]
            node_id = node_tag.split("_")[1]
            # Gọi Controller xử lý menu cho Đỉnh
            if self.controller:
                self.controller.show_node_context_menu(event, node_id)
                
        elif "edge" in tags:
            # Lọc tag edge_...
            potential = [t for t in tags if t.startswith("edge_")]
            
            # Đảm bảo danh sách không rỗng
            if potential:
                edge_tag = potential[0]
                parts = edge_tag.split("_")
                # edge_A_B -> Đảm bảo string tag phải có ít nhất 3 phần tử (edge, hai đỉnh được nối với nhau)
                if len(parts) >= 3:
                    u, v = parts[1], parts[2]
                    if self.controller:
                        self.controller.show_edge_context_menu(event, u, v)

    def _draw_single_edge(self, u, v, weight, is_directed):
        x1, y1 = self.node_positions[u]
        x2, y2 = self.node_positions[v]
        
        dx, dy = x2 - x1, y2 - y1
        dist = math.sqrt(dx*dx + dy*dy)
        if dist == 0: return
        
        r = 20 
        start_x = x1 + (dx/dist) * r
        start_y = y1 + (dy/dist) * r
        end_x = x2 - (dx/dist) * r
        end_y = y2 - (dy/dist) * r
        
        arrow_opt = tk.LAST if is_directed else None
        
        # ID định danh cho cạnh
        tag_id = f"edge_{u}_{v}"
        # Nhóm tag chung cho tất cả thành phần của cạnh
        edge_tags = ('edge', tag_id)

        # 1. Vẽ đường thẳng (Tăng độ dày lên 3 hoặc 4 để dễ bấm)
        self.create_line(start_x, start_y, end_x, end_y, 
                         fill=self.COLOR_EDGE, width=3, 
                         arrow=arrow_opt, arrowshape=(10, 12, 5),
                         tags=edge_tags)
        
        # Tính vị trí trọng số
        mid_x = (start_x + end_x) / 2
        mid_y = (start_y + end_y) / 2
        
        # 2. Vẽ nền trắng cho trọng số (Cũng gán tag để bấm vào nền trắng vẫn ăn)
        self.create_rectangle(mid_x-10, mid_y-10, mid_x+10, mid_y+10, 
                              fill="white", outline="",
                              tags=edge_tags) # <--- Gán tag
        
        # 3. Vẽ chữ số trọng số (Cũng gán tag nốt)
        weight_text = str(int(weight) if weight % 1 == 0 else weight)
        self.create_text(mid_x, mid_y, text=weight_text, 
                         fill="red", font=("Arial", 9, "bold"),
                         tags=edge_tags) # <--- Gán tag

    def _draw_single_node(self, label, x, y, color=None):
        r = 20
        # Nếu không truyền màu thì lấy màu mặc định
        fill_color = color if color else self.COLOR_NODE
        tag_id = f"node_{label}"
        self.create_oval(x-r, y-r, x+r, y+r, fill=fill_color, outline="white", width=2,tags=('node',tag_id))
        self.create_text(x, y, text=str(label), fill=self.COLOR_TEXT, font=("Arial", 12, "bold"),tags=('node',tag_id))
