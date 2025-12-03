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
