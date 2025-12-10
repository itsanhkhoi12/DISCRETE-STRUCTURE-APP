from models.graph import Graph

class Euler():
    @staticmethod
    def fleury(graph, start):
    # dfs
        def dfs(u, visited):
            visited.add(u)
            for v in graph[u]:
                if v not in visited:
                    dfs(v, visited)

        # kiểm tra cạnh có phải cầu không
        def is_not_bridge(u, v):
            if len(graph[u]) == 1:
                return True

            visited = set()
            dfs(u, visited)
            count1 = len(visited)

            graph[u].remove(v)
            graph[v].remove(u)

            visited = set()
            dfs(u, visited)
            count2 = len(visited)

            graph[u].append(v)
            graph[v].append(u)

            return count1 == count2

        # kiểm tra điều kiện Euler
        def has_euler():
            odd = 0
            for u in graph:
                if len(graph[u]) % 2 == 1:
                    odd += 1
            return odd == 0 or odd == 2

        # tìm điểm bắt đầu (nếu không truyền start), trường hợp là đường đi Euler thì sẽ bắt đầu tại đỉnh lẻ
        def find_start():
            for u in graph:
                if len(graph[u]) % 2 == 1:
                    return u
            return list(graph.keys())[0]

        # xử lý start nếu không set đúng
        if start is None:
            start = find_start()

        # nếu không có đường đi Euler thì dừng
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