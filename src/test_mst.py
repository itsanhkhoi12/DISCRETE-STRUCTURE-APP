# src/test_mst.py – ĐÃ SỬA ĐÚNG VỚI CODE CỦA BẠN
from src.models.graph import Graph
from src.algorithms.mst import run_prim, run_kruskal

g = Graph(directed=False)  # bạn đang dùng directed=False, không có weighted

# SỬA TỪ add_vertex → add_node
g.add_node("Nhà thờ Đức Bà")
g.add_node("Chợ Bến Thành")
g.add_node("Bitexco")
g.add_node("Nguyễn Huệ")

# add_edge thì giữ nguyên
g.add_edge("Nhà thờ Đức Bà", "Chợ Bến Thành", 0.8)
g.add_edge("Nhà thờ Đức Bà", "Nguyễn Huệ", 0.5)
g.add_edge("Nguyễn Huệ", "Bitexco", 0.6)
g.add_edge("Chợ Bến Thành", "Bitexco", 1.2)

print(g)
print("\n--- PRIM ---")
run_prim(g)
print("\n--- KRUSKAL ---")
run_kruskal(g)
