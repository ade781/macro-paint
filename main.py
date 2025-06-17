# main.py

import tkinter as tk
from tkinter import ttk
from painting import PaintApp


def show_about_dialog(parent):
    """Menampilkan jendela 'Tentang'."""
    about_win = tk.Toplevel(parent)
    about_win.title("Tentang Aplikasi")
    about_win.geometry("300x150")
    about_win.resizable(False, False)

    # Memastikan jendela 'Tentang' selalu di atas jendela utama
    about_win.transient(parent)
    about_win.grab_set()

    # Konten jendela
    ttk.Label(about_win, text="Paint Sederhana v2.0", font=(
        "Helvetica", 12, "bold")).pack(pady=(15, 5))
    ttk.Label(about_win, text="MADE BY ADE7").pack()

    close_button = ttk.Button(about_win, text="Tutup",
                              command=about_win.destroy)
    close_button.pack(pady=15)

    # Menunggu sampai jendela ditutup
    parent.wait_window(about_win)


def main():
    root = tk.Tk()
    # -- DIUBAH: Judul diperbarui --
    root.title("Paint Sederhana - by ADE7")
    root.geometry("850x750")

    style = ttk.Style()
    try:
        style.theme_use('clam')
    except tk.TclError:
        pass

    # -- BARU: Membuat Menu Bar --
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    # Menu File (opsional, tapi bagus untuk struktur)
    file_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Keluar", command=root.quit)

    # Menu Bantuan
    help_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Bantuan", menu=help_menu)
    help_menu.add_command(label="Tentang...",
                          command=lambda: show_about_dialog(root))

    app = PaintApp(root)

    # Frame untuk kontrol
    main_controls_frame = tk.Frame(root, pady=5)
    main_controls_frame.pack(fill=tk.X, padx=10)

    # 1. Frame untuk alat
    tool_frame = ttk.LabelFrame(main_controls_frame, text="Alat", padding=5)
    tool_frame.pack(side=tk.LEFT, padx=5)

    pen_btn = ttk.Button(tool_frame, text="Kuas", command=app.use_pen)
    pen_btn.pack(side=tk.LEFT, padx=2)

    eraser_btn = ttk.Button(
        tool_frame, text="Penghapus", command=app.use_eraser)
    eraser_btn.pack(side=tk.LEFT, padx=2)

    # 2. Frame untuk kontrol kuas
    brush_frame = ttk.LabelFrame(
        main_controls_frame, text="Ukuran Kuas", padding=5)
    brush_frame.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

    brush_slider = ttk.Scale(
        brush_frame, from_=1, to=50, orient=tk.HORIZONTAL,
        command=app.set_brush_size
    )
    brush_slider.set(2)
    brush_slider.pack(fill=tk.X, expand=True)

    # 3. Frame untuk warna
    color_frame = ttk.LabelFrame(main_controls_frame, text="Warna", padding=5)
    color_frame.pack(side=tk.LEFT, padx=5)

    colors = ["black", "red", "green", "blue", "yellow", "purple", "orange"]
    for color in colors:
        btn = tk.Button(color_frame, bg=color, width=3, relief=tk.RIDGE,
                        command=lambda c=color: app.set_color(c))
        btn.pack(side=tk.LEFT, padx=2, pady=2)

    # 4. Frame untuk Aksi
    action_frame = ttk.LabelFrame(main_controls_frame, text="Aksi", padding=5)
    action_frame.pack(side=tk.RIGHT, padx=5)

    clear_btn = ttk.Button(action_frame, text="Bersihkan",
                           command=app.clear_canvas)
    clear_btn.pack(side=tk.LEFT, padx=2)

    save_btn = ttk.Button(action_frame, text="Simpan", command=app.save_image)
    save_btn.pack(side=tk.LEFT, padx=2)

    root.mainloop()


if __name__ == "__main__":
    main()
