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
        self.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()
        if w < 50: w, h = 800, 600
        
        # 1. Tính toán vị trí bằng thuật toán Lò xo (Spring Layout)
        self.node_positions = LayoutMath.calculate_spring_positions(nodes, edges, w, h)
        
        # 2. Xử lý highlight
        highlight_set = set()
        if highlight_edges:
            for u, v in highlight_edges:
                highlight_set.add((u, v))
                if not is_directed: 
                    highlight_set.add((v, u))

        # 3. Tạo set chứa tất cả các cạnh để tra cứu nhanh O(1)
        existing_edges = set()
        for u, v, w_val in edges:
            existing_edges.add((u, v))

        # 4. Vẽ từng cạnh
        for u, v, weight in edges:
            if u not in self.node_positions or v not in self.node_positions:
                continue
            
            is_highlight = (u, v) in highlight_set
            
            # Kiểm tra xem có cạnh ngược lại không (v -> u)
            has_reverse = (v, u) in existing_edges
            
            # Nếu là đồ thị CÓ HƯỚNG và CÓ CẠNH NGƯỢC -> Vẽ cong để né nhau
            curvature = 0
            if is_directed and has_reverse and u != v:
                curvature = 30 # Độ cong (pixel)
            
            self._draw_smart_edge(u, v, weight, is_directed, curvature, is_highlight)

        # 5. Vẽ Đỉnh (Nodes) - Vẽ sau cùng để đè lên cạnh
        for node, (x, y) in self.node_positions.items():
            self._draw_single_node(node, x, y)

    def _draw_smart_edge(self, u, v, weight, is_directed, curvature, is_highlight):
        x1, y1 = self.node_positions[u]
        x2, y2 = self.node_positions[v]
        
        # Cấu hình màu sắc
        if is_highlight:
            color = "#e74c3c" # Đỏ cam
            width = 3
            text_color = "red"
        else:
            color = self.COLOR_EDGE
            width = 2
            text_color = "black"

        tag_id = f"edge_{u}_{v}"
        edge_tags = ('edge', tag_id)
        
        arrow_opt = tk.LAST if is_directed else None

        # --- TRƯỜNG HỢP 1: VẼ THẲNG (Không cong) ---
        if curvature == 0:
            # Tính điểm lùi lại để mũi tên không đâm vào tâm node
            angle = math.atan2(y2 - y1, x2 - x1)
            r = 20
            start_x = x1 + r * math.cos(angle)
            start_y = y1 + r * math.sin(angle)
            end_x = x2 - r * math.cos(angle)
            end_y = y2 - r * math.sin(angle)

            self.create_line(start_x, start_y, end_x, end_y, 
                             fill=color, width=width, 
                             arrow=arrow_opt, arrowshape=(10, 12, 5),
                             tags=edge_tags)
            
            mid_x = (start_x + end_x) / 2
            mid_y = (start_y + end_y) / 2
            self._draw_weight(mid_x, mid_y, weight, text_color, edge_tags)
            
        # --- TRƯỜNG HỢP 2: VẼ CONG (Bezier) ---
        else:
            # 1. Tính trung điểm M
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            
            # 2. Tính vector pháp tuyến để tìm điểm điều khiển C
            dx, dy = x2 - x1, y2 - y1
            dist = math.sqrt(dx*dx + dy*dy)
            if dist == 0: return

            # Vector vuông góc (-dy, dx)
            norm_x, norm_y = -dy / dist, dx / dist
            
            # Điểm điều khiển (lệch sang phải so với chiều đi)
            cx = mx + norm_x * curvature
            cy = my + norm_y * curvature

            # 3. Tạo đường cong mượt bằng nhiều đoạn thẳng nhỏ
            points = []
            steps = 15
            for i in range(steps + 1):
                t = i / steps
                # Công thức Bezier bậc 2
                bx = (1-t)**2 * x1 + 2*(1-t)*t * cx + t**2 * x2
                by = (1-t)**2 * y1 + 2*(1-t)*t * cy + t**2 * y2
                points.append(bx)
                points.append(by)

            self.create_line(*points, 
                             fill=color, width=width, 
                             arrow=arrow_opt, arrowshape=(10, 12, 5),
                             smooth=True,
                             tags=edge_tags)

            # 4. Vẽ trọng số tại đỉnh parabol (điểm giữa của mảng points)
            mid_idx = len(points) // 2
            if mid_idx % 2 != 0: mid_idx -= 1
            wx, wy = points[mid_idx], points[mid_idx+1]
            
            self._draw_weight(wx, wy, weight, text_color, edge_tags)

    def _draw_weight(self, x, y, weight, color, tags):
        """Vẽ nhãn trọng số có nền trắng"""
        text = str(int(weight) if weight % 1 == 0 else weight)
        self.create_rectangle(x-10, y-10, x+10, y+10, fill="white", outline="", tags=tags)
        self.create_text(x, y, text=text, fill=color, font=("Arial", 9, "bold"), tags=tags)

    def _draw_single_node(self, label, x, y, color=None):
        r = 20
        fill_color = color if color else self.COLOR_NODE
        tag_id = f"node_{label}"
        self.create_oval(x-r, y-r, x+r, y+r, fill=fill_color, outline="white", width=2,
                         tags=('node', tag_id))
        self.create_text(x, y, text=str(label), fill=self.COLOR_TEXT, 
                         font=("Arial", 12, "bold"), tags=('node', tag_id))

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