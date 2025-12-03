from collections import deque

def check_bipartite(graph_adj):
    V = graph_adj.keys()
    # 0:Chưa tô màu; 1:Màu A (V1); 2:Màu B (V2)
    color = {node: 0 for node in V}

    #Bắt đầu duyệt qua tất cả các đỉnh để xử lý đồ thị không liên thông
    for start_node in V:
        if color[start_node] == 0:
            
            queue = deque([start_node])
            color[start_node] = 1 #Gán màu khởi đầu là Màu 1

            while queue:
                u = queue.popleft()
                current_color = color[u]
                next_color = 3 - current_color #Tìm màu đối lập (1 -> 2, 2 -> 1)

                for v in graph_adj.get(u, []):
                    
                    if color[v] == 0:
                        #Tô màu đối lập và thêm vào hàng đợi
                        color[v] = next_color
                        queue.append(v)
                            
                    elif color[v] == current_color:
                        #Phát hiện xung đột (Chu trình lẻ)
                        return False, {} # Trả về False và dữ liệu tô màu rỗng

    #Nếu hoàn tất mà không có xung đột, trả về True và bản đồ màu
    return True, color