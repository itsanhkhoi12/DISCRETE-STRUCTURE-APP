
from typing import List, Tuple
import heapq
# Thuật toán Prim


def prim(graph) -> Tuple[List[Tuple[str, str, float]], float]:
    if not graph.nodes:
        return [], 0.0

    start_vertex = min(iter(graph.nodes))

    visited = set()
    parent = {v: None for v in graph.nodes}
    key = {v: float('inf') for v in graph.nodes}
    key[start_vertex] = 0.0

    pq = [(0.0, start_vertex)]
    mst_edges = []
    total_weight = 0.0
    while pq:
        current_weight, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        if parent[u] is not None:
            mst_edges.append((parent[u], u, current_weight))
            total_weight += current_weight
        for v, weight in graph.adj_list[u].items():
            if v not in visited and weight < key[v]:
                key[v] = weight
                parent[v] = u
                heapq.heappush(pq, (weight, v))
    return mst_edges, total_weight
# Thuật toán kruskal


def kruskal(graph) -> Tuple[List[Tuple[str, str, float]], float]:
    if not graph.nodes:
        return [], 0.0
    edges = sorted(graph.get_edges(), key=lambda x: x[2])
    parent = {v: v for v in graph.nodes}
    rank = {v: 0 for v in graph.nodes}

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
    total_weight = 0.0
    for u, v, w in edges:
        if union(u, v):
            mst_edges.append((u, v, w))
            total_weight += w
            if len(mst_edges) == len(graph.nodes) - 1:
                break
    return mst_edges, total_weight
