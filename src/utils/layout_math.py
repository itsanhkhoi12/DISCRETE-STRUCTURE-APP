import math, random

class LayoutMath:
    @staticmethod
    def calculate_circular_positions(nodes, canvas_width, canvas_height):
        n = len(nodes)
        if n == 0: return {}
        positions = {}
        radius = min(canvas_width, canvas_height) * 0.35
        center_x = canvas_width / 2
        center_y = canvas_height / 2
        
        sorted_nodes = sorted(list(nodes))
        for i, node in enumerate(sorted_nodes):
            angle = 2 * math.pi * i / n
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            positions[node] = (x, y)
        return positions


    @staticmethod
    def calculate_spring_positions(nodes, edges, width, height, iterations=50):
        """
        Thuật toán Force-Directed (Fruchterman-Reingold)
        Giúp đồ thị tự dàn trải ra, hạn chế cắt chéo cạnh.
        """
        node_list = list(nodes)
        n = len(node_list)
        if n == 0: return {}
        
        # 1. Khởi tạo vị trí ngẫu nhiên (gom vào giữa để tránh văng ra ngoài)
        area = width * height
        k = math.sqrt(area / n) * 0.75 # Hằng số lực lý tưởng
        
        pos = {node: (width/2 + random.uniform(-50, 50), 
                      height/2 + random.uniform(-50, 50)) for node in node_list}

        t = width / 10  # Nhiệt độ ban đầu
        dt = t / (iterations + 1)

        # 2. Chạy mô phỏng lực
        for _ in range(iterations):
            # Vector dịch chuyển
            disp = {node: [0, 0] for node in node_list}

            # A. Lực đẩy (Repulsive) giữa MỌI cặp đỉnh
            for i in range(n):
                v = node_list[i]
                for j in range(n):
                    if i == j: continue
                    u = node_list[j]
                    
                    dx = pos[v][0] - pos[u][0]
                    dy = pos[v][1] - pos[u][1]
                    dist = math.sqrt(dx*dx + dy*dy)
                    if dist < 0.01: dist = 0.01

                    # Công thức lực đẩy: f = k^2 / d
                    repulse = (k * k) / dist
                    disp[v][0] += (dx / dist) * repulse
                    disp[v][1] += (dy / dist) * repulse

            # B. Lực hút (Attractive) giữa các đỉnh CÓ CẠNH NỐI
            for u, v, w in edges:
                if u not in pos or v not in pos: continue
                if u == v: continue # Bỏ qua khuyên (self-loop) khi tính lực

                dx = pos[v][0] - pos[u][0]
                dy = pos[v][1] - pos[u][1]
                dist = math.sqrt(dx*dx + dy*dy)
                if dist < 0.01: dist = 0.01

                # Công thức lực hút: f = d^2 / k
                attract = (dist * dist) / k
                
                disp[u][0] += (dx / dist) * attract
                disp[u][1] += (dy / dist) * attract
                
                disp[v][0] -= (dx / dist) * attract
                disp[v][1] -= (dy / dist) * attract

            # C. Cập nhật vị trí & Giới hạn biên
            for node in node_list:
                d_len = math.sqrt(disp[node][0]**2 + disp[node][1]**2)
                if d_len > 0:
                    limited_dist = min(d_len, t)
                    pos[node] = (
                        pos[node][0] + (disp[node][0] / d_len) * limited_dist,
                        pos[node][1] + (disp[node][1] / d_len) * limited_dist
                    )
                
                # Giữ node nằm trong khung hình (padding 30px)
                x = min(width - 30, max(30, pos[node][0]))
                y = min(height - 30, max(30, pos[node][1]))
                pos[node] = (x, y)

            t -= dt # Giảm nhiệt độ

        return pos