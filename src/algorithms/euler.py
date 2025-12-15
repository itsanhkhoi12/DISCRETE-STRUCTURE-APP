from models.graph import Graph
from algorithms.traversal import Traversal
import copy

class Euler:
    @staticmethod
    def fleury(graph: Graph, start=None):
        """
        Thực hiện thuật toán Fleury để tìm kiếm chu trình hoặc đường đi Euler
        Args:
            graph: Đồ thị cần tìm kiếm chu trình
            start: Đỉnh bắt đầu thực hiện để tìm kiếm chu trình
        Returns:
            path: Đường đi/ Chu trình Euler
        """
        g = copy.deepcopy(graph)

        def is_not_bridge(u, v) -> bool:
            if len(g.adj_list[u]) == 1:
                return True

            path_before = Traversal.dfs_traversal(g, u)
            count_1 = len(path_before)

            w = g.adj_list[u].get(v, 1.0)
            g.remove_edge(u, v)

            path_after = Traversal.dfs_traversal(g, u)
            count_2 = len(path_after)

            g.add_edge(u, v, w)

            return count_1 == count_2

        def has_euler():
            odd = 0
            for u in g.adj_list:
                if len(g.adj_list[u]) % 2 != 0:
                    odd += 1
            return odd == 0 or odd == 2

        def find_start():
            for u in g.adj_list:
                if len(g.adj_list[u]) % 2 != 0:
                    return u
            for u in g.adj_list:
                if len(g.adj_list[u]) > 0:
                    return u
            return None

        if not has_euler():
            return None

        if start is None:
            start = find_start()
        
        if start is None or start not in g.nodes:
            return None

        path = [start]
        u = start

        while True:
            if not g.adj_list.get(u):
                break

            neighbors = list(g.adj_list[u].keys())
            found_edge = False

            for v in neighbors:
                if is_not_bridge(u, v):
                    path.append(v)
                    g.remove_edge(u, v)
                    u = v
                    found_edge = True
                    break
            
            if not found_edge:
                if neighbors:
                    v = neighbors[0]
                    path.append(v)
                    g.remove_edge(u, v)
                    u = v
                else:
                    break

        return path

    @staticmethod
    def hierholzer(graph: Graph, start=None):
        adj = {}
        degrees = {}
        
        for u, neighbors in graph.adj_list.items():
            adj[u] = list(neighbors.keys())
            degrees[u] = len(adj[u])
        
        odd_nodes = [u for u, deg in degrees.items() if deg % 2 != 0]
        if len(odd_nodes) not in [0, 2]:
            return None

        if start is None:
            if len(odd_nodes) == 2:
                start = odd_nodes[0]
            else:
                for u in adj:
                    if len(adj[u]) > 0:
                        start = u
                        break
        
        if start is None or start not in adj:
            return None

        stack = [start]
        path = []

        while stack:
            u = stack[-1]
            if u in adj and adj[u]:
                v = adj[u].pop(0) 
                
                if not graph.directed:
                    if v in adj and u in adj[v]:
                        adj[v].remove(u)
                
                stack.append(v)
            else:
                path.append(stack.pop())

        return path[::-1]