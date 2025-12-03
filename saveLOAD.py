import tkinter as tk
import json
from tkinter import messagebox, filedialog
import networkx as nx

def save_graph(self):
        #Kiểm tra nếu đồ thị trống thì báo, không lưu
        if not self.graph.nodes:
            messagebox.showwarning("Cảnh báo", "Đồ thị trống, không có gì để lưu!")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                graph_data = {
                    'directed': self.directed,
                    'weighted': self.weighted,
                    'nodes': list(self.graph.nodes()),
                    #data=True rất quan trọng để lưu được trọng số
                    'edges': list(self.graph.edges(data=True)) 
                }
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(graph_data, f, ensure_ascii=False, indent=2)
                    
                messagebox.showinfo("Thành công", "Đã lưu đồ thị!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể lưu file: {str(e)}")

def load_graph(self):
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    graph_data = json.load(f)
                
                #Cập nhật biến trạng thái
                self.directed = graph_data['directed']
                self.weighted = graph_data['weighted']
                
                #Cập nhật giao diện điều khiển 
                #Để người dùng thấy đúng chế độ đang dùng
                self.graph_type.set("có hướng" if self.directed else "vô hướng")
                self.weight_var.set(self.weighted)
                
                #Khởi tạo lại đồ thị mới dựa trên loại (Có hướng/Vô hướng)
                if self.directed:
                    self.graph = nx.DiGraph()
                else:
                    self.graph = nx.Graph()
                    
                #Nạp dữ liệu đỉnh và cạnh
                self.graph.add_nodes_from(graph_data['nodes'])
                self.graph.add_edges_from(graph_data['edges'])
                
                #Xóa các ô nhập liệu cũ (nếu có) để tránh nhầm lẫn
                self.vertex_entry.delete(0, tk.END)
                self.edge_entry.delete(0, tk.END)

                #Vẽ lại và cập nhật thông tin
                self.update_graph_display()
                self.update_graph_info()
                
                messagebox.showinfo("Thành công", "Đã tải đồ thị!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể tải file: {str(e)}")