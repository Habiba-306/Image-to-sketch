"""
Painter's Grid Assistant
Main feature: Grid overlay on image for canvas transfer.
Sketch view is optional. No image cropping.
"""

import cv2
import numpy as np
import string
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk


# ─── CORE FUNCTIONS ──────────────────────────────────────────────────────────

def apply_grid(img_bgr: np.ndarray, cols: int, rows: int,
               opacity: float, thickness: int, color_mode: str,
               label_cells: bool, label_size: float = 0.6) -> np.ndarray:
    img = img_bgr.copy()
    h, w = img.shape[:2]
    cw, ch = w // cols, h // rows

    COLORS = {"red": (0,0,220), "blue": (200,60,0), "green": (20,160,20),
              "black": (0,0,0), "white": (255,255,255)}
    color   = COLORS.get(color_mode, (0, 0, 220))
    overlay = img.copy()

    for i in range(1, cols):
        cv2.line(overlay, (i*cw, 0), (i*cw, h), color, thickness)
    for j in range(1, rows):
        cv2.line(overlay, (0, j*ch), (w, j*ch), color, thickness)
    cv2.rectangle(overlay, (0, 0), (w-1, h-1), color, thickness+1)
    cv2.addWeighted(overlay, opacity, img, 1-opacity, 0, img)

    if label_cells:
        letters    = string.ascii_uppercase
        fs         = max(0.25, label_size)          # font scale
        ft         = max(1, int(label_size * 2.0))  # font thickness

        def _put(text, x, y):
            """Draw white shadow then colored text for legibility."""
            cv2.putText(img, text, (x+1, y+1), cv2.FONT_HERSHEY_SIMPLEX,
                        fs, (255,255,255), ft+1, cv2.LINE_AA)
            cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                        fs, color, ft, cv2.LINE_AA)

        # ── Column letters along the TOP edge ─────────────────────
        for c in range(cols):
            letter = letters[c % 26]
            tw, th = cv2.getTextSize(letter, cv2.FONT_HERSHEY_SIMPLEX, fs, ft)[0]
            x = c*cw + (cw - tw) // 2          # horizontally centred in column
            y = min(th + 6, ch - 4)             # near top, inside image bounds
            _put(letter, x, y)

        # ── Row numbers along the LEFT edge ───────────────────────
        for r in range(rows):
            number = str(r + 1)
            tw, th = cv2.getTextSize(number, cv2.FONT_HERSHEY_SIMPLEX, fs, ft)[0]
            x = 4                               # near left edge
            y = r*ch + (ch + th) // 2          # vertically centred in row
            _put(number, x, y)

    return img


def fit_image(img: np.ndarray, target_w: int, target_h: int) -> np.ndarray:
    """Scale image to fit inside target dimensions, preserving aspect ratio. No cropping."""
    ih, iw = img.shape[:2]
    scale  = min(target_w / iw, target_h / ih)
    nw, nh = int(iw * scale), int(ih * scale)
    return cv2.resize(img, (nw, nh), interpolation=cv2.INTER_LANCZOS4)


def create_sketch(img_bgr: np.ndarray, blur: int = 21) -> np.ndarray:
    k = blur if blur % 2 == 1 else blur + 1
    k = max(3, k)
    gray    = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(255 - gray, (k, k), 0)
    sketch  = cv2.divide(gray, 255 - blurred, scale=256.0)
    return cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)


def export_pdf(images: dict, path: str):
    pil_imgs = [Image.fromarray(cv2.cvtColor(v, cv2.COLOR_BGR2RGB))
                for v in images.values()]
    if pil_imgs:
        pil_imgs[0].save(path, save_all=True, append_images=pil_imgs[1:], resolution=150)


# ─── GUI ─────────────────────────────────────────────────────────────────────

class App(tk.Tk):
    BG     = "#1a1a2e"
    PANEL  = "#16213e"
    ACC    = "#e94560"
    TEXT   = "#eaeaea"
    SUB    = "#a0a0b0"
    ENT    = "#0f3460"
    CBGR   = "#0d0d1a"

    def __init__(self):
        super().__init__()
        self.title("Painter's Grid Assistant")
        self.configure(bg=self.BG)
        self.state("zoomed")
        self.minsize(900, 600)

        self._orig        = None   # raw loaded image (np BGR)
        self._processed   = {}     # title → full-res np array for saving
        self._ph_main     = None
        self._ph_sketch   = None
        self._resize_job  = None

        self._build_ui()
        self.bind("<Configure>", self._on_resize)

    # ─── BUILD UI ─────────────────────────────────────────────────

    def _build_ui(self):
        self._style()

        sidebar = tk.Frame(self, bg=self.PANEL, width=300)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        self._content = tk.Frame(self, bg=self.BG)
        self._content.pack(side="left", fill="both", expand=True)

        self._build_sidebar(sidebar)
        self._build_content()

    def _build_sidebar(self, p):
        # Scrollable sidebar
        sb  = ttk.Scrollbar(p, orient="vertical")
        cvs = tk.Canvas(p, bg=self.PANEL, highlightthickness=0,
                        yscrollcommand=sb.set)
        sb.config(command=cvs.yview)
        sb.pack(side="right", fill="y")
        cvs.pack(side="left", fill="both", expand=True)
        inner = tk.Frame(cvs, bg=self.PANEL)
        win   = cvs.create_window((0,0), window=inner, anchor="nw")

        def _cfg(e):
            cvs.configure(scrollregion=cvs.bbox("all"))
            cvs.itemconfig(win, width=cvs.winfo_width())
        inner.bind("<Configure>", _cfg)
        cvs.bind("<MouseWheel>",
                 lambda e: cvs.yview_scroll(int(-1*(e.delta/120)), "units"))

        q = inner
        self._lbl(q, "Grid Assistant", 14, bold=True, color=self.ACC
                  ).pack(anchor="w", padx=14, pady=(16,2))
        self._lbl(q, "Load image → configure → Process", 9, color=self.SUB
                  ).pack(anchor="w", padx=14, pady=(0,8))

        self._sep(q)
        self._head(q, "Grid Settings")
        self.cols_var = tk.StringVar(value="10")
        self.rows_var = tk.StringVar(value="8")
        self._pair(q, "Columns:", self.cols_var, "Rows:", self.rows_var)

        self._head(q, "Grid Color")
        self.color_var = tk.StringVar(value="red")
        self._combo(q, self.color_var, ["red","blue","green","black","white"])

        self._head(q, "Line Thickness")
        self.thick_var = tk.IntVar(value=2)
        self._scale(q, self.thick_var, 1, 8, 1)

        self._head(q, "Grid Opacity")
        self.opacity_var = tk.DoubleVar(value=0.80)
        self._scale(q, self.opacity_var, 0.1, 1.0, 0.05)

        self._head(q, "Label Size")
        self.label_size_var = tk.DoubleVar(value=0.6)
        self._scale(q, self.label_size_var, 0.2, 2.0, 0.1)

        self._head(q, "Options")
        self.labels_var = tk.BooleanVar(value=True)
        self._check(q, "Show cell labels (A1, B2…)", self.labels_var)

        self.sketch_var = tk.BooleanVar(value=False)
        self._check(q, "Show sketch view below", self.sketch_var)

        self.sketch_blur_var = tk.IntVar(value=21)
        self._sketch_blur_lbl = self._head(q, "Sketch Strength")
        self._sketch_blur_scale = self._scale(q, self.sketch_blur_var, 3, 111, 2)

        self._sep(q)

        for txt, cmd in [
            ("Load Image", self._load),
            ("Process",    self._process),
            ("Save PNGs",  self._save_pngs),
            ("Export PDF", self._export_pdf),
        ]:
            self._btn(q, txt, cmd)

        self._sep(q)
        self.status_var = tk.StringVar(value="Ready.")
        tk.Label(q, textvariable=self.status_var, fg=self.SUB, bg=self.PANEL,
                 font=("Segoe UI", 9), wraplength=260, justify="left"
                 ).pack(anchor="w", padx=14, pady=(4,16))

    def _build_content(self):
        p = self._content

        self._main_lbl = tk.Label(p, text="Original + Grid",
                 font=("Segoe UI", 11, "bold"),
                 fg=self.ACC, bg=self.BG)
        self._main_lbl.pack(anchor="w", padx=12, pady=(10,2))

        self.c_main = tk.Canvas(p, bg=self.CBGR,
                                highlightthickness=2,
                                highlightbackground=self.ACC)
        self.c_main.pack(fill="both", expand=True, padx=12, pady=(2,4))

        self._div = tk.Frame(p, bg=self.ACC, height=2)

        self._sk_lbl = tk.Label(p, text="Sketch + Grid",
                 font=("Segoe UI", 11, "bold"),
                 fg=self.ACC, bg=self.BG)

        self.c_sketch = tk.Canvas(p, bg=self.CBGR,
                                  highlightthickness=2,
                                  highlightbackground=self.ACC)

        self.after(200, lambda: self._placeholder(self.c_main, "Original + Grid appears here"))

    # ─── WIDGET HELPERS ───────────────────────────────────────────

    def _style(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure("C.TCombobox", fieldbackground=self.ENT,
                    background=self.ENT, foreground=self.TEXT,
                    selectbackground=self.ACC)
        s.configure("Vertical.TScrollbar", background=self.ENT,
                    troughcolor=self.PANEL, arrowcolor=self.TEXT)

    def _lbl(self, p, text, size=10, bold=False, color=None):
        color = color or self.TEXT
        font  = ("Segoe UI", size, "bold") if bold else ("Segoe UI", size)
        return tk.Label(p, text=text, font=font, fg=color, bg=self.PANEL)

    def _sep(self, p):
        tk.Frame(p, bg=self.ENT, height=1).pack(fill="x", padx=10, pady=6)

    def _head(self, p, text):
        l = tk.Label(p, text=text, font=("Segoe UI", 10, "bold"),
                     fg=self.TEXT, bg=self.PANEL)
        l.pack(anchor="w", padx=14, pady=(8,2))
        return l

    def _pair(self, p, l1, v1, l2, v2):
        f = tk.Frame(p, bg=self.PANEL)
        f.pack(fill="x", padx=14, pady=3)
        for col, (lbl, var) in enumerate([(l1,v1),(l2,v2)]):
            tk.Label(f, text=lbl, fg=self.SUB, bg=self.PANEL,
                     font=("Segoe UI",10)).grid(row=0, column=col*2, sticky="w")
            tk.Entry(f, textvariable=var, width=5, bg=self.ENT, fg=self.TEXT,
                     insertbackground=self.TEXT, relief="flat",
                     font=("Segoe UI",11)).grid(row=0, column=col*2+1, padx=(3,14))

    def _combo(self, p, var, vals):
        ttk.Combobox(p, textvariable=var, values=vals, width=13,
                     state="readonly", style="C.TCombobox",
                     font=("Segoe UI",10)).pack(anchor="w", padx=16, pady=3)

    def _scale(self, p, var, lo, hi, res):
        s = tk.Scale(p, variable=var, from_=lo, to=hi, resolution=res,
                     orient="horizontal", bg=self.PANEL, fg=self.TEXT,
                     troughcolor=self.ENT, highlightthickness=0,
                     activebackground=self.ACC, length=250,
                     font=("Segoe UI",9))
        s.pack(anchor="w", padx=14, pady=2)
        return s

    def _check(self, p, text, var):
        tk.Checkbutton(p, text=text, variable=var,
                       fg=self.TEXT, bg=self.PANEL,
                       selectcolor=self.ENT,
                       activebackground=self.PANEL,
                       activeforeground=self.ACC,
                       font=("Segoe UI",10)
                       ).pack(anchor="w", padx=18, pady=2)

    def _btn(self, p, text, cmd):
        b = tk.Button(p, text=text, command=cmd,
                      bg=self.ACC, fg="white",
                      activebackground="#c73652", activeforeground="white",
                      relief="flat", bd=0,
                      font=("Segoe UI",11,"bold"),
                      cursor="hand2", pady=9)
        b.pack(fill="x", padx=14, pady=3)
        b.bind("<Enter>", lambda e: b.config(bg="#c73652"))
        b.bind("<Leave>", lambda e: b.config(bg=self.ACC))

    def _placeholder(self, canvas, text):
        w = canvas.winfo_width()  or 700
        h = canvas.winfo_height() or 300
        canvas.delete("all")
        canvas.create_text(w//2, h//2, text=text,
                           fill=self.SUB, font=("Segoe UI",13))

    # ─── DRAW IMAGE ON CANVAS (fills space, no cropping) ─────────

    def _draw(self, canvas: tk.Canvas, img_bgr: np.ndarray, ref_attr: str):
        canvas.update_idletasks()
        cw = canvas.winfo_width()
        ch = canvas.winfo_height()

        if cw <= 1 or ch <= 1:
            self.after(80, lambda: self._draw(canvas, img_bgr, ref_attr))
            return

        rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        pil = Image.fromarray(rgb)
        iw, ih = pil.size

        # Fit image INSIDE canvas — no cropping, no distortion
        scale = min((cw - 4) / iw, (ch - 4) / ih)
        nw    = max(1, int(iw * scale))
        nh    = max(1, int(ih * scale))
        pil   = pil.resize((nw, nh), Image.LANCZOS)

        bg = Image.new("RGB", (cw, ch), (13, 13, 26))
        bg.paste(pil, ((cw - nw) // 2, (ch - nh) // 2))

        ph = ImageTk.PhotoImage(bg)
        canvas.delete("all")
        canvas.create_image(0, 0, anchor="nw", image=ph)
        setattr(self, ref_attr, ph)   # keep GC reference

    # ─── TOGGLE SKETCH PANEL ──────────────────────────────────────

    def _show_sketch_panel(self, show: bool):
        if show:
            self._div.pack(fill="x", padx=12, pady=2)
            self._sk_lbl.pack(anchor="w", padx=12, pady=(4,2))
            self.c_sketch.pack(fill="both", expand=True, padx=12, pady=(2,12))
        else:
            self._div.pack_forget()
            self._sk_lbl.pack_forget()
            self.c_sketch.pack_forget()

    # ─── ACTIONS ─────────────────────────────────────────────────

    def _load(self):
        path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Images","*.jpg;*.jpeg;*.png;*.bmp;*.tiff;*.webp")])
        if not path:
            return
        img = cv2.imread(path)
        if img is None:
            messagebox.showerror("Error", "Cannot open this image.")
            return
        self._orig = img
        self.status_var.set(
            f"Loaded: {os.path.basename(path)}  ({img.shape[1]}×{img.shape[0]} px)")
        self._draw(self.c_main, img, "_ph_main")

    def _parse(self):
        try:
            cols = int(self.cols_var.get())
            rows = int(self.rows_var.get())
            assert 1 <= cols <= 50 and 1 <= rows <= 50
        except Exception:
            messagebox.showerror("Invalid Input", "Columns and Rows must be between 1 and 50.")
            return None
        return dict(
            cols       = cols,
            rows       = rows,
            thick      = self.thick_var.get(),
            opacity    = self.opacity_var.get(),
            color      = self.color_var.get(),
            labels     = self.labels_var.get(),
            label_size = self.label_size_var.get(),
            sketch     = self.sketch_var.get(),
            blur       = self.sketch_blur_var.get(),
        )

    def _process(self):
        if self._orig is None:
            messagebox.showwarning("No Image", "Load an image first.")
            return
        s = self._parse()
        if s is None:
            return

        self.status_var.set("Processing…")
        self.update()

        # Grid is applied on the ORIGINAL full-resolution image — no canvas resize, no cropping
        orig_grid = apply_grid(self._orig,
                               cols=s["cols"], rows=s["rows"],
                               opacity=s["opacity"],
                               thickness=s["thick"],
                               color_mode=s["color"],
                               label_cells=s["labels"],
                               label_size=s["label_size"])

        self._processed = {"original_with_grid": orig_grid}
        self._draw(self.c_main, orig_grid, "_ph_main")

        show_sketch = s["sketch"]
        self._show_sketch_panel(show_sketch)

        if show_sketch:
            sketch  = create_sketch(self._orig, blur=s["blur"])
            sk_grid = apply_grid(sketch,
                                 cols=s["cols"], rows=s["rows"],
                                 opacity=s["opacity"],
                                 thickness=s["thick"],
                                 color_mode=s["color"],
                                 label_cells=s["labels"],
                                 label_size=s["label_size"])
            self._processed["sketch_with_grid"] = sk_grid
            self._draw(self.c_sketch, sk_grid, "_ph_sketch")

        self.status_var.set(
            f"Done  |  Grid {s['cols']}×{s['rows']}  "
            f"|  {self._orig.shape[1]}×{self._orig.shape[0]} px  "
            f"|  {'Sketch ON' if show_sketch else 'Sketch OFF'}")

    def _on_resize(self, event):
        if not self._processed:
            return
        if self._resize_job:
            self.after_cancel(self._resize_job)
        self._resize_job = self.after(150, self._redraw)

    def _redraw(self):
        orig = self._processed.get("original_with_grid")
        sk   = self._processed.get("sketch_with_grid")
        if orig is not None:
            self._draw(self.c_main, orig, "_ph_main")
        if sk is not None:
            self._draw(self.c_sketch, sk, "_ph_sketch")

    def _save_pngs(self):
        if not self._processed:
            messagebox.showwarning("Nothing to save", "Run Process first.")
            return
        folder = filedialog.askdirectory(title="Save To Folder")
        if not folder:
            return
        for name, img in self._processed.items():
            cv2.imwrite(os.path.join(folder, name + ".png"), img)
        messagebox.showinfo("Saved", f"Saved to:\n{folder}")
        self.status_var.set(f"Saved → {folder}")

    def _export_pdf(self):
        if not self._processed:
            messagebox.showwarning("Nothing to export", "Run Process first.")
            return
        path = filedialog.asksaveasfilename(
            title="Save PDF", defaultextension=".pdf",
            filetypes=[("PDF","*.pdf")])
        if not path:
            return
        try:
            export_pdf(self._processed, path)
            messagebox.showinfo("PDF Saved", f"Saved:\n{path}")
            self.status_var.set(f"PDF → {os.path.basename(path)}")
        except Exception as ex:
            messagebox.showerror("Export Failed", str(ex))


if __name__ == "__main__":
    App().mainloop()
