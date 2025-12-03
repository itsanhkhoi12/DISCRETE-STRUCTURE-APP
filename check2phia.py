from collections import deque

def is_bipartite_bfs(graph_adj):
    V = graph_adj.keys()
    # 0:Chưa tô màu; 1:Màu A; 2:Màu B
    color = {node: 0 for node in V}

    for start_node in V:
        if color[start_node] == 0:
            
            queue = deque([start_node])
            color[start_node] = 1 # Bắt đầu với Màu 1

            while queue:
                u = queue.popleft()
                current_color = color[u]
                next_color = 3 - current_color # Tìm màu đối lập (1 -> 2, 2 -> 1)

                # Duyệt qua các đỉnh kề
                for v in graph_adj.get(u, []):
                    
                    if color[v] == 0:
                        # Tô màu đối lập và thêm vào hàng đợi
                        color[v] = next_color
                        queue.append(v)
                            
                    elif color[v] == current_color:
                        # Phát hiện xung đột: Hai đỉnh kề cùng màu
                        print(f"❌ Xung đột phát hiện: Đỉnh {u} và {v} cùng màu {current_color}.")
                        return False # KHÔNG phải đồ thị 2 phía

    # Nếu hoàn tất mà không có xung đột
    return True

# --- LOGIC NHẬP DỮ LIỆU TỪ TERMINAL (SỬA ĐỔI) ---

def input_graph_from_terminal():
    print("--- NHẬP ĐỒ THỊ VÔ HƯỚNG ---")
    
    try:
        # 1. Nhập tổng số đỉnh
        num_vertices = int(input("Nhập tổng số đỉnh (N): "))
        if num_vertices <= 0:
             print("Lỗi: Số đỉnh phải lớn hơn 0.")
             return {}
             
    except ValueError:
        print("Lỗi: Vui lòng nhập một số nguyên hợp lệ.")
        return {}

    # Khởi tạo danh sách kề với N đỉnh, được đánh số từ 1 đến N
    graph_adj = {i: [] for i in range(1, num_vertices + 1)}

    # 2. Nhập các cạnh
    print(f"\nĐồ thị có {num_vertices} đỉnh (1 đến {num_vertices}).")
    print("Nhập các cạnh dưới dạng 'u v'. Nhập 'done' để kết thúc.")
    
    while True:
        line = input(f"Nhập cạnh (hoặc 'done'): ").strip()
        if line.lower() == 'done':
            break
        
        try:
            u_str, v_str = line.split()
            u = int(u_str)
            v = int(v_str)

            # Kiểm tra tính hợp lệ của đỉnh (phải nằm trong phạm vi 1 đến N)
            if 1 <= u <= num_vertices and 1 <= v <= num_vertices and u != v:
                # Vì là đồ thị vô hướng, thêm cả hai chiều
                if v not in graph_adj[u]:
                    graph_adj[u].append(v)
                if u not in graph_adj[v]:
                    graph_adj[v].append(u)
            else:
                print(f"Cảnh báo: Đỉnh {u} hoặc {v} không nằm trong phạm vi [1, {num_vertices}] hoặc cạnh lặp/khuyên.")
        except ValueError:
            print("Lỗi định dạng: Vui lòng nhập hai số nguyên cách nhau bằng dấu cách.")
        except Exception as e:
            print(f"Lỗi không xác định khi nhập cạnh: {e}")

    return graph_adj


# --- PHẦN CHẠY CHÍNH CỦA CHƯƠNG TRÌNH ---
if __name__ == "__main__":
    # 1. Gọi hàm nhập dữ liệu
    my_graph = input_graph_from_terminal()
    
    if not my_graph:
        print("\nChương trình kết thúc.")
    else:
        # 2. In danh sách kề để xác nhận (Tùy chọn)
        print("\n--- DANH SÁCH KỀ ĐÃ NHẬP ---")
        for node, neighbors in my_graph.items():
            print(f"Đỉnh {node}: Kề với {neighbors}")

        # 3. Chạy thuật toán kiểm tra
        is_bipartite = is_bipartite_bfs(my_graph)
        
        # 4. Hiển thị kết quả
        print("\n--- KẾT QUẢ KIỂM TRA ĐỒ THỊ 2 PHÍA ---")
        if is_bipartite:
            print("✅ Đồ thị LÀ đồ thị 2 phía (Bipartite Graph).")
        else:
            print("❌ Đồ thị KHÔNG phải là đồ thị 2 phía (Chứa chu trình lẻ).")