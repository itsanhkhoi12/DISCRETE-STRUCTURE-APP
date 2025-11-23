# BÀI TẬP LỚN CẤU TRÚC RỜI RẠC
## Cấu trúc các folder và file của bài tập lớn như sau
``` text
src/
│
├── main.py                   <-- Dùng để chạy app chính
|
├── models/                   <-- DỮ LIỆU
│   ├── __init__.py
│   └── graph.py              # Class Graph (V, E)
│
├── views/                    <-- GIAO DIỆN 
│   ├── __init__.py
│   ├── main_window.py        # Cửa sổ chính
│   ├── components/           # (Tách nhỏ view ra nữa cho gọn)
│   │   ├── control_panel.py  # Panel nút bấm bên trái
│   │   └── canvas_view.py    # Canvas vẽ bên phải
│   └── dialogs/              # Các cửa sổ phụ
│       └── converter_view.py # Cửa sổ xem Ma trận/DS kề
│
├── controllers/              <-- ĐIỀU PHỐI
│   ├── __init__.py
│   ├── app_controller.py     # Controller tổng (Quản lý các controller con)
│   ├── graph_controller.py   # Xử lý thêm/sửa/xóa đỉnh, cạnh
│   ├── algorithm_controller.py # Xử lý việc gọi thuật toán (BFS, Dijkstra...)
│   └── file_controller.py    # Xử lý nút Lưu/Mở file
│
├── algorithms/               <-- CHỨA THUẬT TOÁN 
│   ├── __init__.py
│   ├── traversal.py          # BFS, DFS
│   ├── pathfinding.py        # Dijkstra (Tìm đường đi)
│   ├── mst.py                # Prim, Kruskal (Cây khung)
│   ├── flow.py               # Ford-Fulkerson (Luồng cực đại)
│   ├── euler.py              # Fleury, Hierholzer (Chu trình Euler)
│   └── properties.py         # Kiểm tra 2 phía (Bipartite)
│
├── utils/                    <-- TIỆN ÍCH 
│   ├── __init__.py
│   ├── file_io.py            # Đọc/Ghi file JSON
│   ├── layout_math.py        # Tính toán tọa độ (Sin/Cos)
│   └── converters.py         # Chuyển đổi Ma trận <-> Danh sách kề
│
└── data/                     <-- THƯ MỤC CHỨA FILE INPUT/OUTPUT
    ├── graph_demo.json
    └── test_input.json
```
## Changelog
- 23/11/2025: Tạo trước UI để dễ hình dung hơn ứng dụng BTL mình sẽ làm, từ tuần sau sẽ triển khai dần dần các yêu cầu cần thiết. Nếu muốn chạy thử thì chạy file test.py nhé.