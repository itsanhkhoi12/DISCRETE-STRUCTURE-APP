from models.graph import Graph
from algorithms.traversal import Traversal
class Euler():
    @staticmethod
    def fleury(graph:Graph, start = None):
        """
        Thực hiện thuật toán Fleury để tìm kiếm chu trình hoặc đường đi Euler
        Args:
            graph: Đồ thị cần tìm kiếm chu trình
            start: Đỉnh bắt đầu thực hiện để tìm kiếm chu trình
        Returns:
            path: Đường đi/Chu trình Euler
        """
        # Kiểm tra cạnh có phải cầu không
        def is_not_bridge(u, v) -> bool:
            '''
            Kiểm tra một cạnh (u,v) có phải là cạnh "cầu" (bridge) hay không            
            Args:
                u: Đỉnh u của cạnh cần xét
                v: Đinh v của cạnh cần xét
            Returns:
                True|False: True nếu hiện tại từ đỉnh u chỉ có một đỉnh có thể đi được, hoặc số lượng các đỉnh có thể đến được từ đỉnh u trước và sau khi xoá đỉnh v như nhau
            '''
            
            if len(graph.adj_list[u]) == 1:
                return True

            # Đếm các đỉnh co thể đến được đỉnh u
            path_before = Traversal.dfs_traversal(graph, u)
            count_1 = len(path_before)

            # Tạm xoá cạnh u, v 
            graph.remove_edge(u,v)
            
            # Đếm số đỉnh có thể đến được đỉnh u (sau khi xoá cạnh (u,v))
            path_after = Traversal.dfs_traversal(graph,u)
            count_2 = path_after

            # Thêm lại cạnh (u,v)
            graph.add_edge(u,v)

            return count_1 == count_2

        # kiểm tra điều kiện Euler
        def has_euler():
            odd = 0
            for u,v_set in graph.adj_list.items():
                if len(v_set) % 2 == 1:
                    odd += 1
            return odd == 0 or odd == 2

        # Tìm điểm bắt đầu (nếu không truyền start), ưu tiên đỉnh bắt đầu bằng bậc lẻ (Đường đi Euler).
        # Nếu không thấy thì mặc định là đỉnh đầu tiên của danh sách kề
        def find_start():
            for u,v_list in graph.adj_list.items():
                if len(v_list) % 2 == 1:
                    return u
            return list(graph.adj_list.keys())[0]

        # ---------- Logic xử lý thuật toán Fleury ----------
        # Xử lý start nếu người dùng không set đúng
        if start is None:
            start = find_start()

        # nếu không có đường đi Euler → dừng
        if not has_euler():
            return None

        # Fleury
        path = [start]
        u = start

        while True:
            if not graph.adj_list[u]:
                break

            for v in list(graph.adj_list[u]):
                if is_not_bridge(u, v):
                    graph.remove_edge(u,v)
                    path.append(v)
                    u = v
                    break
        return path
    
    @staticmethod
    def hierholzer(graph:Graph,start):
        #vì thuật toán sẽ xóa cạnh dần dần, cần copy để không mất dữ liệu gốc
        adj = {}
        degrees = {}
        adj_list = graph.adj_list
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