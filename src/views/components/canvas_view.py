import tkinter as tk
import math
from utils.layout_math import LayoutMath 

class CanvasView(tk.Canvas):
    def __init__(self, master, controller = None, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.configure(bg="white")
        self.node_positions = {}
        
        self.COLOR_NODE = "#3498db"
        self.COLOR_TEXT = "white"
        self.COLOR_EDGE = "#2c3e50"
        self.bind("<Button-3>", self.on_right_click)

    def draw_graph(self, nodes, edges, is_directed, highlight_edges=None):
        """
        highlight_edges: List các tuple [(u, v), ...] cần tô màu nổi bật
        """
        self.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()
        if w < 50: w, h = 800, 600
        
        # 1. Tính toán vị trí
        self.node_positions = LayoutMath.calculate_circular_positions(nodes, w, h)
        
        # Chuẩn bị set highlight để tra cứu nhanh O(1)
        highlight_set = set()
        if highlight_edges:
            for u, v in highlight_edges:
                highlight_set.add((u, v))
                highlight_set.add((v, u)) # Hỗ trợ đồ thị vô hướng (tô cả 2 chiều)

        # 2. Vẽ Cạnh
        for u, v, weight in edges:
            if u in self.node_positions and v in self.node_positions:
                is_highlight = (u, v) in highlight_set
                self._draw_single_edge(u, v, weight, is_directed, is_highlight)

        # 3. Vẽ Đỉnh
        for node, (x, y) in self.node_positions.items():
            self._draw_single_node(node, x, y)
        
        # (Đã xóa đoạn code lặp lại ở đây)

    def on_right_click(self, event):
        item = self.find_closest(event.x, event.y)
        tags = self.gettags(item)
        if not tags: return

        if "node" in tags:
            node_tag = [t for t in tags if t.startswith("node_")][0]
            node_id = node_tag.split("_")[1]
            if self.controller:
                self.controller.show_node_context_menu(event, node_id)
                
        elif "edge" in tags:
            potential = [t for t in tags if t.startswith("edge_")]
            if potential:
                edge_tag = potential[0]
                parts = edge_tag.split("_")
                if len(parts) >= 3:
                    u, v = parts[1], parts[2]
                    if self.controller:
                        self.controller.show_edge_context_menu(event, u, v)

    def _draw_single_edge(self, u, v, weight, is_directed, is_highlight=False):
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
        
        if is_highlight:
            color = "#e74c3c" # Màu đỏ cam nổi bật
            width = 4       
        else:
            color = self.COLOR_EDGE
            width = 3

        tag_id = f"edge_{u}_{v}"
        edge_tags = ('edge', tag_id)

        self.create_line(start_x, start_y, end_x, end_y, 
                         fill=color, width=width,
                         arrow=arrow_opt, arrowshape=(10, 12, 5),
                         tags=edge_tags)
        
        mid_x = (start_x + end_x) / 2
        mid_y = (start_y + end_y) / 2
        
        # Vẽ background cho text trọng số để dễ nhìn
        self.create_rectangle(mid_x-10, mid_y-10, mid_x+10, mid_y+10, 
                              fill="white", outline="", tags=edge_tags)
        
        text_color = "red" # Mặc định trọng số màu đỏ
        
        weight_text = str(int(weight) if weight % 1 == 0 else weight)
        self.create_text(mid_x, mid_y, text=weight_text, 
                         fill=text_color, font=("Arial", 9, "bold"),
                         tags=edge_tags)

    def _draw_single_node(self, label, x, y, color=None):
        r = 20
        fill_color = color if color else self.COLOR_NODE
        tag_id = f"node_{label}"
        self.create_oval(x-r, y-r, x+r, y+r, fill=fill_color, outline="white", width=2,tags=('node',tag_id))
        self.create_text(x, y, text=str(label), fill=self.COLOR_TEXT, font=("Arial", 12, "bold"),tags=('node',tag_id))