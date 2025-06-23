# main.py
# VERSI BARU - Dibuat ulang dari awal untuk stabilitas

import tkinter as tk
from tkinter import ttk

from features.canvas_feature import CanvasFeature
from features.ui_manager import UIManager
from tools.file_handler import FileHandler


def main():
    """Fungsi utama untuk menginisialisasi dan menjalankan aplikasi."""
    root = tk.Tk()
    root.title("Paint Terstruktur v6.0 - Stabilitas Baru")
    root.geometry("1200x800")

    style = ttk.Style()
    try:
        style.theme_use('clam')
    except tk.TclError:
        pass

    canvas_frame = tk.Frame(
        root, highlightbackground="gray", highlightthickness=1)
    canvas_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    # Inisiasi setiap modul
    canvas_feature = CanvasFeature(canvas_frame)
    file_handler = FileHandler()
    ui_manager = UIManager(root, canvas_feature, file_handler)

    # Membangun antarmuka pengguna
    ui_manager.setup_ui()

    # Menghubungkan semua tombol UI ke logika di kanvas untuk manajemen state
    canvas_feature.link_ui_elements(
        pen_button=ui_manager.pen_button,
        eraser_button=ui_manager.eraser_button,
        bucket_button=ui_manager.bucket_button,
        shape_buttons=ui_manager.shape_buttons
    )

    root.mainloop()


if __name__ == "__main__":
    main()
