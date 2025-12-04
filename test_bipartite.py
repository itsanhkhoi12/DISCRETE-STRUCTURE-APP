# File: test_bipartite.py (Đặt trong thư mục gốc DISCRETE-STRUCTURE-APP/)

from src.algorithms.properties import check_bipartite
import sys
import os

# Tính toán đường dẫn tuyệt đối của thư mục 'src' và thêm nó vào sys.path
current_file_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_file_dir, 'src'))


def run_bipartite_test():
    """Chạy trường hợp kiểm tra đồ thị KHÔNG phải 2 phía."""

    # ----------------------------------------------------
    # ĐỒ THỊ VÍ DỤ: KHÔNG PHẢI ĐỒ THỊ 2 PHÍA (Chứa chu trình lẻ 2-3-4)
    # ----------------------------------------------------
    graph_fail = {
        1: [2, 5],
        2: [1, 3, 4],
        3: [2, 4],
        4: [2, 3],
        5: [1]
    }

    print("--- KIỂM TRA Đồ thị KHÔNG PHẢI 2 PHÍA ---")
    is_fail, coloring_fail = check_bipartite(graph_fail)

    if not is_fail:
        print("✅ Thành công. Đồ thị KHÔNG phải là 2 phía (Do phát hiện xung đột).")
    else:
        # Trường hợp này sẽ không xảy ra nếu code chạy đúng,
        # nhưng đây là logic xử lý nếu có lỗi
        v1 = [n for n, c in coloring_fail.items() if c == 1]
        v2 = [n for n, c in coloring_fail.items() if c == 2]
        print("❌ Thất bại. Lẽ ra không phải 2 phía nhưng lại được phân hoạch:")
        print(f"   Phân hoạch (V1/Màu 1): {v1}")
        print(f"   Phân hoạch (V2/Màu 2): {v2}")


if __name__ == "__main__":
    run_bipartite_test()
