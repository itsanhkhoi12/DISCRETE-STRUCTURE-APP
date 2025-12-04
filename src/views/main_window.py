import tkinter as tk
from .components.control_panel import ControlPanel
from .components.canvas_view import CanvasView


class MainWindow:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("Ứng dụng Đồ thị - Cấu trúc Rời rạc")
        self.root.geometry("1200x750")

        # Màu nền chung
        BG_COLOR = "#f4f6f7"

        # Setup Layout chính (PanedWindow)
        main_container = tk.PanedWindow(
            self.root, orient=tk.HORIZONTAL, bg="#2c3e50")
        main_container.pack(fill=tk.BOTH, expand=True)

        # 1. Khởi tạo Control Panel (Truyền controller vào để xử lý nút bấm)
        self.control_panel = ControlPanel(
            main_container, controller=self.controller, bg=BG_COLOR, width=350)
        main_container.add(self.control_panel)

        # 2. Khởi tạo Canvas View
        self.canvas_view = CanvasView(main_container, bg="white")
        main_container.add(self.canvas_view)

    # SỬA ĐỔI: Thêm tham số 'is_weighted'
    def refresh_graph(self, nodes, edges, is_directed, is_weighted):
        """Hàm này để Controller gọi khi cần vẽ lại đồ thị"""

        # LƯU Ý: Bạn cũng cần đảm bảo hàm draw_graph trong CanvasView
        # chấp nhận tham số is_weighted
        # <-- Truyền thêm is_weighted
        self.canvas_view.draw_graph(nodes, edges, is_directed, is_weighted)

    def log(self, message):
        """Hàm này để Controller gọi khi cần ghi log"""
        self.control_panel.append_log(message)
