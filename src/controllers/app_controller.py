# from views.main_window import MainWindow
# from controllers.graph_controller import GraphController
# from utils.converters import GraphConverter
# from views.components.converter_view import ConverterView
# from controllers.file_controller import FileController

# class AppController:
#     def __init__(self, root):
#         self.root = root
#         self.graph_ctrl = GraphController(self)
#         self.file_ctrl = FileController()
#         self.view = MainWindow(root, self)

    
#     def action_add_edge(self):
#         # Lấy dữ liệu từ View input
#         u = self.view.control_panel.ent_u.get()
#         v = self.view.control_panel.ent_v.get()
#         w = self.view.control_panel.ent_w.get()
        
#         # Chuyển việc cho GraphController xử lý
#         self.graph_ctrl.handle_add_edge(u, v, w)
        
#         self.view.control_panel.ent_u.delete(0, 'end')
#         self.view.control_panel.ent_v.delete(0, 'end')

#     def toggle_mode(self):
#         # Lấy giá trị checkbox từ View
#         is_directed = self.view.control_panel.var_directed.get()
#         self.graph_ctrl.handle_toggle_mode(is_directed)

#     def action_convert_view(self):
#         """Hàm này được gọi khi bấm nút 'Xem Ma trận/DS Kề'"""
        
#         current_graph = self.graph_ctrl.graph
        
#         str_matrix = GraphConverter.to_matrix_string(current_graph)
#         str_adj = GraphConverter.to_adj_list_string(current_graph)
#         str_edges = GraphConverter.to_edge_list_string(current_graph)

#         ConverterView(self.view.root, str_matrix, str_adj, str_edges)

#     def action_save(self):
#         """
#         Ủy quyền (Delegate) cho FileController xử lý việc lưu file.
#         Lấy trạng thái đồ thị từ GraphController.
#         """
#         current_graph = self.graph_ctrl.graph
#         is_directed = self.graph_ctrl.directed
#         is_weighted = self.graph_ctrl.weighted # Giả sử GraphController có thuộc tính này

#         self.file_ctrl.handle_save_graph(
#             graph=current_graph,
#             directed=is_directed,
#             weighted=is_weighted
#         )

#     def action_load(self):
#         """
#         Gọi FileController để tải dữ liệu, sau đó cập nhật GraphController và View.
#         """
#         load_result = self.file_ctrl.handle_load_graph()
        
#         if load_result:
#             # 1. Cập nhật trạng thái trong GraphController (Model/Logic)
#             self.graph_ctrl.set_new_graph(
#                 graph=load_result['graph'],
#                 directed=load_result['directed'],
#                 weighted=load_result['weighted']
#             )
            
#             # 2. Cập nhật View (Giao diện người dùng)
#             self.view.control_panel.var_directed.set(load_result['directed'])
#             self.view.control_panel.var_weighted.set(load_result['weighted'])
            
#             # 3. Yêu cầu View vẽ lại và cập nhật thông tin (Nếu có hàm tương tự)
#             # Giả sử View có hàm update_display()
#             # self.view.update_display()
            
#             # Nếu bạn đang sử dụng logic update trong GraphController
#             # (như handle_toggle_mode), có thể gọi nó thay vì cập nhật trực tiếp View
            
#             # Tạm thời gọi lại hàm vẽ và cập nhật info từ View (cần được bạn tự định nghĩa)
#             # self.view.refresh_all() 
#             pass # Tùy thuộc vào cách bạn thiết kế hàm refresh của View

#     def run_basic_algo(self, algo_type):
#         pass

#     def run_advanced_algo(self):
#         pass


from src.views.main_window import MainWindow
from src.controllers.graph_controller import GraphController
from src.utils.converters import GraphConverter
from src.views.dialogs.converter_view import ConverterView
from src.algorithms.mst import run_prim, run_kruskal


class AppController:
    def __init__(self, root):
        self.root = root
        self.graph_ctrl = GraphController(self)
        self.view = MainWindow(root, self)

    def action_add_edge(self):
        # Lấy dữ liệu từ View input
        u = self.view.control_panel.ent_u.get()
        v = self.view.control_panel.ent_v.get()
        w = self.view.control_panel.ent_w.get()

        # Chuyển việc cho GraphController xử lý
        self.graph_ctrl.handle_add_edge(u, v, w)

        self.view.control_panel.ent_u.delete(0, 'end')
        self.view.control_panel.ent_v.delete(0, 'end')

    def toggle_mode(self):
        # Lấy giá trị checkbox từ View
        is_directed = self.view.control_panel.var_directed.get()
        self.graph_ctrl.handle_toggle_mode(is_directed)

    def action_convert_view(self):
        """Hàm này được gọi khi bấm nút 'Xem Ma trận/DS Kề'"""

        current_graph = self.graph_ctrl.graph

        str_matrix = GraphConverter.to_matrix_string(current_graph)
        str_adj = GraphConverter.to_adj_list_string(current_graph)
        str_edges = GraphConverter.to_edge_list_string(current_graph)

        ConverterView(self.view.root, str_matrix, str_adj, str_edges)

    def action_load(self):
        pass

    def action_save(self):
        pass

    def run_basic_algo(self, algo_type):
        pass

    def run_advanced_algo(self):
        algo = self.view.control_panel.combo_algo.get()  # lấy từ combobox
        graph = self.graph_ctrl.graph
        edges = graph.get_edges() if hasattr(graph, "edges") else graph.get_edges()
        if algo == "Prim":
            self.view.control_panel.append_log("Thuật toán Prim đang chạy")
            mst_edges = run_prim(graph)
            # vẽ đồ thị
            self.view.canvas_view.draw_graph(
                graph.nodes,
                edges, graph.directed
            )
            # Highlight MST
            self.view.canvas_view.highlight_edges(mst_edges, color="#32CD32")
            self.view.control_panel.append_log(
                f"Prim đã hoàn thành. Đã tô màu {len(mst_edges)} cạnh cây khung màu xanh lá")
        elif algo == "Kruskal":
            self.view.control_panel.append_log("Thuật toán Kruskal đang chạy")
            mst_edges = run_kruskal(graph)
            self.view.canvas_view.draw_graph(
                graph.nodes,
                edges, graph.directed
            )
            self.view.canvas_view.highlight_edges(mst_edges, color="#00FF00")
            self.view.control_panel.append_log(
                f"Kruskal đã hoàn thành. Đã tô màu {len(mst_edges)} cạnh cây khung có màu xanh")
        else:
            self.view.control_panel.append_log(
                f"Chưa hỗ trợ thuật toán: {algo}")
