# BÀI TẬP LỚN CẤU TRÚC RỜI RẠC

## Yêu cầu bài tập

Xây dựng một ứng dụng thoả mãn các chức năng sau:

* **Phần cơ bản:**
    1. Vẽ đồ thị trực quan
    2. Lưu đồ thị
    3. Tìm đường đi ngắn nhất (Dijkstra)
    4. Duyệt đồ thị theo các chiến lược: BFS & DFS
    5. Kiểm tra một đồ thị có phải là đồ thị 2 phía không?
    6. Chuyển đổi qua lại giữa các phương pháp biểu diễn đồ thị:
        * (ma trận kề <-> danh sách kề <-> danh sách cạnh)
        * (Lưu ý: đồ thị có thể vô hướng & có hướng)

* **Phần nâng cao:**
    7. Trực quan hóa các thuật toán: (Prim, Kruskal, Hierholzer, Fleury, Ford-Fulkerson)
## Cấu trúc các folder và file của bài tập lớn như sau

```text
src/
│
├── main.py                   <-- Dùng để chạy app chính
│
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
│   ├── graph_controller.py   # Xử lý thêm/sửa/xóa đỉnh, cạnh và các tính năng cơ bản
│   ├── algorithm_controller.py # Xử lý việc gọi thuật toán nâng cao (Kruskal, Fleury,...)
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
│   ├── file_processor.py     # Đọc/Ghi file JSON
│   ├── layout_math.py        # Tính toán tọa độ (Sin/Cos)
│   └── converters.py         # Chuyển đổi Ma trận <-> Danh sách kề
│
└── data/                     <-- THƯ MỤC CHỨA FILE INPUT/OUTPUT
```

## Cập nhật
* 23/11/2025: Tạo trước UI để dễ hình dung hơn ứng dụng BTL mình sẽ làm, từ tuần sau sẽ triển khai dần dần các yêu cầu cần thiết.
* 30/11/2025: Thêm tính năng chuyển đổi giữa các kiểu đồ thị (Ma trận kề <-> Danh sách kề <-> Danh sách cạnh)
* 02/12/2025: Thêm tính năng nhập/lưu đồ thị, kiểm tra đồ thị hai phía và duyệt theo BFS, DFS.
* 03/12/2025: Sửa gọn gàng cấu trúc file của ứng dụng. Hoàn thành các tính năng cơ bản cần thiết.
* 04/12/2025: Thêm tính năng chỉnh sửa Node, Edge của đồ thị (Xoá, cập nhật tên đỉnh, trọng số của cạnh,...)
* 11/12/2025: Hoàn thiện các thuật toán nâng cao của chương trình.
