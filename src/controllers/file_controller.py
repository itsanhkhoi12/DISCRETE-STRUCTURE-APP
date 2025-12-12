import os
from tkinter import filedialog, messagebox
from utils.file_processor import FileProcessor
from models.graph import Graph

class FileController:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        src_dir = os.path.dirname(current_dir)
        root_dir = os.path.dirname(src_dir)
        
        self.default_dir = os.path.join(root_dir, 'data')
        if not os.path.exists(self.default_dir):
            try:
                os.makedirs(self.default_dir)
                print(f"Đã tự động tạo thư mục dữ liệu tại: {self.default_dir}")
            except OSError as e:
                print(f"Lỗi không thể tạo thư mục: {e}")
                self.default_dir = "." 

    def handle_save_graph(self, graph, directed, weighted):
        """
        Xử lý logic lưu đồ thị
        """
        if not graph.nodes:
            messagebox.showwarning("Cảnh báo", "Đồ thị trống, không có gì để lưu!")
            return

        # Mở hộp thoại lưu file tại thư mục mặc định
        filename = filedialog.asksaveasfilename(
            initialdir=self.default_dir,  # <--- Tự động trỏ vào folder data
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Lưu Đồ thị"
        )
        
        if not filename:
            return # Người dùng nhấn Cancel

        # Chuẩn bị dữ liệu
        graph_data = {
            'directed': directed,
            'weighted': weighted,
            'nodes': list(graph.nodes),
            'edges': graph.get_edges(),
        }

        # Gọi tầng Utils để ghi file
        success, result = FileProcessor.write_json(filename, graph_data)
        
        if success:
            messagebox.showinfo("Thành công", f"Đã lưu đồ thị vào:\n{filename}")
        else:
            messagebox.showerror("Lỗi", f"Không thể lưu file: {result}")

    def handle_load_graph(self):
        """
        Xử lý logic tải đồ thị
        """
        # Mở hộp thoại chọn file tại thư mục mặc định
        filename = filedialog.askopenfilename(
            initialdir=self.default_dir, # <--- Tự động trỏ vào folder data
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Mở Đồ thị"
        )
        
        if not filename:
            return None # Người dùng nhấn Cancel

        # Gọi tầng Utils để đọc file
        success, data = FileProcessor.read_json(filename)
        
        if not success:
            messagebox.showerror("Lỗi", f"Không thể đọc file: {data}")
            return None

        try:
            # Parse dữ liệu
            directed = data['directed']
            weighted = data['weighted']
            nodes = data['nodes']
            edges = data['edges']
            
            # 1. Khởi tạo graph mới
            new_graph = Graph(directed=directed, weighted=weighted)
            
            # 2. Khôi phục đỉnh
            for node in nodes:
                new_graph.add_node(node)
                
            # 3. Khôi phục cạnh
            for u, v, w in edges:
                new_graph.add_edge(u, v, w) 
            
            return {
                'graph': new_graph,
                'directed': directed,
                'weighted': weighted
            }
            
        except KeyError as e:
            messagebox.showerror("Lỗi", f"File JSON thiếu trường dữ liệu: {str(e)}")
            return None
        except Exception as e:
            messagebox.showerror("Lỗi", f"Dữ liệu file bị hỏng: {str(e)}")
            return None