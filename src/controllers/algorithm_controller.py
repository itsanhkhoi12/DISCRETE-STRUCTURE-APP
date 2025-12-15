# src/controllers/algorithm_controller.py
from tkinter import messagebox
from algorithms.traversal import Traversal
from algorithms.properties import Bipartite
from algorithms.mst import MST
from algorithms.euler import Euler
from algorithms.flow import Flow
from algorithms.path_finding import PathFinding

class AlgorithmController:
    def __init__(self, app_controller):
        self.app = app_controller

    @property
    def graph(self):
        return self.app.graph_ctrl.graph

    def handle_bfs(self, start_node):
        start_node = start_node.strip().upper()
        if not start_node:
            messagebox.showwarning("Cảnh báo", "Cần nhập đỉnh bắt đầu!")
            return
        
        path = Traversal.bfs_traversal(self.graph, start_node)
        self._display_path_node_result("BFS", start_node, path)

    def handle_dfs(self, start_node):
        start_node = start_node.strip().upper()
        if not start_node:
            messagebox.showwarning("Cảnh báo", "Cần nhập đỉnh bắt đầu!")
            return

        path = Traversal.dfs_traversal(self.graph, start_node)
        self._display_path_node_result("DFS", start_node, path)

    def handle_check_bipartite(self):
        if not self.graph.nodes:
            messagebox.showwarning("Cảnh báo", "Đồ thị trống!")
            return

        is_bipartite, color_map = Bipartite.check_bipartite(self.graph)

        if is_bipartite:
            msg = "KẾT LUẬN: Đây là đồ thị 2 phía."
            self.app.view.log(msg)
            messagebox.showinfo("Kết quả", msg)
            self.app.graph_ctrl.apply_node_coloring(color_map)
        else:
            msg = "KẾT LUẬN: Không phải đồ thị 2 phía."
            self.app.view.log(msg)
            messagebox.showerror("Kết quả", msg)
            self.app.graph_ctrl.refresh_view()

    def handle_advanced_algo(self, algo_name, start_node=None, end_node=None):
        self.app.view.log(f"--- Đang chạy thuật toán: {algo_name} ---")
        
        if algo_name == "Prim":
            mst_edges, total_w = MST.prim(self.graph)
            self._display_mst_result(mst_edges, total_w)

        elif algo_name == "Kruskal":
            mst_edges, total_w = MST.kruskal(self.graph)
            self._display_mst_result(mst_edges, total_w)

        elif algo_name == "Fleury":
            path = Euler.fleury(self.graph, start_node)
            self._display_euler_result(path)

        elif algo_name == "Hierholzer":
            path = Euler.hierholzer(self.graph, start_node)
            self._display_euler_result(path)

        elif algo_name == "Ford-Fulkerson":
            if not start_node or not end_node:
                 messagebox.showwarning("Thiếu thông tin", "Cần nhập Đỉnh đầu và Đỉnh đích cho thuật toán Luồng!")
                 return
            max_flow = Flow.ford_fulkerson(self.graph, start_node, end_node)
            self.app.view.log(f"Luồng cực đại từ {start_node} -> {end_node}: {max_flow}")
            messagebox.showinfo("Kết quả", f"Luồng cực đại: {max_flow}")


    def _display_path_node_result(self, method, start, path):
        """Hiển thị kết quả duyệt đỉnh (tô màu node)"""
        if not path:
            self.app.view.log(f"Không tìm thấy đường đi từ {start}!")
            return
        
        result = '->'.join(map(str, path))
        self.app.view.log(f"Kết quả {method}: {result}")
        
        # Tô màu các đỉnh đã đi qua
        path_map = {node: 1 for node in path}
        self.app.graph_ctrl.apply_node_coloring(path_map)

    def _display_mst_result(self, edges, total_weight):
        """Hiển thị kết quả cây khung (tô màu cạnh)"""
        if not edges and total_weight == 0:
             self.app.view.log("Không tìm thấy cây khung (Đồ thị rời rạc hoặc rỗng).")
             return

        self.app.view.log(f"Tổng trọng số cây khung: {total_weight}")
        
        highlight_list = []
        for u, v, w in edges:
            self.app.view.log(f"Chọn cạnh: {u} - {v} ({w})")
            highlight_list.append((u, v))
            
        # Gọi GraphController để vẽ lại và highlight cạnh
        self.app.graph_ctrl.refresh_view(highlight_edges=highlight_list)

    def _display_euler_result(self, path):
        if not path:
            self.app.view.log("Không tìm thấy chu trình/đường đi Euler.")
            messagebox.showinfo("Thông báo", "Không tồn tại đường đi Euler!")
            return

        # Điều kiện để in ra đúng thông báo
        if len(path) > 1 and path[0] == path[-1]:
            euler_type = "Chu trình Euler"
        else:
            euler_type = "Đường đi Euler"

        path_str = " -> ".join(map(str, path))
        self.app.view.log(f"{euler_type}: {path_str}")

        # Tạo danh sách cạnh để tô màu
        highlight_list = []
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            highlight_list.append((u, v))

        self.app.graph_ctrl.refresh_view(highlight_edges=highlight_list)

        # Pop-up thông báo
        messagebox.showinfo("Kết quả", f"{euler_type}:\n{path_str}")


    def handle_shortest_path(self, algo_type, start_node):
        start_node = start_node.strip().upper()
        if not start_node or start_node not in self.graph.nodes:
            messagebox.showwarning("Lỗi", "Đỉnh bắt đầu không hợp lệ!")
            return

        distances = {}
        previous = {}
        
        # 1. Chạy thuật toán để lấy dữ liệu
        if algo_type == "Dijkstra":
            distances, previous = PathFinding.dijkstra(self.graph, start_node)
        
        elif algo_type == "Bellman-Ford":
            result = PathFinding.bellman_ford(self.graph, start_node)
            if result is None:
                messagebox.showerror("Lỗi", "Đồ thị có chu trình âm, không thể dùng Bellman-Ford!")
                return
            # Chuẩn hóa dữ liệu từ Bellman-Ford cho giống Dijkstra
            distances = {n: val['distance'] for n, val in result.items()}
            previous = {n: val['previous'] for n, val in result.items()}

        # 2. Hiển thị kết quả ra Log & Thu thập cạnh để tô màu
        self.app.view.log(f"=== KẾT QUẢ {algo_type.upper()} TỪ ĐỈNH {start_node} ===")
        self.app.view.log(f"{'Đến':<5} | {'Khoảng cách để đi':<5} | {'Đường đi'}")
        self.app.view.log("-" * 40)

        spt_edges = [] # Danh sách các cạnh thuộc cây đường đi ngắn nhất (Shortest Path Tree)

        sorted_nodes = sorted(self.graph.nodes)
        for target in sorted_nodes:
            if target == start_node: 
                continue
            
            dist = distances.get(target, float('inf'))
            parent = previous.get(target)

            if dist != float('inf'):
                # Truy vết ngược từ đích về nguồn để ra đường đi
                path = []
                curr = target
                while curr is not None:
                    path.append(curr)
                    curr = previous.get(curr)
                path.reverse() # Đảo ngược lại: Start -> ... -> Target

                # In ra Log
                path_str = " -> ".join(path)
                self.app.view.log(f"{target:<5} | {dist:<17} | {path_str}")

                # Thêm cạnh (Parent -> Target) vào danh sách highlight
                if parent:
                    spt_edges.append((parent, target))
            else:
                self.app.view.log(f"{target:<5} | {'Inf':<17} | Không có đường đi")

        # 3. Vẽ lại đồ thị và highlight toàn bộ cây đường đi ngắn nhất
        self.app.graph_ctrl.refresh_view(highlight_edges=spt_edges)