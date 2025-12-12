from views.main_window import MainWindow
from controllers.graph_controller import GraphController
from controllers.algorithm_controller import AlgorithmController # Import mới
from controllers.file_controller import FileController
from utils.converters import GraphConverter
from views.components.converter_view import ConverterView

class AppController:
    def __init__(self, root):
        self.root = root
        self.graph_ctrl = GraphController(self)
        self.algo_ctrl = AlgorithmController(self) 
        self.file_ctrl = FileController()
        self.view = MainWindow(root, self)

    def show_node_context_menu(self, event, node_id):
        self.graph_ctrl.show_node_context_menu(event, node_id)

    def show_edge_context_menu(self, event, u, v):
        self.graph_ctrl.show_edge_context_menu(event, u, v)

    def action_add_edge(self):
        self.graph_ctrl.handle_add_edge(self.view.control_panel.ent_u.get(), 
                                        self.view.control_panel.ent_v.get(), 
                                        self.view.control_panel.ent_w.get())
        # Clear input
        self.view.control_panel.ent_u.delete(0, 'end')
        self.view.control_panel.ent_v.delete(0, 'end')

    def toggle_mode(self):
        self.graph_ctrl.handle_toggle_mode(self.view.control_panel.var_directed.get())

    def action_save(self):
        self.file_ctrl.handle_save_graph(self.graph_ctrl.graph, self.graph_ctrl.directed, self.graph_ctrl.weighted)

    def action_load(self):
        self.view.clear_log()
        res = self.file_ctrl.handle_load_graph()
        if res:
            self.graph_ctrl.set_new_graph(res['graph'], res['directed'], res['weighted'])
            self.view.control_panel.var_directed.set(res['directed'])

    def action_convert_view(self):
        g = self.graph_ctrl.graph
        ConverterView(self.view.root, 
                      GraphConverter.to_matrix_string(g), 
                      GraphConverter.to_adj_list_string(g), 
                      GraphConverter.to_edge_list_string(g))

    def run_shortest_path(self, algo_type):
        self.view.clear_log()
        start_node = self.view.control_panel.ent_start_node.get()
        self.algo_ctrl.handle_shortest_path(algo_type, start_node)

    def run_basic_algo(self, algo_type):
        self.view.clear_log()
        self.view.log(f"--- Yêu cầu: {algo_type} ---")
        if algo_type == "BIPARTITE":
            self.algo_ctrl.handle_check_bipartite()
        elif algo_type == "DFS":
            self.algo_ctrl.handle_dfs(self.view.control_panel.ent_start_node.get())
        elif algo_type == "BFS":
            self.algo_ctrl.handle_bfs(self.view.control_panel.ent_start_node.get())

    def run_advanced_algo(self):
        self.view.clear_log()
        algo = self.view.control_panel.combo_algo.get()
        start = self.view.control_panel.ent_start_node.get()
        end = self.view.control_panel.ent_end_node.get() 
        
        self.algo_ctrl.handle_advanced_algo(algo, start, end)