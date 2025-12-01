import math

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
