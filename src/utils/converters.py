class GraphConverter:
    @staticmethod
    def to_matrix_string(graph):
        """Chuyển Graph thành chuỗi Ma trận kề để hiển thị"""
        matrix, sorted_nodes = graph.get_adjacency_matrix()
        
        header = "     " + "   ".join([f"{n:>3}" for n in sorted_nodes]) + "\n"
        separator = "    " + "-" * (len(header) - 4) + "\n"
        
        body = ""
        for i, row in enumerate(matrix):
            row_str = "   ".join([f"{int(x):>3}" if x != 0 else "  ." for x in row])
            body += f"{sorted_nodes[i]:<3} | {row_str}\n"
            
        return header + separator + body

    @staticmethod
    def to_adj_list_string(graph):
        """Chuyển Graph thành chuỗi Danh sách kề"""
        res = ""
        sorted_nodes = sorted(list(graph.nodes))
        
        for u in sorted_nodes:
            neighbors = []
            if u in graph.adj_list:
                for v, w in sorted(graph.adj_list[u].items()):
                    w_str = f"({int(w)})" if w % 1 == 0 else f"({w})"
                    neighbors.append(f"{v}{w_str}")
            
            line = ", ".join(neighbors) if neighbors else "(Cô lập)"
            res += f"{u} -> {line}\n"
            
        return res

    @staticmethod
    def to_edge_list_string(graph):
        """Chuyển Graph thành danh sách cạnh"""
        edges = graph.get_edges()
        edges.sort(key=lambda x: (x[0], x[1]))
        
        res = f"{'Nguồn':<8} {'Đích':<8} {'Trọng số':<8}\n"
        res += "-"*30 + "\n"
        
        for u, v, w in edges:
            res += f"{u:<8} {v:<8} {w}\n"
        return res