import tkinter as tk
from src.views.main_window import MainWindow

# --- MOCK CONTROLLER (GIẢ LẬP) ---
class DummyController:
    """
    Class này đóng vai trò là 'diễn viên đóng thế' cho Controller thật.
    Nó chứa đủ các hàm mà UI yêu cầu, nhưng chỉ in ra log thay vì chạy thật.
    """
    def __init__(self):
        self.view = None # Sẽ được gán sau

    # Các hàm xử lý sự kiện (Actions)
    def action_load(self):
        self.view.log("Simulate: Đang mở file...")

    def action_save(self):
        self.view.log("Simulate: Đang lưu file...")

    def toggle_mode(self):
        # Lấy giá trị từ biến Var trong View
        is_directed = self.view.control_panel.var_directed.get()
        mode = "CÓ HƯỚNG" if is_directed else "VÔ HƯỚNG"
        self.view.log(f"Simulate: Đã đổi chế độ sang {mode}")
        # Giả vờ vẽ lại đồ thị (gọi hàm vẽ rỗng hoặc vẽ test)
        # self.view.refresh_graph(...) 

    def action_add_edge(self):
        # Lấy dữ liệu từ các ô nhập trong View
        u = self.view.control_panel.ent_u.get()
        v = self.view.control_panel.ent_v.get()
        w = self.view.control_panel.ent_w.get()
        self.view.log(f"Simulate: Thêm cạnh {u} -> {v} (w={w})")

    def action_convert_view(self):
        self.view.log("Simulate: Mở cửa sổ xem Ma trận/DS kề")
        # Bạn có thể code thử mở cửa sổ dialog ở đây nếu muốn test dialog
        # from views.dialogs.converter_view import ConverterView
        # ConverterView(self.view.root, "Matrix...", "Adj...", "Edges...")

    def run_basic_algo(self, algo_type):
        start_node = self.view.control_panel.ent_start_node.get()
        self.view.log(f"Simulate: Chạy thuật toán {algo_type} từ đỉnh '{start_node}'")

    def run_advanced_algo(self):
        algo_name = self.view.control_panel.combo_algo.get()
        self.view.log(f"Simulate: Chạy thuật toán nâng cao: {algo_name}")

# --- CHẠY APP ---
if __name__ == "__main__":
    # 1. Khởi tạo Tkinter
    root = tk.Tk()

    # 2. Khởi tạo Controller giả
    controller = DummyController()

    # 3. Khởi tạo View chính và tiêm Controller giả vào
    app = MainWindow(root, controller)
    
    # 4. Gắn ngược view vào controller (để controller giả có thể gọi hàm log của view)
    controller.view = app

    # 5. Chạy vòng lặp
    print("Đang khởi động chế độ Test UI...")
    root.mainloop()