# features/canvas_feature.py
# VERSI BARU - Dibuat ulang dari awal untuk stabilitas

import tkinter as tk
import math


class CanvasFeature:
    """Mengelola fungsionalitas kanvas gambar dengan state management yang benar."""

    def __init__(self, parent_frame):
        # State Internal
        self.pen_color = "black"
        self.brush_size = 2
        self.current_tool = "pen"
        self.current_shape = None
        self.start_x = None
        self.start_y = None
        self.temp_shape_id = None
        self.history = []
        self.redo_stack = []
        self.current_stroke = []

        # Referensi UI
        self.pen_button = None
        self.eraser_button = None
        self.bucket_button = None
        self.shape_buttons = {}

        # Setup Canvas
        self.canvas = tk.Canvas(parent_frame, bg="white", cursor="crosshair")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self._on_press)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)

    def link_ui_elements(self, pen_button, eraser_button, bucket_button, shape_buttons):
        """Menghubungkan semua elemen UI dari UIManager untuk manajemen state."""
        self.pen_button = pen_button
        self.eraser_button = eraser_button
        self.bucket_button = bucket_button
        self.shape_buttons = shape_buttons
        self.use_pen()  # Mengaktifkan Kuas sebagai alat default saat startup

    def _deactivate_all_tools(self):
        """Mengatur SEMUA tombol alat (dasar dan bentuk) ke status normal (tidak ditekan)."""
        if self.pen_button:
            self.pen_button.config(relief=tk.RAISED)
        if self.eraser_button:
            self.eraser_button.config(relief=tk.RAISED)
        if self.bucket_button:
            self.bucket_button.config(relief=tk.RAISED)
        for button in self.shape_buttons.values():
            button.config(relief=tk.RAISED)

    # --- Logika Event (Tidak berubah banyak) ---
    def _on_press(self, event):
        if self.current_tool == "bucket":
            self._fill_at(event.x, event.y)
        else:
            self.start_x = event.x
            self.start_y = event.y
            if self.current_tool in ["pen", "eraser"]:
                self.last_x, self.last_y = event.x, event.y

    def _on_drag(self, event):
        if self.current_tool in ["pen", "eraser"]:
            self._paint(event)
        elif self.current_tool == "shape" and self.start_x is not None:
            self._draw_shape_preview(event.x, event.y)

    def _on_release(self, event):
        if self.current_tool == "shape" and self.start_x is not None:
            self._finalize_shape(event.x, event.y)
        elif self.current_tool in ["pen", "eraser"]:
            self._finalize_stroke()
        self.start_x, self.start_y, self.temp_shape_id = None, None, None

    # --- Logika Menggambar (Kode Asli Anda) ---
    def _paint(self, event):
        paint_color = self.pen_color if self.current_tool == "pen" else "white"
        if self.last_x and self.last_y:
            item_id = self.canvas.create_line(
                self.last_x, self.last_y, event.x, event.y,
                width=self.brush_size, fill=paint_color, capstyle=tk.ROUND, smooth=tk.TRUE
            )
            self.current_stroke.append(item_id)
        self.last_x, self.last_y = event.x, event.y

    def _get_shape_coords(self, end_x, end_y):
        sx, sy, ex, ey = self.start_x, self.start_y, end_x, end_y
        center_x, center_y = (sx + ex) / 2, (sy + ey) / 2
        radius_x, radius_y = abs(ex - sx) / 2, abs(ey - sy) / 2
        coords = {'line': (sx, sy, ex, ey), 'rectangle': (sx, sy, ex, ey), 'oval': (sx, sy, ex, ey),
                  'triangle': (sx, ey, (sx+ex)/2, sy, ex, ey), 'right_triangle': (sx, sy, sx, ey, ex, ey),
                  'diamond': (center_x, sy, ex, center_y, center_x, ey, sx, center_y)}
        pent_points = []
        for i in range(5):
            angle = math.pi/2 + (2*math.pi*i)/5
            pent_points.extend(
                (center_x + radius_x*math.cos(angle), center_y - radius_y*math.sin(angle)))
        coords['pentagon'] = tuple(pent_points)
        star_points = []
        for i in range(10):
            r, ry = (radius_x, radius_y) if i % 2 == 0 else (
                radius_x/2, radius_y/2)
            angle = math.pi/2 + (2*math.pi*i)/10
            star_points.extend((center_x + r*math.cos(angle),
                               center_y - ry*math.sin(angle)))
        coords['star'] = tuple(star_points)
        return coords.get(self.current_shape)

    def _draw_shape(self, coords):
        if not coords:
            return None
        st, sc, sw, sf = self.current_shape, self.pen_color, self.brush_size, ""
        if st in ['line']:
            return self.canvas.create_line(*coords, fill=sc, width=sw)
        elif st in ['rectangle', 'oval']:
            return (self.canvas.create_rectangle if st == 'rectangle' else self.canvas.create_oval)(*coords, outline=sc, width=sw, fill=sf)
        elif st in ['triangle', 'right_triangle', 'diamond', 'pentagon', 'star']:
            return self.canvas.create_polygon(coords, outline=sc, width=sw, fill=sf)

    def _draw_shape_preview(self, end_x, end_y):
        if self.temp_shape_id:
            self.canvas.delete(self.temp_shape_id)
        self.temp_shape_id = self._draw_shape(
            self._get_shape_coords(end_x, end_y))

    # --- Logika Alat & Aksi ---
    def _fill_at(self, x, y):
        try:
            items = self.canvas.find_overlapping(x, y, x, y)
            if not items:
                return
            item_id = items[-1]
            if self.canvas.type(item_id) == "line":
                return
            old_fill_color = self.canvas.itemcget(item_id, "fill")
            if old_fill_color == self.pen_color:
                return
            self.canvas.itemconfigure(item_id, fill=self.pen_color)
            action = {'action': 'configure', 'item': item_id, 'before': {
                'fill': old_fill_color}, 'after': {'fill': self.pen_color}}
            self.history.append(action)
            self.redo_stack.clear()
        except tk.TclError:
            pass

    def _finalize_stroke(self):
        if self.current_stroke:
            action = {'action': 'create', 'items': self.current_stroke}
            self.history.append(action)
            self.current_stroke = []
            self.redo_stack.clear()

    def _finalize_shape(self, end_x, end_y):
        if self.temp_shape_id:
            self.canvas.delete(self.temp_shape_id)
        coords = self._get_shape_coords(end_x, end_y)
        shape_id = self._draw_shape(coords)
        if shape_id:
            action = {'action': 'create', 'items': [shape_id]}
            self.history.append(action)
            self.redo_stack.clear()

    def undo(self):
        if not self.history:
            return
        last_action = self.history.pop()
        if last_action['action'] == 'create':
            for item_id in last_action['items']:
                self.canvas.itemconfigure(item_id, state='hidden')
        elif last_action['action'] == 'configure':
            self.canvas.itemconfigure(
                last_action['item'], **last_action['before'])
        self.redo_stack.append(last_action)

    def redo(self):
        if not self.redo_stack:
            return
        action_to_redo = self.redo_stack.pop()
        if action_to_redo['action'] == 'create':
            for item_id in action_to_redo['items']:
                self.canvas.itemconfigure(item_id, state='normal')
        elif action_to_redo['action'] == 'configure':
            self.canvas.itemconfigure(
                action_to_redo['item'], **action_to_redo['after'])
        self.history.append(action_to_redo)

    def set_color(self, c): self.pen_color = c
    def set_brush_size(self, s): self.brush_size = int(float(s))

    def use_pen(self):
        self._deactivate_all_tools()
        self.current_tool = "pen"
        if self.pen_button:
            self.pen_button.config(relief=tk.SUNKEN)

    def use_eraser(self):
        self._deactivate_all_tools()
        self.current_tool = "eraser"
        if self.eraser_button:
            self.eraser_button.config(relief=tk.SUNKEN)

    def use_bucket(self):
        self._deactivate_all_tools()
        self.current_tool = "bucket"
        if self.bucket_button:
            self.bucket_button.config(relief=tk.SUNKEN)

    def set_shape_tool(self, s):
        self._deactivate_all_tools()
        self.current_tool, self.current_shape = "shape", s
        if s in self.shape_buttons:
            self.shape_buttons[s].config(relief=tk.SUNKEN)

    def clear(self):
        self.canvas.delete("all")
        self.history.clear()
        self.redo_stack.clear()
        self.current_stroke.clear()
