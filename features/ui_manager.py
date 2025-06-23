# features/ui_manager.py
# VERSI BARU - Dibuat ulang dari awal untuk stabilitas

import tkinter as tk
from tkinter import ttk, messagebox


class UIManager:
    """Membangun dan mengelola semua widget UI dengan pendekatan yang bersih."""

    def __init__(self, root, canvas_feature, file_handler):
        self.root = root
        self.canvas = canvas_feature
        self.file_handler = file_handler

        # Atribut untuk semua tombol yang statusnya perlu dikelola
        self.pen_button = None
        self.eraser_button = None
        self.bucket_button = None
        self.shape_buttons = {}

    def _show_about(self):
        """Menampilkan dialog 'Tentang'."""
        messagebox.showinfo(
            "Tentang Aplikasi",
            "Paint Terstruktur v6.0\n\nMADE BY ADE7\nDirevisi untuk Stabilitas"
        )

    def setup_ui(self):
        """Membangun semua komponen UI dan menatanya di jendela."""
        # --- Menu Bar ---
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(
            label="Simpan", command=lambda: self.file_handler.save_image(self.canvas.canvas))
        file_menu.add_separator()
        file_menu.add_command(label="Keluar", command=self.root.quit)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Bantuan", menu=help_menu)
        help_menu.add_command(label="Tentang...", command=self._show_about)

        # --- Frame Kontrol Utama ---
        main_controls_frame = tk.Frame(self.root, pady=5)
        main_controls_frame.pack(fill=tk.X, padx=10, side=tk.TOP)

        left_panel_frame = tk.Frame(main_controls_frame)
        left_panel_frame.pack(side=tk.LEFT, padx=5, anchor='n')

        # --- Frame Alat Dasar ---
        tool_frame = ttk.LabelFrame(
            left_panel_frame, text="Alat Dasar", padding=5)
        tool_frame.pack(side=tk.TOP, pady=(0, 5), fill=tk.X)

        self.pen_button = tk.Button(
            tool_frame, text="Kuas", command=self.canvas.use_pen)
        self.pen_button.pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)

        self.eraser_button = tk.Button(
            tool_frame, text="Penghapus", command=self.canvas.use_eraser)
        self.eraser_button.pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)

        self.bucket_button = tk.Button(
            tool_frame, text="Ember Cat", command=self.canvas.use_bucket)
        self.bucket_button.pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)

        # --- Frame Ukuran Kuas ---
        brush_frame = ttk.LabelFrame(
            left_panel_frame, text="Ukuran/Tebal", padding=5)
        brush_frame.pack(side=tk.TOP, fill=tk.X, pady=5)
        brush_slider = ttk.Scale(
            brush_frame, from_=1, to=50, orient=tk.HORIZONTAL, command=self.canvas.set_brush_size)
        brush_slider.set(2)
        brush_slider.pack(fill=tk.X, expand=True)

        # --- Frame Bentuk ---
        shape_frame = ttk.LabelFrame(
            main_controls_frame, text="Bentuk", padding=5)
        shape_frame.pack(side=tk.LEFT, padx=5, anchor='n')
        shape_map = {
            "line": "Garis", "rectangle": "Persegi", "oval": "Lingkaran", "triangle": "Segitiga",
            "right_triangle": "Siku-siku", "diamond": "Wajik", "pentagon": "Segi-5", "star": "Bintang"
        }
        for i, (shape_name, shape_text) in enumerate(shape_map.items()):
            btn = tk.Button(shape_frame, text=shape_text,
                            command=lambda s=shape_name: self.canvas.set_shape_tool(s))
            btn.grid(row=i // 4, column=i % 4, padx=2, pady=2, sticky='ew')
            self.shape_buttons[shape_name] = btn

        # --- Frame Warna ---
        color_frame = ttk.LabelFrame(
            main_controls_frame, text="Warna", padding=5)
        color_frame.pack(side=tk.LEFT, padx=5, fill=tk.BOTH, expand=True)
        colors = ["black", "red", "green", "blue", "yellow",
                  "purple", "orange", "cyan", "magenta", "white"]
        for i, color in enumerate(colors):
            btn = tk.Button(color_frame, bg=color, width=3, relief=tk.RIDGE,
                            command=lambda c=color: self.canvas.set_color(c))
            btn.grid(row=i // 5, column=i % 5, padx=3, pady=3, sticky='nsew')
            color_frame.grid_columnconfigure(i % 5, weight=1)
        color_frame.grid_rowconfigure(0, weight=1)
        color_frame.grid_rowconfigure(1, weight=1)

        # --- Frame Aksi ---
        action_frame = ttk.LabelFrame(
            main_controls_frame, text="Aksi", padding=5)
        action_frame.pack(side=tk.RIGHT, padx=5, anchor='n')
        undo_btn = ttk.Button(action_frame, text="Undo",
                              command=self.canvas.undo)
        undo_btn.pack(side=tk.LEFT, padx=2)
        redo_btn = ttk.Button(action_frame, text="Redo",
                              command=self.canvas.redo)
        redo_btn.pack(side=tk.LEFT, padx=2)
        clear_btn = ttk.Button(
            action_frame, text="Bersihkan", command=self.canvas.clear)
        clear_btn.pack(side=tk.LEFT, padx=2)
