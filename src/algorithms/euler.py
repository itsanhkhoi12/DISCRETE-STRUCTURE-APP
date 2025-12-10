from src.models.graph import Graph
import copy


class Euler():
    @staticmethod
    def fleury(graph: Graph):
        adj_copy = copy.deepcopy(graph.adj_list)
        # Chọn đỉnh bắt đầu
        start_node = None
        for node in graph.nodes:
            if len(adj_copy.get(node, {})) % 2 == 0:
                start_node = node
            break
        if start_node is None and graph.nodes:
            start_node = next(iter(graph.nodes))
        if start_node is None:
            return None
        # Chạy bắt đầu từ start_node
        path = []
        path.append(start_node)
        current = start_node
        # Lặp đến hết cạnh từ đỉnh hiện tại. Nếu đỉnh không có cạnh nào thì dừng.
        while True:
            current_neightbors = adj_copy.get(current, {})
            # Kiểm tra không có cạnh nào thì dừng
            if len(current_neightbors) == 0:
                break
            next_node = next(iter(current_neightbors))
            del adj_copy[current][next_node]
            if next_node in adj_copy and current in adj_copy[next_node]:
                del adj_copy[next_node][current]
            # Đi sang đỉnhh tiếp theo
            path.append(next_node)
            current = next_node
        # Kiểm tra đã chạy qua hết cạnh chưa
        total_edges_in_graph = len(graph.get_edges())
        if len(path) == total_edges_in_graph+1:
            return path
        else:
            return None

    @staticmethod
    def hierholzer(graph: Graph):
        """
        Cách hoạt động: đi lòng vòng, khi không đi được nữa thì quay lại
        Trả về:
            - Danh sách các đỉnh theo thứ tự đi qua (ví dụ: [0 -> 1 -> 2 -> 0)
            - Nếu không tìm được chu trình hoàn chỉnh thì trả về None
        """
        adj_copy = copy.deepcopy(graph.adj_list)
        start_node = None
        for node in graph.nodes:
            if len(adj_copy.get(node, {})) % 2 == 1:
                start_node = node
                break
        if start_node is None and graph.nodes:
            start_node = next(iter(graph.nodes))
        # Kiểm tra đồ thị có rỗng không
        if start_node is None:
            return None
        stack = []  # Để lưu trữ đường đi
        stack.append(start_node)
        euler_path = []  # Lưu ds kết quả
        while len(stack) > 0:
            current = stack[-1]
            if current in adj_copy and len(adj_copy[current]) > 0:
                next_node = next(iter(adj_copy[current]))
                stack.append(next_node)
                # Xóa cạnh đồ thị vừa đi
                del adj_copy[current][next_node]
                if next_node in adj_copy and current in adj_copy[next_node]:
                    del adj_copy[next_node][current]
            else:
                # Không còn đường đi thì lấy ra stack và thêm vào ds kết quả
                finished_node = stack.pop()
                euler_path.append(finished_node)
        euler_path.reverse()
        # Kiểm tra đã đi qua hết cạnh trong đồ thị chưa.
        total_edges_in_graph = len(graph.get_edges())
        if len(euler_path) == total_edges_in_graph+1:
            return euler_path
        else:
            return None
