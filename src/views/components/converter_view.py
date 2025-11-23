import tkinter as tk
from tkinter import ttk

class ConverterView(tk.Toplevel):
    def __init__(self, master, matrix_str, adj_list_str, edge_list_str):
        """
        Khởi tạo cửa sổ popup.
        Nhận vào 3 chuỗi string đã được xử lý từ Controller/Utils
        """
        super().__init__(master)
        self.title("Các dạng biểu diễn Đồ thị")
        self.geometry("650x500")
        
        # Tạo Notebook (Tab container)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Tạo 3 tab
        self._create_tab("Ma trận kề", matrix_str)
        self._create_tab("Danh sách kề", adj_list_str)
        self._create_tab("Danh sách cạnh", edge_list_str)

        # Nút đóng
        btn_close = ttk.Button(self, text="Đóng", command=self.destroy)
        btn_close.pack(pady=5)

    def _create_tab(self, title, content):
        frame = tk.Frame(self.notebook)
        self.notebook.add(frame, text=title)
        
        # Text widget có thanh cuộn (Scrollbar)
        text_area = tk.Text(frame, font=("Consolas", 11), wrap=tk.NONE)
        
        # Scrollbar dọc
        scroll_y = tk.Scrollbar(frame, orient=tk.VERTICAL, command=text_area.yview)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Scrollbar ngang (cho ma trận lớn)
        scroll_x = tk.Scrollbar(frame, orient=tk.HORIZONTAL, command=text_area.xview)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        text_area.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Insert dữ liệu và khóa không cho sửa
        text_area.insert(tk.END, content)
        text_area.config(state=tk.DISABLED) # Read-only