# features/ui_manager.py
# Peran: Mengelola pembuatan dan penataan semua elemen antarmuka pengguna (UI),
# seperti tombol, slider, dan frame.

import tkinter as tk
from tkinter import ttk, messagebox


class UIManager:
    """Membangun dan mengelola semua widget UI."""

    def __init__(self, root, canvas_feature, file_handler):
        self.root = root
        self.canvas = canvas_feature
        self.file_handler = file_handler

    def _show_about(self):
        """Menampilkan dialog 'Tentang'."""
        messagebox.showinfo(
            "Tentang Aplikasi",
            "Paint Terstruktur v5.2\n\nMADE BY ADE7"
        )

    def setup_ui(self):
        """Membangun semua komponen UI dan menatanya di jendela."""
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

        main_controls_frame = tk.Frame(self.root, pady=5)
        main_controls_frame.pack(fill=tk.X, padx=10, side=tk.TOP)

        # --- DIPERBARUI: Membuat frame baru untuk menampung Alat dan Ukuran ---
        left_panel_frame = tk.Frame(main_controls_frame)
        left_panel_frame.pack(side=tk.LEFT, padx=5, anchor='n')

        # Frame Alat Dasar sekarang ada di dalam left_panel_frame
        tool_frame = ttk.LabelFrame(
            left_panel_frame, text="Alat Dasar", padding=5)
        tool_frame.pack(side=tk.TOP, pady=(0, 5))
        pen_btn = ttk.Button(tool_frame, text="Kuas",
                             command=self.canvas.use_pen)
        pen_btn.pack(side=tk.LEFT, padx=2)
        eraser_btn = ttk.Button(
            tool_frame, text="Penghapus", command=self.canvas.use_eraser)
        eraser_btn.pack(side=tk.LEFT, padx=2)

        # Frame Ukuran/Tebal sekarang ada di dalam left_panel_frame, di bawah Alat
        brush_frame = ttk.LabelFrame(
            left_panel_frame, text="Ukuran/Tebal", padding=5)
        brush_frame.pack(side=tk.TOP)
        brush_slider = ttk.Scale(
            brush_frame, from_=1, to=50, orient=tk.HORIZONTAL,
            command=self.canvas.set_brush_size
        )
        brush_slider.set(2)
        brush_slider.pack(fill=tk.X, expand=True)

        # Frame Bentuk tetap sama
        shape_frame = ttk.LabelFrame(
            main_controls_frame, text="Bentuk", padding=5)
        shape_frame.pack(side=tk.LEFT, padx=5)
        shape_map = {
            "line": "Garis", "rectangle": "Persegi", "oval": "Lingkaran", "triangle": "Segitiga",
            "right_triangle": "Siku-siku", "diamond": "Wajik", "pentagon": "Segi-5", "star": "Bintang"
        }
        for i, (shape_name, shape_text) in enumerate(shape_map.items()):
            btn = ttk.Button(shape_frame, text=shape_text,
                             command=lambda s=shape_name: self.canvas.set_shape_tool(s))
            btn.grid(row=i // 4, column=i % 4, padx=2, pady=2)

        # --- DIPERBARUI: Frame Warna diatur menjadi 2 baris ---
        color_frame = ttk.LabelFrame(
            main_controls_frame, text="Warna", padding=5)
        color_frame.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        colors = ["black", "red", "green", "blue", "yellow",
                  "purple", "orange", "cyan", "magenta", "white"]
        for i, color in enumerate(colors):
            btn = tk.Button(color_frame, bg=color, width=3, relief=tk.RIDGE,
                            command=lambda c=color: self.canvas.set_color(c))
            # Menggunakan grid 2x5
            btn.grid(row=i // 5, column=i % 5, padx=2, pady=2)

        # Frame Aksi tetap di kanan
        action_frame = ttk.LabelFrame(
            main_controls_frame, text="Aksi", padding=5)
        action_frame.pack(side=tk.RIGHT, padx=5)
        undo_btn = ttk.Button(action_frame, text="Undo",
                              command=self.canvas.undo)
        undo_btn.pack(side=tk.LEFT, padx=2)
        redo_btn = ttk.Button(action_frame, text="Redo",
                              command=self.canvas.redo)
        redo_btn.pack(side=tk.LEFT, padx=2)
        clear_btn = ttk.Button(
            action_frame, text="Bersihkan", command=self.canvas.clear)
        clear_btn.pack(side=tk.LEFT, padx=2)
