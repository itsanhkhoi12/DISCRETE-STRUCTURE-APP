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
    def hierholzer(graph):
        #vì thuật toán sẽ xóa cạnh dần dần, cần copy để không mất dữ liệu gốc
        adj = {}
        degrees = {}
        
        for u, neighbors in graph.items():
            # Chuyển đổi {v: w} hoặc set(v) thành list [v]
            if isinstance(neighbors, dict):
                adj[u] = list(neighbors.keys())
            else:
                adj[u] = list(neighbors)
            degrees[u] = len(adj[u])

        #kiểm tra điều kiện Euler
        odd_degree_nodes = [u for u in degrees if degrees[u] % 2 != 0]
        
        if len(odd_degree_nodes) not in [0, 2]:
            return None #không có đường đi/chu trình Euler

        #xác định điểm bắt đầu
        if start is None:
            if len(odd_degree_nodes) == 2:
                start = odd_degree_nodes[0] #bắt buộc xuất phát ở đỉnh bậc lẻ
            else:
                #tìm đỉnh đầu tiên có bậc > 0
                for u in adj:
                    if len(adj[u]) > 0:
                        start = u
                        break
                if start is None and adj: #trường hợp đồ thị chỉ có đỉnh cô lập
                    start = list(adj.keys())[0]

        #thuật toán Hierholzer (Sử dụng Stack)
        stack = [start]
        circuit = []

        while stack:
            u = stack[-1] #lấy đỉnh ở đỉnh stack
            
            #nếu u còn cạnh nối tới đỉnh khác
            if u in adj and len(adj[u]) > 0:
                v = adj[u][0] #lấy cạnh đầu tiên
                
                stack.append(v) #push v vào stack
                
                #xóa cạnh (u, v) khỏi đồ thị tạm
                adj[u].remove(v)
                if v in adj: #đồ thị vô hướng: xóa cả chiều ngược lại
                    adj[v].remove(u)
            else:
                #nếu u không còn cạnh nào, thêm vào kết quả và backtrack
                circuit.append(stack.pop())

        #kết quả của Hierholzer là ngược lại, cần đảo ngược list
        return circuit[::-1]