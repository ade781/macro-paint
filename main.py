# main.py
# Peran: Titik masuk utama aplikasi.
# Bertanggung jawab untuk membuat jendela utama dan mengorkestrasi
# pembuatan komponen dari modul-modul lain.

import tkinter as tk
from tkinter import ttk

# Mengimpor kelas-kelas dari modul yang telah kita buat
from features.canvas_feature import CanvasFeature
from features.ui_manager import UIManager
from tools.file_handler import FileHandler


def main():
    """Fungsi utama untuk menginisialisasi dan menjalankan aplikasi."""
    # 1. Inisialisasi jendela utama
    root = tk.Tk()
    root.title("Paint Terstruktur - MADE BY ADE7")
    # -- DIUBAH: Ukuran jendela diperbesar --
    root.geometry("1200x800")

    # Menggunakan style yang lebih modern jika tersedia
    style = ttk.Style()
    try:
        style.theme_use('clam')
    except tk.TclError:
        pass  # Gunakan tema default jika 'clam' tidak ada

    # 2. Inisialisasi komponen inti
    # Frame utama untuk kanvas, ditempatkan terlebih dahulu
    canvas_frame = tk.Frame(
        root, highlightbackground="gray", highlightthickness=1)
    canvas_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    # Inisiasi setiap modul/fitur
    # Kanvas dimasukkan ke dalam frame-nya
    canvas_feature = CanvasFeature(canvas_frame)
    file_handler = FileHandler()

    # 3. Inisialisasi UI Manager yang akan membangun semua tombol dan kontrol
    # UI Manager memerlukan akses ke root, kanvas, dan file_handler untuk menghubungkan tombol
    ui_manager = UIManager(root, canvas_feature, file_handler)
    ui_manager.setup_ui()  # Membangun antarmuka pengguna

    # 4. Menjalankan aplikasi
    root.mainloop()


if __name__ == "__main__":
    main()
