from src.views.main_window import MainWindow
from src.controllers.graph_controller import GraphController
from src.utils.converters import GraphConverter
from src.views.components.converter_view import ConverterView
from src.controllers.file_controller import FileController
from src.algorithms.traversal import Traversal
from src.algorithms.properties import Bipartite


class AppController:
    def __init__(self, root):
        self.root = root
        self.graph_ctrl = GraphController(self)
        self.file_ctrl = FileController()
        self.view = MainWindow(root, self)

    def show_node_context_menu(self, event, node_id):
        self.graph_ctrl.show_node_context_menu(event, node_id)

    def show_edge_context_menu(self, event, u, v):
        self.graph_ctrl.show_edge_context_menu(event, u, v)

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

    def action_save(self):
        """
        Ủy quyền (Delegate) cho FileController xử lý việc lưu file.
        Lấy trạng thái đồ thị từ GraphController.
        """
        current_graph = self.graph_ctrl.graph
        is_directed = self.graph_ctrl.directed
        # Giả sử GraphController có thuộc tính này
        is_weighted = self.graph_ctrl.weighted

        self.file_ctrl.handle_save_graph(
            graph=current_graph,
            directed=is_directed,
            weighted=is_weighted
        )

    def action_load(self):
        """
        Gọi FileController để tải dữ liệu, sau đó cập nhật GraphController và View.
        """
        load_result = self.file_ctrl.handle_load_graph()
        if load_result:
            self.graph_ctrl.set_new_graph(
                graph=load_result['graph'],
                directed=load_result['directed'],
                weighted=load_result['weighted']
            )
            self.view.control_panel.var_directed.set(load_result['directed'])

    def run_basic_algo(self, algo_type):
        self.view.log(f"--- Đang thực hiện: {algo_type} ---")
        if algo_type == "BIPARTITE":
            self.graph_ctrl.handle_check_bipartite()
        elif algo_type == "DFS":
            start_node = self.view.control_panel.ent_start_node.get()
            self.graph_ctrl.handle_traversal(algo_type, start_node)
        elif algo_type == "BFS":
            start_node = self.view.control_panel.ent_start_node.get()
            self.graph_ctrl.handle_traversal(algo_type, start_node)

    def run_advanced_algo(self):
        pass
