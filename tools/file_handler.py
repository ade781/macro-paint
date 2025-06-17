# tools/file_handler.py
# Peran: Mengelola semua operasi yang berhubungan dengan file,
# seperti menyimpan gambar. Ini mengisolasi logika I/O.

from tkinter import filedialog
from PIL import ImageGrab


class FileHandler:
    """Menangani operasi file seperti menyimpan."""

    def save_image(self, canvas_widget):
        """
        Menyimpan konten kanvas sebagai file gambar.

        Args:
            canvas_widget (tk.Canvas): Widget kanvas yang akan disimpan.
        """
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[
                    ("PNG files", "*.png"),
                    ("JPEG files", "*.jpg"),
                    ("All files", "*.*")
                ]
            )
            if not file_path:
                return  # Keluar jika pengguna membatalkan dialog

            # Mendapatkan koordinat absolut dari widget kanvas
            x = canvas_widget.winfo_rootx()
            y = canvas_widget.winfo_rooty()
            x1 = x + canvas_widget.winfo_width()
            y1 = y + canvas_widget.winfo_height()

            # Mengambil screenshot dari area kanvas dan menyimpannya
            ImageGrab.grab().crop((x, y, x1, y1)).save(file_path)
            print(f"Gambar berhasil disimpan di: {file_path}")

        except Exception as e:
            # Sebaiknya tampilkan pesan error ini di UI, tapi untuk sekarang di console saja
            print(f"Gagal menyimpan gambar: {e}")
