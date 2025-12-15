import tkinter as tk
from tkinter import ttk

class ControlPanel(tk.Frame):
    def __init__(self, master, controller=None, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.bg_color = kwargs.get('bg', '#f4f6f7')
        self._init_widgets()

    def _init_widgets(self):
        tk.Label(self, text="ĐIỀU KHIỂN ĐỒ THỊ", font=("Arial", 14, "bold"), bg=self.bg_color).pack(pady=(0, 10))

        # --- SECTION 1: FILE & INPUT ---
        frame_config = tk.LabelFrame(self, text="1. File & Nhập liệu", bg=self.bg_color, font=("Arial", 10, "bold"))
        frame_config.pack(fill=tk.X, pady=5)

        file_btn_frame = tk.Frame(frame_config, bg=self.bg_color)
        file_btn_frame.pack(fill=tk.X, padx=5, pady=5)
        tk.Button(file_btn_frame, text="📂 Mở File", bg="#34495e", fg="white", 
                  command=self.controller.action_load).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        tk.Button(file_btn_frame, text="💾 Lưu File", bg="#34495e", fg="white", 
                  command=self.controller.action_save).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        chk_frame = tk.Frame(frame_config, bg=self.bg_color)
        chk_frame.pack(fill=tk.X, padx=5)

        self.var_directed = tk.BooleanVar(value=True)
        tk.Checkbutton(chk_frame, text="Đồ thị Có Hướng", var=self.var_directed, 
                       bg=self.bg_color, command=self.controller.toggle_mode).pack(side=tk.LEFT)

        grid_input = tk.Frame(frame_config, bg=self.bg_color)
        grid_input.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(grid_input, text="Từ:", bg=self.bg_color).grid(row=0, column=0)
        self.ent_u = tk.Entry(grid_input, width=4); self.ent_u.grid(row=0, column=1)
        
        tk.Label(grid_input, text="Đến:", bg=self.bg_color).grid(row=0, column=2)
        self.ent_v = tk.Entry(grid_input, width=4); self.ent_v.grid(row=0, column=3)
        
        tk.Label(grid_input, text="W:", bg=self.bg_color).grid(row=0, column=4)
        self.ent_w = tk.Entry(grid_input, width=4); self.ent_w.insert(0,"1"); self.ent_w.grid(row=0, column=5)

        tk.Button(grid_input, text="Thêm", bg="#27ae60", fg="white", 
                  command=self.controller.action_add_edge).grid(row=0, column=6, padx=5)
        
        tk.Button(frame_config, text="👁 Xem Ma trận / DS Kề", 
                  command=self.controller.action_convert_view).pack(fill=tk.X, padx=5, pady=5)

        # --- SECTION 2: ALGORITHMS ---
        frame_algo = tk.LabelFrame(self, text="2. Duyệt & Kiểm tra", bg=self.bg_color, font=("Arial", 10, "bold"))
        frame_algo.pack(fill=tk.X, pady=10)
        
        tk.Label(frame_algo, text="Đỉnh bắt đầu:", bg=self.bg_color).pack(anchor="w", padx=5)
        self.ent_start_node = tk.Entry(frame_algo, width=10)
        self.ent_start_node.pack(anchor="w", padx=5, pady=(0,5))

        row_algo = tk.Frame(frame_algo, bg=self.bg_color)
        row_algo.pack(fill=tk.X)
        tk.Button(row_algo, text="BFS", width=6, command=lambda: self.controller.run_basic_algo("BFS")).pack(side=tk.LEFT, padx=2)
        tk.Button(row_algo, text="DFS", width=6, command=lambda: self.controller.run_basic_algo("DFS")).pack(side=tk.LEFT, padx=2)
        
        mb_path = tk.Menubutton(row_algo, text="Tìm đường đi", relief=tk.RAISED, bg="#e74c3c", fg="white")
        menu_path = tk.Menu(mb_path, tearoff=0)
        
        # Thêm 2 lựa chọn vào menu
        menu_path.add_command(label="Dijkstra", command=lambda: self.controller.run_shortest_path("Dijkstra"))
        menu_path.add_command(label="Bellman-Ford", command=lambda: self.controller.run_shortest_path("Bellman-Ford"))
        
        mb_path.config(menu=menu_path)
        mb_path.pack(side=tk.LEFT, padx=2)

        # Nút kiểm tra 2 phía (giữ nguyên hoặc dời sang phải)
        tk.Button(row_algo, text="2 Phía", command=lambda: self.controller.run_basic_algo("BIPARTITE")).pack(side=tk.LEFT, padx=2)
       
        # --- SECTION 3: ADVANCED ---
        frame_adv = tk.LabelFrame(self, text="3. Nâng cao", bg=self.bg_color, font=("Arial", 10, "bold"))
        frame_adv.pack(fill=tk.X, pady=10)

        tk.Label(frame_adv, text="Chọn thuật toán:", bg=self.bg_color).pack(anchor="w", padx=5)
        self.algo_choice = tk.StringVar()
        self.combo_algo = ttk.Combobox(frame_adv, textvariable=self.algo_choice, state="readonly")
        self.combo_algo['values'] = ("Prim", "Kruskal", "Ford-Fulkerson", "Fleury", "Hierholzer")
        self.combo_algo.current(0)
        self.combo_algo.pack(fill=tk.X, padx=5, pady=5)

        tk.Label(frame_adv, text="Đỉnh đích (Ford-Fulkerson):", bg=self.bg_color).pack(anchor="w", padx=5)
        self.ent_end_node = tk.Entry(frame_adv, width=10)
        self.ent_end_node.pack(anchor="w", padx=5, pady=(0,5))

        tk.Button(frame_adv, text="▶ CHẠY THUẬT TOÁN", bg="#e67e22", fg="white", font=("Arial", 10, "bold"),
                  command=self.controller.run_advanced_algo).pack(fill=tk.X, padx=5, pady=10)

        self.log_box = tk.Text(self, height=10, font=("Consolas", 9))
        self.log_box.pack(fill=tk.BOTH, expand=True)

    def append_log(self, message):
        self.log_box.insert(tk.END, f"> {message}\n")
        self.log_box.see(tk.END)

    def clear_log(self):
        """Xóa toàn bộ nội dung trong khung Log"""
        self.log_box.delete('1.0', tk.END)