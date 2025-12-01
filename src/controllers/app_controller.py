from views.main_window import MainWindow
from controllers.graph_controller import GraphController
from utils.converters import GraphConverter
from views.components.converter_view import ConverterView

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
        pass