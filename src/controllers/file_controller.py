from tkinter import filedialog, messagebox
from utils.file_processor import FileProcessor
from src.models.graph import Graph
class FileController:
    def __init__(self):
        pass

    def handle_save_graph(self, graph, directed, weighted):
        """
        Xử lý logic lưu đồ thị:
        1. Hỏi người dùng nơi lưu
        2. Chuyển đổi dữ liệu Graph -> Dict
        3. Gọi Utils để ghi file
        """
        if not graph.nodes:
            messagebox.showwarning(
                "Cảnh báo", "Đồ thị trống, không có gì để lưu!")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if not filename:
            return  # Người dùng nhấn Cancel

        # Chuẩn bị dữ liệu (Data transformation)
        graph_data = {
            'directed': directed,
            'weighted': weighted,
            'nodes': list(graph.nodes),
            'edges': graph.get_edges(),
        }

        # Gọi tầng Utils để ghi file
        success, result = FileProcessor.write_json(filename, graph_data)
        if success:
            messagebox.showinfo("Thành công", "Đã lưu đồ thị!")
        else:
            messagebox.showerror("Lỗi", f"Không thể lưu file: {result}")

    def handle_load_graph(self):
        """
        Xử lý logic tải đồ thị:
        1. Hỏi người dùng chọn file
        2. Gọi Utils để đọc file
        3. Chuyển đổi dữ liệu Dict -> Graph
        4. Trả về object Graph và các thông số cho AppController
        """
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if not filename:
            return None  # Người dùng nhấn Cancel

        # Gọi tầng Utils để đọc file
        success, data = FileProcessor.read_json(filename)
        if not success:
            messagebox.showerror("Lỗi", f"Không thể đọc file: {data}")
            return None

        try:
            # Parse dữ liệu (Data transformation)
            directed = data['directed']
            weighted = data['weighted']
            nodes = data['nodes']
            edges = data['edges']  # Edges có format: [(u, v, w), ...]

            # 1. Khởi tạo một object Graph mới

            new_graph = Graph(directed=directed, weighted=weighted)

            # 2. KHÔI PHỤC ĐỈNH
            for node in nodes:
                new_graph.add_node(node)

            # 3. KHÔI PHỤC CẠNH VÀ TRỌNG SỐ
            for u, v, w in edges:
                # w là trọng số (float)
                new_graph.add_edge(u, v, w)

            # Trả về dữ liệu đã xử lý sạch sẽ cho AppController
            return {
                'graph': new_graph,
                'directed': directed,
                'weighted': weighted
            }

        except KeyError as e:
            messagebox.showerror(
                "Lỗi", f"File JSON thiếu trường dữ liệu: {str(e)}")
            return None
        except Exception as e:
            messagebox.showerror("Lỗi", f"Dữ liệu file bị hỏng: {str(e)}")
            return None
