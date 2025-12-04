import tkinter as tk
import math
from src.utils.layout_math import LayoutMath


class CanvasView(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(bg="white")
        self.node_positions = {}

        # Màu sắc cấu hình riêng cho Canvas
        self.COLOR_NODE = "#3498db"
        self.COLOR_TEXT = "white"
        self.COLOR_EDGE = "#2c3e50"

    def draw_graph(self, nodes, edges, is_directed, is_weighted):
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
        if w < 10:
            w, h = 800, 600

        # 1. Tính toán vị trí
        self.node_positions = LayoutMath.calculate_circular_positions(
            nodes, w, h)

        # 2. Vẽ Cạnh (Edges)
        for u, v, weight in edges:
            if u in self.node_positions and v in self.node_positions:
                self._draw_single_edge(u, v, weight, is_directed, is_weighted)

        # 3. Vẽ Đỉnh (Nodes)
        for node, (x, y) in self.node_positions.items():
            self._draw_single_node(node, x, y)

    def _draw_single_edge(self, u, v, weight, is_directed, is_weighted):
        x1, y1 = self.node_positions[u]
        x2, y2 = self.node_positions[v]

        dx, dy = x2 - x1, y2 - y1
        dist = math.sqrt(dx*dx + dy*dy)
        if dist == 0:
            return

        # Tính toán điểm vẽ để không đè lên hình tròn
        r = 20
        start_x = x1 + (dx/dist) * r
        start_y = y1 + (dy/dist) * r
        end_x = x2 - (dx/dist) * r
        end_y = y2 - (dy/dist) * r

        arrow_opt = tk.LAST if is_directed else None

        # Vẽ đường thẳng
        self.create_line(start_x, start_y, end_x, end_y,
                         fill=self.COLOR_EDGE, width=2,
                         arrow=arrow_opt, arrowshape=(10, 12, 5))

        # vẽ trọng số weight
        if is_weighted:
            mid_x = (start_x + end_x) / 2
            mid_y = (start_y + end_y) / 2

            # Khung nền trắng cho trọng số để dễ đọc
            self.create_rectangle(mid_x-10, mid_y-10, mid_x+10, mid_y+10,
                                  fill="white", outline="")

            # Vẽ văn bản trọng số
            # Đảm bảo hiển thị là số nguyên nếu trọng số là X.0
            weight_text = str(int(weight) if weight % 1 == 0 else weight)

            self.create_text(mid_x, mid_y, text=weight_text,
                             fill="red", font=("Arial", 9, "bold"))

    def _draw_single_node(self, label, x, y):
        r = 20
        self.create_oval(x-r, y-r, x+r, y+r,
                         fill=self.COLOR_NODE, outline="white", width=2)
        self.create_text(x, y, text=str(label),
                         fill=self.COLOR_TEXT, font=("Arial", 12, "bold"))

    def highlight_mst(self, edges, color="#00FF00"):
        """Tô màu cây khung nhỏ nhất – dùng cho Prim & Kruskal"""
        self.delete("mst_highlight")  # Xóa cây cũ

        for u, v, _ in edges:
            if u in self.node_positions and v in self.node_positions:
                x1, y1 = self.node_positions[u]
                x2, y2 = self.node_positions[v]

                dx = x2 - x1
                dy = y2 - y1
                dist = (dx**2 + dy**2)**0.5
                if dist == 0:
                    continue

                r = 20
                sx = x1 + (dx/dist) * r
                sy = y1 + (dy/dist) * r
                ex = x2 - (dx/dist) * r
                ey = y2 - (dy/dist) * r

                line = self.create_line(sx, sy, ex, ey,
                                        fill=color, width=8,
                                        tags="mst_highlight")
                self.tag_raise(line)  # Đưa lên trên cùng

    def highlight_edges(self, edges, color="#00FF00"):
        """
        Tô màu các cạnh của cây khung nhỏ nhất (Prim/Kruskal)
        edges: danh sách [(u, v, w), ...]
        color: màu xanh lá đẹp
        """
        # Xóa các đường tô cũ trước
        self.delete("mst_highlight")

        for u, v, w in edges:
            if u not in self.node_positions or v not in self.node_positions:
                continue

            x1, y1 = self.node_positions[u]
            x2, y2 = self.node_positions[v]

            # Tính điểm đầu/cuối để không đè lên node
            dx = x2 - x1
            dy = y2 - y1
            dist = math.sqrt(dx**2 + dy**2)
            if dist == 0:
                continue

            r = 22  # bán kính node + margin
            start_x = x1 + (dx / dist) * r
            start_y = y1 + (dy / dist) * r
            end_x = x2 - (dx / dist) * r
            end_y = y2 - (dy / dist) * r

            # Vẽ đường xanh lá ĐẬM, ĐẸP, NỔI BẬT
            line = self.create_line(
                start_x, start_y, end_x, end_y,
                fill=color,
                width=9,               # Đậm để thấy rõ
                capstyle=tk.ROUND,
                tags="mst_highlight"
            )
            # Đưa lên trên cùng
            self.tag_raise(line)
