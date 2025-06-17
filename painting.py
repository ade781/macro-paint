# painting.py

import tkinter as tk
from tkinter import filedialog
from PIL import ImageGrab


class PaintApp:
    def __init__(self, root):
        self.root = root
        self.pen_color = "black"
        # -- BARU: Variabel untuk ukuran kuas dan alat yang digunakan --
        self.brush_size = 2
        self.current_tool = "pen"  # Bisa 'pen' atau 'eraser'

        self.setup_canvas()
        self.setup_events()

    def setup_canvas(self):
        """Mempersiapkan kanvas untuk menggambar."""
        # Menambahkan border agar area kanvas terlihat jelas
        self.canvas_frame = tk.Frame(
            self.root, highlightbackground="gray", highlightthickness=1)
        self.canvas_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def setup_events(self):
        """Mengikat event mouse ke fungsi."""
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)
        self.last_x = None
        self.last_y = None

    def paint(self, event):
        """Fungsi untuk menggambar atau menghapus di kanvas."""
        # -- DIUBAH: Logika menggambar disesuaikan dengan alat yang aktif --
        paint_color = self.pen_color if self.current_tool == "pen" else "white"

        if self.last_x and self.last_y:
            self.canvas.create_line(
                self.last_x, self.last_y, event.x, event.y,
                width=self.brush_size,  # Menggunakan ukuran kuas dinamis
                fill=paint_color,
                capstyle=tk.ROUND,
                smooth=tk.TRUE
            )
        self.last_x = event.x
        self.last_y = event.y

    def reset(self, event):
        """Mereset posisi terakhir mouse saat tombol dilepas."""
        self.last_x = None
        self.last_y = None

    def set_color(self, new_color):
        """Mengubah warna pena dan mengaktifkan alat pena."""
        self.pen_color = new_color
        self.current_tool = "pen"

    def set_brush_size(self, new_size):
        """Mengubah ukuran kuas dari slider."""
        self.brush_size = int(float(new_size))

    # -- BARU: Fungsi untuk mengaktifkan alat --
    def use_pen(self):
        """Mengaktifkan alat pena."""
        self.current_tool = "pen"

    def use_eraser(self):
        """Mengaktifkan alat penghapus."""
        self.current_tool = "eraser"

    def clear_canvas(self):
        """Menghapus semua gambar di kanvas."""
        self.canvas.delete("all")

    # -- BARU: Fungsi untuk menyimpan gambar --
    def save_image(self):
        """Menyimpan konten kanvas sebagai file gambar."""
        try:
            # Meminta pengguna memilih lokasi dan nama file
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[
                    ("PNG files", "*.png"),
                    ("JPEG files", "*.jpg"),
                    ("All files", "*.*")
                ]
            )
            if not file_path:
                return  # Pengguna membatalkan dialog

            # Mendapatkan koordinat absolut dari kanvas
            x = self.canvas.winfo_rootx()
            y = self.canvas.winfo_rooty()
            x1 = x + self.canvas.winfo_width()
            y1 = y + self.canvas.winfo_height()

            # Mengambil screenshot dari area kanvas dan menyimpannya
            ImageGrab.grab().crop((x, y, x1, y1)).save(file_path)

        except Exception as e:
            print(f"Gagal menyimpan gambar: {e}")
