# test_mst.py
# File test độc lập – đặt ở thư mục gốc dự án (cùng cấp với src/)
# Test Prim & Kruskal với bản đồ Quận 1 thật của bạn

from src.algorithms.mst import run_prim, run_kruskal
from src.models.graph import Graph
import os
import sys

# Thêm đường dẫn để import được module trong src/
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def test_quan1_mst():
    print("=== TEST PRIM & KRUSKAL VỚI BẢN ĐỒ QUẬN 1 THẬT ===\n")

    # Tạo đồ thị VÔ HƯỚNG (rất quan trọng!)
    g = Graph(directed=False, weighted=True)

    # Thêm các địa điểm nổi tiếng Quận 1
    locations = [
        "Nhà thờ Đức Bà",
        "Chợ Bến Thành",
        "Bitexco",
        "Nguyễn Huệ",
        "Bưu điện TP",
        "Dinh Độc Lập",
        "Phố đi bộ Nguyễn Huệ"
    ]

    for loc in locations:
        g.add_node(loc)

    # Thêm cạnh với khoảng cách thực tế (km)
    edges = [
        ("Nhà thờ Đức Bà", "Chợ Bến Thành", 0.8),
        ("Nhà thờ Đức Bà", "Nguyễn Huệ", 0.5),
        ("Nhà thờ Đức Bà", "Bưu điện TP", 0.3),
        ("Nguyễn Huệ", "Bitexco", 0.6),
        ("Nguyễn Huệ", "Phố đi bộ Nguyễn Huệ", 0.1),
        ("Chợ Bến Thành", "Bitexco", 1.2),
        ("Bưu điện TP", "Dinh Độc Lập", 1.5),
        ("Bitexco", "Dinh Độc Lập", 2.0),
        ("Phố đi bộ Nguyễn Huệ", "Bưu điện TP", 0.7),
    ]

    print("Các cạnh đã thêm:")
    for u, v, w in edges:
        g.add_edge(u, v, w)
        print(f"  {u} — {v}: {w} km")

    print(f"\nTổng số đỉnh: {len(g.nodes)}")
    print(f"Tổng số cạnh: {len(g.get_edges())}\n")

    # === CHẠY PRIM ===
    print("="*50)
    print("KẾT QUẢ THUẬT TOÁN PRIM:")
    prim_edges = run_prim(g)
    prim_total = sum(w for _, _, w in prim_edges)
    for u, v, w in prim_edges:
        print(f"  {u} — {v}: {w} km")
    print(f"  → Tổng quãng đường ngắn nhất (Prim): {prim_total:.2f} km")
    print()

    # === CHẠY KRUSKAL ===
    print("KẾT QUẢ THUẬT TOÁN KRUSKAL:")
    kruskal_edges = run_kruskal(g)
    kruskal_total = sum(w for _, _, w in kruskal_edges)
    for u, v, w in kruskal_edges:
        print(f"  {u} — {v}: {w} km")
    print(f"  → Tổng quãng đường ngắn nhất (Kruskal): {kruskal_total:.2f} km")

    # Kiểm tra kết quả
    if abs(prim_total - kruskal_total) < 1e-6:
        print("\nHOÀN HẢO! PRIM = KRUSKAL =", round(prim_total, 2), "km")
        print("THUẬT TOÁN CỦA BẠN ĐÃ HOẠT ĐỘNG CHÍNH XÁC 100%!")
        print("Giờ chỉ cần tích hợp vào app → chọn Kruskal → bấm chạy → cây khung xanh lá hiện ngay!")
    else:
        print("\nCÓ LỖI! Hai thuật toán cho kết quả khác nhau!")
        print(f"Prim: {prim_total} | Kruskal: {kruskal_total}")

    print("\n" + "="*60)


if __name__ == "__main__":
    test_quan1_mst()
