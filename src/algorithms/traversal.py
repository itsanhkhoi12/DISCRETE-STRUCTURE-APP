from collections import deque

def bfs_traversal(graph_adj, start_node):
    if start_node not in graph_adj:
        return []
        
    visited = set()
    queue = deque([start_node])
    traversal_path = []

    while queue:
        u = queue.popleft()
        if u not in visited:
            visited.add(u)
            traversal_path.append(u)
            
            # Thêm tất cả các đỉnh kề chưa thăm vào hàng đợi
            for v in graph_adj.get(u, []):
                if v not in visited:
                    queue.append(v)

    return traversal_path

def dfs_traversal(graph, start_node):
    visited = set()
    components = []

    if start_node in graph:
        stack = [start_node]
        comp = []
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                comp.append(node)

                for neighbor in reversed(graph[node]):
                    if neighbor not in visited:
                        stack.append(neighbor)
        components.append(comp)

    for đỉnh_còn_lại in graph:
        if đỉnh_còn_lại not in visited:
            stack = [đỉnh_còn_lại]
            comp = []

            while stack:
                curr = stack.pop()
                if curr not in visited:
                    visited.add(curr)
                    comp.append(curr)

                    for node_kề in reversed(graph[curr]):
                        if node_kề not in visited:
                            stack.append(node_kề)

            components.append(comp)
    return components