# # src/controllers/algorithm_controller.py
# # Controller thật – gọi Prim và Kruskal và trả kết quả về View để vẽ

# from src.algorithms.mst import run_prim, run_kruskal


# class AlgorithmController:
#     def __init__(self, graph, view):
#         self.graph = graph      # đối tượng Graph thật
#         self.view = view        # MainWindow để gọi hàm vẽ

#     def run_prim(self):
#         print("Đang chạy thuật toán Prim")
#         mst_edges = run_prim(self.graph)  # trả về danh sách cạnh MST
#         self.view.highlight_mst(mst_edges, color="green")
#         self.view.log("Prim hoàn thành! Đã tô cây khung màu XANH LÁ")

#     def run_kruskal(self):
#         print("Đang chạy thuật toán Kruskal")
#         mst_edges = run_kruskal(self.graph)
#         self.view.highlight_mst(mst_edges, color="#00ff00")
#         self.view.log("Kruskal hoàn thành! Đã tô cây khung màu XANH LÁ")
