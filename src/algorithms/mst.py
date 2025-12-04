# src/algorithms/mst.py
# Thuật toán Prim & Kruskal
import heapq
from typing import List, Tuple, Any


def run_prim(graph) -> List[Tuple[Any, Any, float]]:
    # Thuật toán Prim – tìm MST cho đồ thị vô hưóng
    if not graph.nodes:
        return []

    # Chọn đỉnh bắt đầu (lấy đỉnh đầu tiên trong set)
    start_node = next(iter(graph.nodes))
    visited = set()
    min_heap = []
    mst_edges = []
    # Bắt đầu từ đỉnh start_node
    heapq.heappush(min_heap, (0, start_node, None))
    while min_heap:
        weight, current, parent = heapq.heappop(min_heap)
        if current in visited:
            continue
        visited.add(current)
        # Nếu không phải đỉnh gốc → thêm cạnh vào MST
        if parent is not None:
            mst_edges.append((parent, current, weight))
        # Duyệt tất cả đỉnh kề từ adj_list[current]
        for neighbor, edge_weight in graph.adj_list[current].items():
            if neighbor not in visited:
                heapq.heappush(min_heap, (edge_weight, neighbor, current))
    return mst_edges


def run_kruskal(graph) -> List[Tuple[Any, Any, float]]:
    if not graph.nodes:
        return []
    # Lấy danh sách cạnh và sắp xếp theo trọng số tăng dần
    edges = sorted(graph.get_edges(), key=lambda e: e[2])
    parent = {node: node for node in graph.nodes}
    rank = {node: 0 for node in graph.nodes}

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        px, py = find(x), find(y)
        if px == py:
            return False
        if rank[px] < rank[py]:
            parent[px] = py
        elif rank[px] > rank[py]:
            parent[py] = px
        else:
            parent[py] = px
            rank[px] += 1
        return True
    mst_edges = []
    for u, v, w in edges:
        if union(u, v):
            mst_edges.append((u, v, w))
            if len(mst_edges) == len(graph.nodes) - 1:
                break
    return mst_edges
