"""
==========================================================
  N-Queens Visualizer — Brute Force vs Backtracking
  Strategi Algoritma
==========================================================
  Simulasi interaktif perbandingan algoritma:
  1. Brute Force  : Coba SEMUA permutasi, cek satu per satu
  2. Backtracking : Coba per baris, mundur jika gagal (pruning)

  Dibuat dengan Tkinter (bawaan Python, tanpa install tambahan)
==========================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox
import time
import itertools
import threading

# ============================
# KONFIGURASI WARNA & UKURAN
# ============================
COLORS = {
    "bg_dark":       "#0f1423",
    "bg_card":       "#1a2035",
    "bg_surface":    "#212b45",
    "text_primary":  "#f1f5f9",
    "text_secondary":"#94a3b8",
    "text_muted":    "#64748b",
    "accent_purple": "#a855f7",
    "accent_blue":   "#3b82f6",
    "accent_green":  "#22c55e",
    "accent_red":    "#ef4444",
    "accent_amber":  "#f59e0b",
    "accent_cyan":   "#06b6d4",
    "board_light":   "#e2d1b5",
    "board_dark":    "#b58863",
    "board_safe":    "#4ade80",
    "board_conflict":"#f87171",
    "board_trying":  "#fbbf24",
    "queen_bg":      "#c084fc",
}

CELL_SIZE = 64
QUEEN_SYMBOL = "♛"


class NQueensVisualizer:
    """Kelas utama untuk visualisasi N-Queens."""

    def __init__(self, root):
        self.root = root
        self.root.title("N-Queens Visualizer — Brute Force vs Backtracking")
        self.root.configure(bg=COLORS["bg_dark"])
        self.root.resizable(True, True)

        # --- State ---
        self.N = 5
        self.algorithm = tk.StringVar(value="backtracking")
        self.speed = tk.IntVar(value=50)
        self.is_running = False
        self.should_stop = False

        # Statistik
        self.steps = 0
        self.backtracks = 0
        self.queens_placed = 0
        self.start_time = 0

        # Hasil untuk perbandingan
        self.results = {"backtracking": None, "bruteforce": None}

        # Referensi item canvas
        self.cell_rects = {}   # (row, col) -> rectangle_id
        self.cell_texts = {}   # (row, col) -> text_id
        self.board_state = {}  # (row, col) -> "queen" | None

        self._build_ui()
        self._draw_board()

    # ============================
    # UI BUILDING
    # ============================
    def _build_ui(self):
        """Bangun seluruh antarmuka."""

        # --- Judul ---
        header = tk.Frame(self.root, bg=COLORS["bg_dark"])
        header.pack(fill="x", padx=20, pady=(18, 4))

        tk.Label(
            header, text="N-Queens Visualizer",
            font=("Segoe UI", 22, "bold"), fg=COLORS["accent_purple"],
            bg=COLORS["bg_dark"],
        ).pack()
        tk.Label(
            header, text="Strategi Algoritma — Brute Force vs Backtracking",
            font=("Segoe UI", 10), fg=COLORS["text_secondary"],
            bg=COLORS["bg_dark"],
        ).pack()

        # --- Kontainer utama ---
        main_frame = tk.Frame(self.root, bg=COLORS["bg_dark"])
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Kolom kiri: kontrol + penjelasan
        left_col = tk.Frame(main_frame, bg=COLORS["bg_dark"], width=280)
        left_col.pack(side="left", fill="y", padx=(0, 14))
        left_col.pack_propagate(False)

        # Kolom tengah: papan catur
        center_col = tk.Frame(main_frame, bg=COLORS["bg_dark"])
        center_col.pack(side="left", fill="both", expand=True)

        # Kolom kanan: statistik + log
        right_col = tk.Frame(main_frame, bg=COLORS["bg_dark"], width=280)
        right_col.pack(side="left", fill="y", padx=(14, 0))
        right_col.pack_propagate(False)

        # ---- KOLOM KIRI: Kontrol ----
        self._build_controls(left_col)

        # ---- KOLOM TENGAH: Papan Catur ----
        self._build_board(center_col)

        # ---- KOLOM KANAN: Statistik & Log ----
        self._build_stats(right_col)

    def _build_controls(self, parent):
        """Panel kontrol di kolom kiri."""

        # Header
        self._section_header(parent, "⚙️  Pengaturan")

        card = tk.Frame(parent, bg=COLORS["bg_card"], highlightbackground=COLORS["bg_surface"],
                        highlightthickness=1)
        card.pack(fill="x", pady=(0, 10))

        inner = tk.Frame(card, bg=COLORS["bg_card"])
        inner.pack(fill="x", padx=14, pady=14)

        # Ukuran papan
        tk.Label(inner, text="UKURAN PAPAN (N)", font=("Segoe UI", 8, "bold"),
                 fg=COLORS["text_muted"], bg=COLORS["bg_card"]).pack(anchor="w")

        size_frame = tk.Frame(inner, bg=COLORS["bg_card"])
        size_frame.pack(fill="x", pady=(4, 12))

        self.size_var = tk.IntVar(value=5)
        self.size_label = tk.Label(size_frame, text="5", font=("Consolas", 16, "bold"),
                                    fg=COLORS["accent_purple"], bg=COLORS["bg_card"], width=3)
        self.size_label.pack(side="right")

        size_scale = tk.Scale(
            size_frame, from_=4, to=10, orient="horizontal",
            variable=self.size_var, command=self._on_size_change,
            bg=COLORS["bg_card"], fg=COLORS["text_primary"],
            troughcolor=COLORS["bg_surface"], highlightthickness=0,
            sliderrelief="flat", font=("Segoe UI", 8),
            showvalue=False, length=170
        )
        size_scale.pack(side="left", fill="x", expand=True)

        # Kecepatan
        tk.Label(inner, text="KECEPATAN ANIMASI", font=("Segoe UI", 8, "bold"),
                 fg=COLORS["text_muted"], bg=COLORS["bg_card"]).pack(anchor="w")

        speed_frame = tk.Frame(inner, bg=COLORS["bg_card"])
        speed_frame.pack(fill="x", pady=(4, 12))

        self.speed_label = tk.Label(speed_frame, text="50", font=("Consolas", 16, "bold"),
                                     fg=COLORS["accent_purple"], bg=COLORS["bg_card"], width=3)
        self.speed_label.pack(side="right")

        speed_scale = tk.Scale(
            speed_frame, from_=1, to=100, orient="horizontal",
            variable=self.speed, command=self._on_speed_change,
            bg=COLORS["bg_card"], fg=COLORS["text_primary"],
            troughcolor=COLORS["bg_surface"], highlightthickness=0,
            sliderrelief="flat", font=("Segoe UI", 8),
            showvalue=False, length=170
        )
        speed_scale.pack(side="left", fill="x", expand=True)

        # Pilih Algoritma
        tk.Label(inner, text="ALGORITMA", font=("Segoe UI", 8, "bold"),
                 fg=COLORS["text_muted"], bg=COLORS["bg_card"]).pack(anchor="w", pady=(4, 4))

        self.btn_bt = tk.Radiobutton(
            inner, text="🧠  Backtracking", variable=self.algorithm,
            value="backtracking", font=("Segoe UI", 10, "bold"),
            fg=COLORS["accent_green"], bg=COLORS["bg_card"],
            selectcolor=COLORS["bg_surface"], activebackground=COLORS["bg_card"],
            activeforeground=COLORS["accent_green"], indicatoron=0,
            relief="flat", bd=0, padx=10, pady=8, anchor="w",
        )
        self.btn_bt.pack(fill="x", pady=2)

        self.btn_bf = tk.Radiobutton(
            inner, text="💪  Brute Force", variable=self.algorithm,
            value="bruteforce", font=("Segoe UI", 10, "bold"),
            fg=COLORS["accent_amber"], bg=COLORS["bg_card"],
            selectcolor=COLORS["bg_surface"], activebackground=COLORS["bg_card"],
            activeforeground=COLORS["accent_amber"], indicatoron=0,
            relief="flat", bd=0, padx=10, pady=8, anchor="w",
        )
        self.btn_bf.pack(fill="x", pady=2)

        # Tombol aksi
        btn_frame = tk.Frame(inner, bg=COLORS["bg_card"])
        btn_frame.pack(fill="x", pady=(14, 0))

        self.btn_start = tk.Button(
            btn_frame, text="▶  Mulai", font=("Segoe UI", 11, "bold"),
            fg="white", bg=COLORS["accent_purple"], activebackground="#9333ea",
            activeforeground="white", relief="flat", bd=0, cursor="hand2",
            padx=16, pady=8, command=self._start,
        )
        self.btn_start.pack(fill="x", pady=(0, 6))

        self.btn_reset = tk.Button(
            btn_frame, text="↺  Reset", font=("Segoe UI", 10),
            fg=COLORS["text_secondary"], bg=COLORS["bg_surface"],
            activebackground=COLORS["bg_card"], activeforeground=COLORS["text_primary"],
            relief="flat", bd=0, cursor="hand2",
            padx=16, pady=6, command=self._reset,
        )
        self.btn_reset.pack(fill="x")

        # --- Penjelasan Algoritma ---
        self._section_header(parent, "📖  Penjelasan", top_pad=14)

        self.explain_frame = tk.Frame(parent, bg=COLORS["bg_card"],
                                       highlightbackground=COLORS["bg_surface"], highlightthickness=1)
        self.explain_frame.pack(fill="both", expand=True)

        self.explain_text = tk.Text(
            self.explain_frame, wrap="word", font=("Segoe UI", 9),
            fg=COLORS["text_secondary"], bg=COLORS["bg_card"],
            relief="flat", bd=0, padx=12, pady=12, state="disabled",
            height=12,
        )
        self.explain_text.pack(fill="both", expand=True)
        self._update_explanation()

        self.algorithm.trace_add("write", lambda *_: self._update_explanation())

    def _build_board(self, parent):
        """Papan catur di kolom tengah."""

        # Status
        status_frame = tk.Frame(parent, bg=COLORS["bg_dark"])
        status_frame.pack(pady=(0, 6))

        self.status_label = tk.Label(
            status_frame, text="♛  Siap", font=("Segoe UI", 12, "bold"),
            fg=COLORS["accent_blue"], bg=COLORS["bg_dark"],
        )
        self.status_label.pack()

        # Canvas untuk papan
        canvas_size = CELL_SIZE * 10 + 4  # max N=10
        self.canvas = tk.Canvas(
            parent, width=canvas_size, height=canvas_size,
            bg=COLORS["bg_dark"], highlightthickness=0,
        )
        self.canvas.pack(expand=True)

        # Legend
        legend_frame = tk.Frame(parent, bg=COLORS["bg_dark"])
        legend_frame.pack(pady=(8, 0))

        legends = [
            (COLORS["board_safe"],     "Aman"),
            (COLORS["board_conflict"], "Konflik"),
            (COLORS["board_trying"],   "Dicoba"),
            (COLORS["queen_bg"],       "Ratu"),
        ]
        for color, label in legends:
            f = tk.Frame(legend_frame, bg=COLORS["bg_dark"])
            f.pack(side="left", padx=8)
            tk.Canvas(f, width=12, height=12, bg=color, highlightthickness=0).pack(side="left", padx=(0, 4))
            tk.Label(f, text=label, font=("Segoe UI", 8), fg=COLORS["text_muted"],
                     bg=COLORS["bg_dark"]).pack(side="left")

    def _build_stats(self, parent):
        """Panel statistik & log di kolom kanan."""

        self._section_header(parent, "📊  Statistik")

        stats_card = tk.Frame(parent, bg=COLORS["bg_card"],
                               highlightbackground=COLORS["bg_surface"], highlightthickness=1)
        stats_card.pack(fill="x", pady=(0, 10))

        self.stat_labels = {}
        stats = [
            ("steps",      "📊  Langkah",    "0"),
            ("backtracks", "↩️  Backtrack",   "0"),
            ("queens",     "♛  Ratu Aktif",  "0"),
            ("time",       "⏱️  Waktu",       "0 ms"),
        ]

        for key, label, default in stats:
            row = tk.Frame(stats_card, bg=COLORS["bg_card"])
            row.pack(fill="x", padx=14, pady=6)

            tk.Label(row, text=label, font=("Segoe UI", 9),
                     fg=COLORS["text_muted"], bg=COLORS["bg_card"]).pack(side="left")

            val_label = tk.Label(row, text=default, font=("Consolas", 13, "bold"),
                                  fg=COLORS["text_primary"], bg=COLORS["bg_card"])
            val_label.pack(side="right")
            self.stat_labels[key] = val_label

        # --- Log ---
        self._section_header(parent, "📋  Log Eksekusi", top_pad=6)

        log_card = tk.Frame(parent, bg=COLORS["bg_card"],
                             highlightbackground=COLORS["bg_surface"], highlightthickness=1)
        log_card.pack(fill="both", expand=True)

        self.log_text = tk.Text(
            log_card, wrap="word", font=("Consolas", 8),
            fg=COLORS["text_muted"], bg=COLORS["bg_card"],
            relief="flat", bd=0, padx=10, pady=10, state="disabled",
        )
        scrollbar = tk.Scrollbar(log_card, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.log_text.pack(side="left", fill="both", expand=True)

        # Konfigurasi tag warna log
        self.log_text.tag_configure("info",      foreground=COLORS["accent_blue"])
        self.log_text.tag_configure("try",       foreground=COLORS["accent_amber"])
        self.log_text.tag_configure("place",     foreground=COLORS["accent_green"])
        self.log_text.tag_configure("conflict",  foreground=COLORS["accent_red"])
        self.log_text.tag_configure("backtrack", foreground="#f472b6")
        self.log_text.tag_configure("solution",  foreground=COLORS["accent_purple"],
                                     font=("Consolas", 9, "bold"))

        # --- Perbandingan ---
        self._section_header(parent, "🏆  Perbandingan", top_pad=6)

        self.cmp_card = tk.Frame(parent, bg=COLORS["bg_card"],
                                  highlightbackground=COLORS["accent_purple"], highlightthickness=1)
        self.cmp_card.pack(fill="x")

        self.cmp_text = tk.Label(
            self.cmp_card, text="Jalankan kedua algoritma\nuntuk melihat perbandingan",
            font=("Segoe UI", 9), fg=COLORS["text_muted"],
            bg=COLORS["bg_card"], justify="center", pady=14, padx=10, wraplength=240,
        )
        self.cmp_text.pack()

    def _section_header(self, parent, text, top_pad=0):
        """Label header untuk setiap section."""
        tk.Label(
            parent, text=text, font=("Segoe UI", 10, "bold"),
            fg=COLORS["text_primary"], bg=COLORS["bg_dark"], anchor="w",
        ).pack(fill="x", pady=(top_pad, 4))

    # ============================
    # PAPAN CATUR
    # ============================
    def _draw_board(self):
        """Gambar ulang papan catur sesuai ukuran N."""
        self.canvas.delete("all")
        self.cell_rects.clear()
        self.cell_texts.clear()
        self.board_state.clear()

        n = self.N
        board_px = CELL_SIZE * n
        offset_x = (self.canvas.winfo_reqwidth() - board_px) // 2
        offset_y = (self.canvas.winfo_reqheight() - board_px) // 2

        # Border
        self.canvas.create_rectangle(
            offset_x - 2, offset_y - 2,
            offset_x + board_px + 2, offset_y + board_px + 2,
            outline=COLORS["bg_surface"], width=3,
        )

        for row in range(n):
            for col in range(n):
                x1 = offset_x + col * CELL_SIZE
                y1 = offset_y + row * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                color = COLORS["board_light"] if (row + col) % 2 == 0 else COLORS["board_dark"]

                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
                text = self.canvas.create_text(
                    (x1 + x2) // 2, (y1 + y2) // 2,
                    text="", font=("Segoe UI", int(CELL_SIZE * 0.5), "bold"),
                    fill="#1a1a2e",
                )

                self.cell_rects[(row, col)] = rect
                self.cell_texts[(row, col)] = text
                self.board_state[(row, col)] = None

        # Nomor baris & kolom
        for i in range(n):
            # Nomor baris (kiri)
            self.canvas.create_text(
                offset_x - 14, offset_y + i * CELL_SIZE + CELL_SIZE // 2,
                text=str(i + 1), font=("Consolas", 9), fill=COLORS["text_muted"],
            )
            # Nomor kolom (atas)
            self.canvas.create_text(
                offset_x + i * CELL_SIZE + CELL_SIZE // 2, offset_y - 14,
                text=str(i + 1), font=("Consolas", 9), fill=COLORS["text_muted"],
            )

    def _set_cell_color(self, row, col, color):
        """Ubah warna sel."""
        self.canvas.itemconfig(self.cell_rects[(row, col)], fill=color)

    def _reset_cell_color(self, row, col):
        """Kembalikan warna asli sel."""
        original = COLORS["board_light"] if (row + col) % 2 == 0 else COLORS["board_dark"]
        self.canvas.itemconfig(self.cell_rects[(row, col)], fill=original)

    def _place_queen(self, row, col):
        """Tempatkan ratu secara visual."""
        self._set_cell_color(row, col, COLORS["queen_bg"])
        self.canvas.itemconfig(self.cell_texts[(row, col)], text=QUEEN_SYMBOL)
        self.board_state[(row, col)] = "queen"

    def _remove_queen(self, row, col):
        """Hapus ratu secara visual."""
        self._reset_cell_color(row, col)
        self.canvas.itemconfig(self.cell_texts[(row, col)], text="")
        self.board_state[(row, col)] = None

    def _clear_all(self):
        """Bersihkan semua ratu dan warna dari papan."""
        for row in range(self.N):
            for col in range(self.N):
                self._reset_cell_color(row, col)
                self.canvas.itemconfig(self.cell_texts[(row, col)], text="")
                self.board_state[(row, col)] = None

    def _highlight_attack_zones(self, queens):
        """Tandai zona serangan dari semua ratu yang sudah ditempatkan."""
        # Reset dulu
        for row in range(self.N):
            for col in range(self.N):
                if self.board_state.get((row, col)) != "queen":
                    self._reset_cell_color(row, col)

        for qr, qc in queens:
            for i in range(self.N):
                if i != qc and self.board_state.get((qr, i)) != "queen":
                    self._dim_cell(qr, i)
                if i != qr and self.board_state.get((i, qc)) != "queen":
                    self._dim_cell(i, qc)
            for d in range(1, self.N):
                for dr, dc in [(d, d), (d, -d), (-d, d), (-d, -d)]:
                    nr, nc = qr + dr, qc + dc
                    if 0 <= nr < self.N and 0 <= nc < self.N:
                        if self.board_state.get((nr, nc)) != "queen":
                            self._dim_cell(nr, nc)

    def _dim_cell(self, row, col):
        """Beri warna redup untuk zona serangan."""
        base = COLORS["board_light"] if (row + col) % 2 == 0 else COLORS["board_dark"]
        # Gelapkan sedikit
        self._set_cell_color(row, col, self._darken(base, 0.7))

    @staticmethod
    def _darken(hex_color, factor):
        """Gelapkan warna hex."""
        hex_color = hex_color.lstrip("#")
        r = int(int(hex_color[0:2], 16) * factor)
        g = int(int(hex_color[2:4], 16) * factor)
        b = int(int(hex_color[4:6], 16) * factor)
        return f"#{r:02x}{g:02x}{b:02x}"

    # ============================
    # LOGGING & STATS
    # ============================
    def _add_log(self, message, tag="info"):
        """Tambah entri log."""
        self.log_text.configure(state="normal")
        prefix = f"[{self.steps:>5}] "
        self.log_text.insert("end", prefix + message + "\n", tag)
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def _clear_log(self):
        """Bersihkan log."""
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")

    def _update_stats(self):
        """Update label statistik."""
        self.stat_labels["steps"].config(text=f"{self.steps:,}")
        self.stat_labels["backtracks"].config(text=f"{self.backtracks:,}")
        self.stat_labels["queens"].config(text=str(self.queens_placed))
        elapsed = (time.time() - self.start_time) * 1000
        if elapsed < 1000:
            self.stat_labels["time"].config(text=f"{elapsed:.0f} ms")
        else:
            self.stat_labels["time"].config(text=f"{elapsed / 1000:.2f} s")

    def _set_status(self, text, color):
        """Update label status."""
        self.status_label.config(text=text, fg=color)

    def _get_delay(self):
        """Hitung delay animasi dari slider kecepatan (dalam detik)."""
        sp = self.speed.get()
        return max(0.005, 0.8 - (sp - 1) * 0.008)

    # ============================
    # PENJELASAN ALGORITMA
    # ============================
    def _update_explanation(self):
        """Update teks penjelasan sesuai algoritma yang dipilih."""
        self.explain_text.configure(state="normal")
        self.explain_text.delete("1.0", "end")

        if self.algorithm.get() == "backtracking":
            text = (
                "🧠 BACKTRACKING\n\n"
                "Cara Kerja:\n"
                "1. Tempatkan ratu di kolom pertama\n"
                "   baris saat ini\n"
                "2. Cek apakah posisi aman\n"
                "3. Aman → lanjut ke baris berikutnya\n"
                "4. Tidak aman → coba kolom berikutnya\n"
                "5. Semua kolom gagal → BACKTRACK!\n"
                "   (mundur ke baris sebelumnya)\n\n"
                "Kompleksitas: O(N!)\n"
                "Pruning: Ya ✓ (lebih efisien)"
            )
        else:
            text = (
                "💪 BRUTE FORCE\n\n"
                "Cara Kerja:\n"
                "1. Generate SEMUA permutasi\n"
                "   penempatan N ratu\n"
                "2. Untuk setiap permutasi,\n"
                "   tempatkan semua ratu di papan\n"
                "3. Cek apakah ada konflik diagonal\n"
                "4. Valid → solusi ditemukan!\n"
                "5. Tidak → coba permutasi berikutnya\n\n"
                "Kompleksitas: O(N! × N)\n"
                "Pruning: Tidak ✗ (semua dicoba)"
            )

        self.explain_text.insert("1.0", text)
        self.explain_text.configure(state="disabled")

    # ============================
    # EVENT HANDLERS
    # ============================
    def _on_size_change(self, val):
        """Saat slider ukuran berubah."""
        self.N = int(val)
        self.size_label.config(text=str(self.N))
        if not self.is_running:
            self._draw_board()

    def _on_speed_change(self, val):
        """Saat slider kecepatan berubah."""
        self.speed_label.config(text=str(int(float(val))))

    def _start(self):
        """Mulai visualisasi di thread terpisah."""
        if self.is_running:
            return

        self.is_running = True
        self.should_stop = False
        self.steps = 0
        self.backtracks = 0
        self.queens_placed = 0
        self.start_time = time.time()

        self.btn_start.config(state="disabled", text="⏳ Menjalankan...")
        self._draw_board()
        self._clear_log()
        self._update_stats()
        self._set_status("⏳ Menjalankan...", COLORS["accent_amber"])

        algo = self.algorithm.get()
        self._add_log(f"Memulai {'Backtracking' if algo == 'backtracking' else 'Brute Force'} untuk {self.N}-Queens", "info")
        self._add_log(f"Ukuran papan: {self.N}×{self.N}", "info")

        # Jalankan di thread terpisah agar UI tidak freeze
        thread = threading.Thread(target=self._run_algorithm, daemon=True)
        thread.start()

    def _reset(self):
        """Reset visualisasi."""
        self.should_stop = True
        self.is_running = False
        self.steps = 0
        self.backtracks = 0
        self.queens_placed = 0

        self._draw_board()
        self._update_stats()
        self.stat_labels["time"].config(text="0 ms")
        self._set_status("♛  Siap", COLORS["accent_blue"])
        self.btn_start.config(state="normal", text="▶  Mulai")
        self._clear_log()
        self._add_log("Visualisasi direset. Klik Mulai untuk memulai.", "info")

    # ============================
    # ALGORITMA
    # ============================
    def _run_algorithm(self):
        """Jalankan algoritma sesuai pilihan."""
        algo = self.algorithm.get()

        if algo == "backtracking":
            board = [-1] * self.N
            found = self._backtrack(board, 0)
        else:
            found = self._brute_force()

        elapsed = (time.time() - self.start_time) * 1000

        if not self.should_stop:
            # Simpan hasil
            self.results[algo] = {
                "steps": self.steps,
                "backtracks": self.backtracks,
                "time": elapsed,
                "found": found,
            }

            if not found:
                self.root.after(0, lambda: self._set_status(
                    "✗ Tidak ada solusi", COLORS["accent_red"]))
                self.root.after(0, lambda: self._add_log(
                    f"Tidak ada solusi untuk {self.N}-Queens", "conflict"))

            # Update perbandingan
            if self.results["backtracking"] and self.results["bruteforce"]:
                self.root.after(0, self._show_comparison)

        self.is_running = False
        self.root.after(0, lambda: self.btn_start.config(state="normal", text="▶  Mulai"))

    def _safe_update(self, func, *args):
        """Jalankan fungsi UI update dari thread utama secara sinkron."""
        if self.should_stop:
            return
        event = threading.Event()
        def wrapped():
            func(*args)
            event.set()
        self.root.after(0, wrapped)
        event.wait(timeout=2)

    def _sleep(self, seconds):
        """Sleep yang bisa di-interrupt."""
        time.sleep(seconds)

    # --- Backtracking ---
    def _backtrack(self, board, row):
        """Algoritma Backtracking rekursif."""
        if self.should_stop:
            return False

        if row == self.N:
            # Solusi ditemukan!
            self._safe_update(self._set_status, "✓ Solusi Ditemukan!", COLORS["accent_green"])
            placement = [str(board[i] + 1) for i in range(self.N)]
            self._safe_update(self._add_log,
                f"🎉 SOLUSI DITEMUKAN! Kolom: [{', '.join(placement)}]", "solution")
            return True

        for col in range(self.N):
            if self.should_stop:
                return False

            self.steps += 1
            self._safe_update(self._update_stats)

            # Highlight sedang dicoba
            self._safe_update(self._set_cell_color, row, col, COLORS["board_trying"])
            self._safe_update(self._add_log,
                f"Mencoba baris {row + 1}, kolom {col + 1}", "try")

            self._sleep(self._get_delay())

            if self._is_safe(board, row, col):
                # Tempatkan ratu
                board[row] = col
                self.queens_placed += 1
                self._safe_update(self._update_stats)
                self._safe_update(self._place_queen, row, col)

                # Tunjukkan zona serangan
                queens = [(i, board[i]) for i in range(row + 1) if board[i] != -1]
                self._safe_update(self._highlight_attack_zones, queens)

                self._safe_update(self._add_log,
                    f"✓ Ratu di baris {row + 1}, kolom {col + 1} (aman)", "place")

                self._sleep(self._get_delay())

                # Rekursi ke baris berikutnya
                if self._backtrack(board, row + 1):
                    return True

                # Backtrack!
                if self.should_stop:
                    return False

                self.backtracks += 1
                board[row] = -1
                self.queens_placed -= 1
                self._safe_update(self._update_stats)
                self._safe_update(self._remove_queen, row, col)

                self._safe_update(self._add_log,
                    f"↩ BACKTRACK dari baris {row + 1}, kolom {col + 1}", "backtrack")

                # Update zona serangan
                queens = [(i, board[i]) for i in range(row) if board[i] != -1]
                self._safe_update(self._highlight_attack_zones, queens)

                self._sleep(self._get_delay() * 0.5)
            else:
                # Konflik
                self._safe_update(self._set_cell_color, row, col, COLORS["board_conflict"])
                self._safe_update(self._add_log,
                    f"✗ Konflik di baris {row + 1}, kolom {col + 1}", "conflict")

                self._sleep(self._get_delay() * 0.4)
                self._safe_update(self._reset_cell_color, row, col)

        return False

    # --- Brute Force ---
    def _brute_force(self):
        """Algoritma Brute Force — coba semua permutasi."""
        n = self.N
        cols = list(range(n))

        self._safe_update(self._add_log,
            f"Generating semua {self._factorial(n)} permutasi...", "info")

        for perm in itertools.permutations(cols):
            if self.should_stop:
                return False

            self.steps += 1
            self._safe_update(self._update_stats)

            # Bersihkan papan
            self._safe_update(self._clear_all)

            perm_str = ", ".join(str(c + 1) for c in perm)
            self._safe_update(self._add_log,
                f"Mencoba permutasi: [{perm_str}]", "try")

            # Tempatkan semua ratu
            for row in range(n):
                if self.should_stop:
                    return False
                self._safe_update(self._set_cell_color, row, perm[row], COLORS["board_trying"])
                self._safe_update(self._place_queen, row, perm[row])
                self.queens_placed = row + 1
                self._safe_update(self._update_stats)
                self._sleep(self._get_delay() / n)

            self._sleep(self._get_delay() * 0.6)

            # Cek apakah valid
            if self._is_valid_arrangement(perm):
                # Tandai semua sebagai berhasil
                for row in range(n):
                    self._safe_update(self._set_cell_color, row, perm[row], COLORS["board_safe"])

                self._safe_update(self._set_status, "✓ Solusi Ditemukan!", COLORS["accent_green"])
                self._safe_update(self._add_log,
                    f"🎉 SOLUSI DITEMUKAN! Kolom: [{perm_str}]", "solution")
                return True
            else:
                self.backtracks += 1
                self._safe_update(self._update_stats)

                # Highlight konflik
                for i in range(n):
                    for j in range(i + 1, n):
                        if abs(perm[i] - perm[j]) == abs(i - j):
                            self._safe_update(self._set_cell_color, i, perm[i], COLORS["board_conflict"])
                            self._safe_update(self._set_cell_color, j, perm[j], COLORS["board_conflict"])

                self._safe_update(self._add_log,
                    f"✗ Konflik diagonal ditemukan", "conflict")

                self._sleep(self._get_delay() * 0.4)

                # Bersihkan
                self._safe_update(self._clear_all)
                self.queens_placed = 0
                self._safe_update(self._update_stats)

        return False

    # ============================
    # HELPER FUNCTIONS
    # ============================
    @staticmethod
    def _is_safe(board, row, col):
        """Cek apakah posisi (row, col) aman dari serangan ratu lain."""
        for i in range(row):
            # Cek kolom sama
            if board[i] == col:
                return False
            # Cek diagonal
            if abs(board[i] - col) == abs(i - row):
                return False
        return True

    @staticmethod
    def _is_valid_arrangement(perm):
        """Cek apakah permutasi valid (tidak ada konflik diagonal)."""
        n = len(perm)
        for i in range(n):
            for j in range(i + 1, n):
                if abs(perm[i] - perm[j]) == abs(i - j):
                    return False
        return True

    @staticmethod
    def _factorial(n):
        """Hitung n!"""
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    # ============================
    # PERBANDINGAN HASIL
    # ============================
    def _show_comparison(self):
        """Tampilkan perbandingan kedua algoritma."""
        bt = self.results["backtracking"]
        bf = self.results["bruteforce"]

        if not bt or not bf:
            return

        ratio = bf["steps"] / bt["steps"] if bt["steps"] > 0 else float("inf")

        text = (
            f"🧠 Backtracking  vs  💪 Brute Force\n"
            f"{'─' * 38}\n"
            f"Langkah:    {bt['steps']:>8,}  vs  {bf['steps']:>8,}\n"
            f"Backtrack:  {bt['backtracks']:>8,}  vs  {bf['backtracks']:>8,}\n"
            f"Waktu:      {bt['time']:>7.0f}ms  vs  {bf['time']:>7.0f}ms\n"
            f"{'─' * 38}\n"
            f"🏆 Backtracking {ratio:.1f}x lebih\n"
            f"   sedikit langkah!"
        )

        self.cmp_text.config(
            text=text, fg=COLORS["accent_purple"],
            font=("Consolas", 8, "bold"), justify="left",
        )


# ============================
# MAIN
# ============================
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1050x680")
    root.minsize(900, 600)

    app = NQueensVisualizer(root)
    root.mainloop()
