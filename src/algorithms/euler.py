from models.graph import Graph

class Euler():
    @staticmethod
    def fleury(graph:Graph, start):
        pass

    @staticmethod
    def hierholzer(graph:Graph,start):
        #vì thuật toán sẽ xóa cạnh dần dần, cần copy để không mất dữ liệu gốc
        adj = {}
        degrees = {}
        adj_list = graph.adj_list()
        for u, neighbors in adj_list.items():
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