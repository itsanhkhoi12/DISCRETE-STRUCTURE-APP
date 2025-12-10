from models.graph import Graph

class Euler():
    @staticmethod
    def fleury(graph:Graph, start):
        edges = graph.get_edges()

        # kiểm tra cạnh có phải cầu không
        def is_not_bridge(u, v):
            while len(u) == 1:
                
        # kiểm tra điều kiện Euler
        def has_euler():
            odd = 0
            for u in graph:
                if len(graph[u]) % 2 == 1:
                    odd += 1
            return odd == 0 or odd == 2

        # tìm điểm bắt đầu (nếu không truyền start)
        def find_start():
            for u in graph:
                if len(graph[u]) % 2 == 1:
                    return u
            return list(graph.keys())[0]

        # xử lý start nếu người dùng không set đúng
        if start is None:
            start = find_start()

        # nếu không có đường đi Euler → dừng
        if not has_euler():
            return None

        # Fleury
        path = [start]
        u = start

        while True:
            if not graph[u]:
                break

            for v in list(graph[u]):
                if is_not_bridge(u, v):
                    graph[u].remove(v)
                    graph[v].remove(u)
                    path.append(v)
                    u = v
                    break

        return path

    @staticmethod
    def hierholzer():
        pass