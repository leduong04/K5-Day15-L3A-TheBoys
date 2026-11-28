"""Tk interface for the Socratic Debugger, with a terminal fallback."""
import keyword
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def _run_terminal():
    import tracing
    from agent import answer

    print("Bản chạy thử — dán đề/code/test theo nhãn. Thoát: Ctrl+C.")
    while True:
        try:
            text = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if not text:
            continue
        tracing.begin("app")
        try:
            result = answer(text)
        except Exception as exc:
            summary, _ = tracing.end()
            print("[lỗi] %s: %s" % (type(exc).__name__, exc))
            continue
        summary, _ = tracing.end()
        print(result.get("output", ""))
        print("   (model: %s · gọi model %d lần · công cụ %d lần · token vào %d / ra %d)"
              % (", ".join(summary["models"]) or "—", summary["model_calls"], summary["tool_calls"],
                 summary["tokens_in"], summary["tokens_out"]))


# Tên 4 cấp — khớp spec.md §4
CAP = {1: "Quan sát", 2: "Định hướng", 3: "Gợi ý khái niệm", 4: "Ví dụ tương tự"}
MO_TA_CAP = {
    1: "So kết quả thực tế với mong đợi — chưa chỉ vào code.",
    2: "Chỉ vào một vùng / dòng / biến để bạn tự theo dõi.",
    3: "Nhắc một khái niệm Python liên quan tới lỗi.",
    4: "Một bài khác có cùng loại lỗi để bạn so sánh.",
}
QUA_CAP_UI = ("Bạn đã đi qua cả 4 cấp gợi ý. Hãy mang đề, code và những gì đã thử tới lab coach — "
              "thử giải thích lại từng bước cho người khác nghe nhé.")

# Bài mẫu để demo — lấy từ data/labs.json (LAB-01, dữ liệu tự soạn)
VI_DU = {
    "de": "Viết hàm tong_chan(n) trả về tổng các số chẵn từ 1 đến n (tính cả n).",
    "code": "def tong_chan(n):\n    s = 0\n    for i in range(1, n):\n        if i % 2 == 0:\n            s += i\n    return s",
    "test": "tong_chan(10) ra 20, mong đợi 30",
}

# Bộ màu xanh navy
MAU = {
    "nen": "#EEF1F7", "the": "#FFFFFF", "bong": "#DCE1EB", "vien": "#D5DBE7", "chu": "#1F2937",
    "phu": "#6B7280", "header": "#1E2A78", "header_phu": "#B9C3EE",
    "chinh": "#1E3A8A", "chinh_hover": "#172E6E", "chinh_tat": "#A9B5D6",
    "nhat": "#DCE7FB", "nhat_hover": "#C9D9F7", "nhat_chu": "#1E3A8A", "nhat_tat": "#EEF1F7",
    "buoc_cho": "#E2E6EE", "buoc_xong": "#8EA2DC", "mo_ta": "#EEF3FD",
    "code_nen": "#1E2230", "code_chu": "#E6E8EE", "so_dong": "#5C6372", "loi": "#DC2626",
}
MAU_CU_PHAP = [   # (tag, màu, regex) — tô màu code học viên cho dễ đọc
    ("so", "#FDBA74", r"\b\d+(\.\d+)?\b"),
    ("tu_khoa", "#F472B6", r"\b(%s)\b" % "|".join(keyword.kwlist)),
    ("co_san", "#93C5FD", r"\b(print|range|len|sum|min|max|abs|int|float|str|list|dict|set|input|round|sorted|enumerate)\b"),
    ("ten_ham", "#86EFAC", r"(?<=\bdef )\w+|(?<=\bclass )\w+"),
    ("chuoi", "#D9F99D", r"\"[^\"\n]*\"|'[^'\n]*'"),
    ("chu_thich", "#7C8496", r"#[^\n]*"),
]


def _bo_goc(c, x1, y1, x2, y2, r, **kw):
    """Hình chữ nhật bo góc trên Canvas (polygon smooth)."""
    r = max(0, min(r, (x2 - x1) / 2, (y2 - y1) / 2))
    pts = [x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r, x2, y2 - r, x2, y2,
           x2 - r, y2, x1 + r, y2, x1, y2, x1, y2 - r, x1, y1 + r, x1, y1]
    return c.create_polygon(pts, smooth=True, **kw)


def _run_gui():
    import queue
    import threading
    import tkinter as tk
    from tkinter import font as tkfont
    from tkinter import messagebox

    import tracing
    from agent import answer

    ui = "Segoe UI" if sys.platform == "win32" else "Helvetica"
    mono = "Consolas" if sys.platform == "win32" else "Menlo"

    class Khung(tk.Canvas):
        """Khung bo góc, có thể có bóng. Đặt widget con vào self.trong.
        tu_cao=True: chiều cao theo nội dung; False: giãn theo chỗ được cấp."""

        def __init__(self, parent, nen_ngoai, fill, vien=None, r=14, pad=16, bong=None, tu_cao=True):
            super().__init__(parent, bg=nen_ngoai, highlightthickness=0, bd=0, width=10, height=10)
            self.fill, self.vien, self.r, self.pad, self.bong, self.tu_cao = fill, vien, r, pad, bong, tu_cao
            self.lech = 3 if bong else 0
            self.trong = tk.Frame(self, bg=fill)
            self._win = self.create_window(pad, pad, window=self.trong, anchor="nw")
            self.bind("<Configure>", self._ve)
            if tu_cao:   # cao theo nội dung — đo reqheight vì khung con chưa hiện thì không có sự kiện <Configure>
                self.trong.bind("<Configure>", lambda e: self._ve())
                self.after_idle(self._ve)

        def _ve(self, _e=None):
            if self.tu_cao:
                can = self.trong.winfo_reqheight() + 2 * self.pad + self.lech
                if int(self["height"]) != can:
                    self.configure(height=can)
            w, h = self.winfo_width(), self.winfo_height()
            self.delete("nen")
            if self.bong:
                _bo_goc(self, 1, 1 + self.lech, w - 1, h - 1, self.r, fill=self.bong, outline="", tags="nen")
            _bo_goc(self, 1, 1, w - 1, h - 1 - self.lech, self.r, fill=self.fill,
                    outline=self.vien or self.fill, tags="nen")
            self.tag_lower("nen")
            kw = {"width": max(1, w - 2 * self.pad)}
            if not self.tu_cao:
                kw["height"] = max(1, h - 2 * self.pad - self.lech)
            self.itemconfigure(self._win, **kw)

        def doi_vien(self, mau):
            self.vien = mau
            self._ve()

    class Nut(tk.Canvas):
        """Nút bo góc, có hover và trạng thái tắt."""
        KIEU = {"chinh": ("chinh", "chinh_hover", "chinh_tat", "#FFFFFF", "#FFFFFF"),
                "nhat": ("nhat", "nhat_hover", "nhat_tat", "nhat_chu", "phu")}

        def __init__(self, parent, text, cmd, nen_ngoai, kieu="chinh"):
            f = tkfont.Font(family=ui, size=10, weight="bold")
            w, h = f.measure(text) + 40, 40
            super().__init__(parent, width=w, height=h, bg=nen_ngoai, highlightthickness=0, bd=0, cursor="hand2")
            self.text, self.cmd, self.f, self.bat = text, cmd, f, True
            k = self.KIEU[kieu]
            self.mau = {"nen": MAU[k[0]], "hover": MAU[k[1]], "tat": MAU[k[2]],
                        "chu": MAU.get(k[3], k[3]), "chu_tat": MAU.get(k[4], k[4]) if kieu == "nhat" else "#E8ECF6"}
            self._ve(self.mau["nen"])
            self.bind("<Button-1>", lambda e: self.bat and self.cmd())
            self.bind("<Enter>", lambda e: self.bat and self._ve(self.mau["hover"]))
            self.bind("<Leave>", lambda e: self._ve(self.mau["nen"] if self.bat else self.mau["tat"]))

        def _ve(self, nen):
            self.delete("all")
            w, h = int(self["width"]), int(self["height"])
            _bo_goc(self, 0, 0, w, h, 10, fill=nen, outline="")
            self.create_text(w / 2, h / 2, text=self.text, font=self.f,
                             fill=self.mau["chu"] if self.bat else self.mau["chu_tat"])

        def dat_bat(self, bat):
            self.bat = bat
            self.configure(cursor="hand2" if bat else "arrow")
            self._ve(self.mau["nen"] if bat else self.mau["tat"])

    class ThanhBuoc(tk.Canvas):
        """Thanh mảnh bo tròn hai đầu cho từng cấp."""

        def __init__(self, parent):
            super().__init__(parent, height=8, bg=MAU["the"], highlightthickness=0, bd=0, width=10)
            self.mau = MAU["buoc_cho"]
            self.bind("<Configure>", lambda e: self._ve())

        def _ve(self):
            self.delete("all")
            w = self.winfo_width()
            self.create_line(4, 4, max(5, w - 4), 4, width=6, capstyle="round", fill=self.mau)

        def dat_mau(self, mau):
            self.mau = mau
            self._ve()

    root = tk.Tk()
    root.title("Socratic Debugger · Python Mini Lab")
    root.geometry("1230x850")
    root.minsize(1000, 700)
    root.configure(bg=MAU["nen"])
    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)

    # ------------------------------------------------------------ header
    header = tk.Frame(root, bg=MAU["header"], padx=28, pady=16)
    header.grid(row=0, column=0, sticky="ew")
    tk.Label(header, text="Socratic Debugger", bg=MAU["header"], fg="white",
             font=(ui, 20, "bold")).pack(side="left")
    tk.Label(header, text="Không đưa đáp án — chỉ hỏi đúng một câu để bạn tự tìm ra lỗi",
             bg=MAU["header"], fg=MAU["header_phu"], font=(ui, 10)).pack(side="left", padx=18, pady=(8, 0))

    body = tk.Frame(root, bg=MAU["nen"], padx=20, pady=16)
    body.grid(row=1, column=0, sticky="nsew")
    body.columnconfigure(0, weight=1, uniform="c")
    body.columnconfigure(1, weight=1, uniform="c")
    body.rowconfigure(0, weight=1)

    def nhan(parent, text):
        tk.Label(parent, text=text, bg=MAU["the"], fg=MAU["chu"], font=(ui, 10, "bold")).pack(anchor="w", pady=(12, 6))

    def o_nhap(parent, height, gian=False):
        k = Khung(parent, MAU["the"], MAU["the"], vien=MAU["vien"], r=10, pad=8, tu_cao=not gian)
        t = tk.Text(k.trong, height=height, wrap="word", undo=True, relief="flat", bd=0, highlightthickness=0,
                    bg=MAU["the"], fg=MAU["chu"], font=(ui, 10), insertbackground=MAU["chinh"], padx=4, pady=2)
        t.pack(fill="both", expand=True)
        t.bind("<FocusIn>", lambda e: k.doi_vien(MAU["chinh"]))
        t.bind("<FocusOut>", lambda e: k.doi_vien(MAU["vien"]))
        k.pack(fill="both" if gian else "x", expand=gian)
        return t

    # ------------------------------------------------------------ cột trái: bài của bạn
    trai_k = Khung(body, MAU["nen"], MAU["the"], r=16, pad=22, bong=MAU["bong"], tu_cao=False)
    trai_k.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
    trai = trai_k.trong

    top = tk.Frame(trai, bg=MAU["the"])
    top.pack(fill="x")
    tk.Label(top, text="Bài của bạn", bg=MAU["the"], fg=MAU["chu"], font=(ui, 14, "bold")).pack(side="left")

    nhan(trai, "Đề bài")
    de = o_nhap(trai, 3)

    nhan(trai, "Code đang chạy sai")
    code_k = Khung(trai, MAU["the"], MAU["code_nen"], r=12, pad=12, tu_cao=False)
    code_k.pack(fill="both", expand=True)
    so_dong = tk.Text(code_k.trong, width=3, bg=MAU["code_nen"], fg=MAU["so_dong"], relief="flat", bd=0,
                      highlightthickness=0, font=(mono, 11), padx=4, pady=2, takefocus=0, cursor="arrow")
    so_dong.tag_configure("phai", justify="right")
    so_dong.pack(side="left", fill="y")
    code = tk.Text(code_k.trong, wrap="none", undo=True, relief="flat", bd=0, highlightthickness=0,
                   bg=MAU["code_nen"], fg=MAU["code_chu"], insertbackground="white", font=(mono, 11),
                   padx=10, pady=2, height=10, selectbackground="#3B4466")
    code.pack(side="left", fill="both", expand=True)
    for tag, mau, _ in MAU_CU_PHAP:
        code.tag_configure(tag, foreground=mau)
    code.configure(yscrollcommand=lambda a, b: so_dong.yview_moveto(a))

    def cap_nhat_code(_e=None):
        noi_dung = code.get("1.0", "end-1c")
        for tag, _, mau_re in MAU_CU_PHAP:
            code.tag_remove(tag, "1.0", "end")
            for m in re.finditer(mau_re, noi_dung):
                code.tag_add(tag, "1.0+%dc" % m.start(), "1.0+%dc" % m.end())
        n = int(code.index("end-1c").split(".")[0])
        so_dong.configure(state="normal")
        so_dong.delete("1.0", "end")
        so_dong.insert("1.0", "\n".join(str(i) for i in range(1, max(n, 10) + 1)), "phai")
        so_dong.configure(state="disabled")
        so_dong.yview_moveto(code.yview()[0])

    code.bind("<KeyRelease>", cap_nhat_code)
    code.bind("<<Paste>>", lambda e: root.after_idle(cap_nhat_code))
    code.bind("<Tab>", lambda e: (code.insert("insert", "    "), "break")[1])

    nhan(trai, "Test  ·  input, ra kết quả gì, mong đợi gì")
    test = o_nhap(trai, 2)
    nhan(trai, "Đã thử  ·  tuỳ chọn")
    tried = o_nhap(trai, 2)

    # ------------------------------------------------------------ cột phải: cấp + câu hỏi
    phai = tk.Frame(body, bg=MAU["nen"])
    phai.grid(row=0, column=1, sticky="nsew", padx=(12, 0))
    phai.columnconfigure(0, weight=1)
    phai.rowconfigure(1, weight=1)

    cap_k = Khung(phai, MAU["nen"], MAU["the"], r=16, pad=22, bong=MAU["bong"])
    cap_k.grid(row=0, column=0, sticky="ew")
    tk.Label(cap_k.trong, text="Cấp gợi ý", bg=MAU["the"], fg=MAU["chu"], font=(ui, 14, "bold")).pack(anchor="w")
    buoc = tk.Frame(cap_k.trong, bg=MAU["the"])
    buoc.pack(fill="x", pady=(14, 4))
    o_cap = {}
    for n in range(1, 5):
        buoc.columnconfigure(n - 1, weight=1, uniform="b")
        o = tk.Frame(buoc, bg=MAU["the"])
        o.grid(row=0, column=n - 1, sticky="ew", padx=2)
        thanh = ThanhBuoc(o)
        thanh.pack(fill="x")
        so = tk.Label(o, text=str(n), bg=MAU["the"], fg=MAU["phu"], font=(ui, 12, "bold"))
        so.pack(pady=(8, 0))
        ten = tk.Label(o, text=CAP[n], bg=MAU["the"], fg=MAU["phu"], font=(ui, 9))
        ten.pack()
        o_cap[n] = (thanh, so, ten)
    mo_ta_k = Khung(cap_k.trong, MAU["the"], MAU["mo_ta"], r=8, pad=10)
    mo_ta_k.pack(fill="x", pady=(12, 0))
    mo_ta = tk.Label(mo_ta_k.trong, text="", bg=MAU["mo_ta"], fg=MAU["chinh"], font=(ui, 10), anchor="w")
    mo_ta.pack(fill="x")

    goi_y_k = Khung(phai, MAU["nen"], MAU["the"], r=16, pad=22, bong=MAU["bong"], tu_cao=False)
    goi_y_k.grid(row=1, column=0, sticky="nsew", pady=(18, 0))
    tk.Label(goi_y_k.trong, text="Câu hỏi gợi mở", bg=MAU["the"], fg=MAU["chu"],
             font=(ui, 14, "bold")).pack(anchor="w")
    nut = tk.Frame(goi_y_k.trong, bg=MAU["the"])
    nut.pack(side="bottom", fill="x", pady=(10, 0))
    goi_y = tk.Text(goi_y_k.trong, wrap="word", relief="flat", bd=0, highlightthickness=0, bg=MAU["the"],
                    fg=MAU["chu"], font=(ui, 12), padx=2, pady=6, height=8, cursor="arrow")
    goi_y.tag_configure("cap", foreground=MAU["chinh"], font=(ui, 9, "bold"), spacing1=12)
    goi_y.tag_configure("hoi", font=(ui, 13), spacing1=4, spacing3=4)
    goi_y.tag_configure("cu", foreground=MAU["phu"], font=(ui, 10), spacing1=2)
    goi_y.tag_configure("loi", foreground=MAU["loi"], font=(ui, 10))
    goi_y.tag_configure("trong", foreground=MAU["phu"], font=(ui, 10, "italic"))
    goi_y.pack(fill="both", expand=True, pady=(6, 0))
    goi_y.configure(state="disabled")

    status = tk.Label(root, text="", bg="#E3E7F0", fg=MAU["phu"], font=(ui, 9), anchor="w", padx=24, pady=7)
    status.grid(row=2, column=0, sticky="ew")
    SAN_SANG = "Sẵn sàng  ·  Ctrl+Enter để nhận gợi ý"

    # ------------------------------------------------------------ trạng thái
    st = {"muc": 1, "lich_su": [], "dang_chay": False, "bai": None}
    kq = queue.Queue()

    def ve_cap():
        for n, (thanh, so, ten) in o_cap.items():
            if n < st["muc"]:
                mau, chu = MAU["buoc_xong"], MAU["chu"]
            elif n == st["muc"]:
                mau, chu = MAU["chinh"], MAU["chinh"]
            else:
                mau, chu = MAU["buoc_cho"], MAU["phu"]
            thanh.dat_mau(mau)
            so.configure(fg=chu)
            ten.configure(fg=chu, font=(ui, 9, "bold" if n == st["muc"] else "normal"))
        mo_ta.configure(text="Cấp %d  ·  %s" % (st["muc"], MO_TA_CAP[st["muc"]]))
        nut_tiep.dat_bat(st["muc"] < 4 and bool(st["lich_su"]) and not st["dang_chay"])
        nut_hoi.dat_bat(not st["dang_chay"])

    def ve_goi_y(dang_cho=False, loi=None):
        goi_y.configure(state="normal")
        goi_y.delete("1.0", "end")
        if not st["lich_su"] and not dang_cho and not loi:
            goi_y.insert("end", "Điền đề, code và test bên trái rồi bấm \"Nhận gợi ý\".\n"
                                "Mỗi lần trợ lý chỉ hỏi một câu — chưa ra thì xin cấp tiếp theo.", "trong")
        for i, (m, q) in enumerate(st["lich_su"]):
            moi = i == len(st["lich_su"]) - 1
            goi_y.insert("end", "CẤP %d  ·  %s\n" % (m, CAP.get(m, "").upper()), "cap")
            goi_y.insert("end", q + "\n", "hoi" if moi else "cu")
        if dang_cho:
            goi_y.insert("end", "\nĐang suy nghĩ câu hỏi cấp %d…" % st["muc"], "trong")
        if loi:
            goi_y.insert("end", "\n" + loi, "loi")
        goi_y.configure(state="disabled")
        goi_y.see("end")

    def lay_bai():
        return (de.get("1.0", "end-1c").strip(), code.get("1.0", "end-1c").strip(), test.get("1.0", "end-1c").strip())

    def chay(muc):
        d, c, t = lay_bai()
        if st["bai"] != (d, c, t):                     # đổi bài / sửa code → bắt đầu lại từ cấp 1
            st["lich_su"] = []
            if st["bai"] is not None:
                muc = 1
        st["bai"], st["muc"], st["dang_chay"] = (d, c, t), muc, True
        raw = "[DE]\n%s\n[CODE]\n%s\n[TEST]\n%s\n[MUC] %d\n[DA_THU]\n%s" % (
            d, c, t, muc, tried.get("1.0", "end-1c").strip())
        ve_cap()
        ve_goi_y(dang_cho=True)
        status.configure(text="Đang gọi trợ lý…")

        def nen():
            tracing.begin("app-level-%d" % muc)
            start = time.perf_counter()
            try:
                output = answer(raw).get("output", "")
                summary, _ = tracing.end()
                kq.put(("ok", muc, output, summary, time.perf_counter() - start))
            except Exception as exc:
                tracing.end()
                kq.put(("loi", muc, "%s: %s" % (type(exc).__name__, exc), None, 0))

        threading.Thread(target=nen, daemon=True).start()
        root.after(100, doi_ket_qua)

    def doi_ket_qua():
        try:
            loai, muc, noi_dung, summary, giay = kq.get_nowait()
        except queue.Empty:
            root.after(100, doi_ket_qua)
            return
        st["dang_chay"] = False
        if loai == "ok":
            st["lich_su"].append((muc, noi_dung))
            ve_goi_y()
            status.configure(text="Model: %s  ·  %d lần gọi  ·  %d công cụ  ·  token vào %d / ra %d  ·  %.1fs" % (
                ", ".join(summary["models"]) or "không gọi", summary["model_calls"], summary["tool_calls"],
                summary["tokens_in"], summary["tokens_out"], giay))
        else:
            ve_goi_y(loi="Không tạo được gợi ý — thử lại sau vài giây.\n(%s)" % noi_dung[:200])
            status.configure(text="Lỗi khi gọi trợ lý")
        ve_cap()

    def nhan_goi_y(_e=None):
        if not st["dang_chay"]:
            chay(st["muc"] if st["bai"] == lay_bai() else 1)
        return "break"

    def cap_tiep():
        if st["dang_chay"]:
            return
        if st["muc"] >= 4:
            messagebox.showinfo("Đã hết cấp gợi ý", QUA_CAP_UI)
            return
        chay(st["muc"] + 1)

    def bai_moi():
        if st["dang_chay"]:
            return
        for t in (de, code, test, tried):
            t.delete("1.0", "end")
        st.update(muc=1, lich_su=[], bai=None)
        cap_nhat_code()
        ve_cap()
        ve_goi_y()
        status.configure(text=SAN_SANG)

    def dan_vi_du():
        bai_moi()
        de.insert("1.0", VI_DU["de"])
        code.insert("1.0", VI_DU["code"])
        test.insert("1.0", VI_DU["test"])
        cap_nhat_code()

    nut_hoi = Nut(nut, "Nhận gợi ý", nhan_goi_y, MAU["the"], "chinh")
    nut_hoi.pack(side="left")
    nut_tiep = Nut(nut, "Vẫn chưa ra  →  cấp tiếp theo", cap_tiep, MAU["the"], "nhat")
    nut_tiep.pack(side="left", padx=10)
    Nut(top, "Bài mới", bai_moi, MAU["the"], "chinh").pack(side="right")
    Nut(top, "Dán ví dụ", dan_vi_du, MAU["the"], "nhat").pack(side="right", padx=8)

    for o in (de, code, test, tried):              # gắn vào từng ô để chặn xuống dòng khi bấm Ctrl+Enter
        o.bind("<Control-Return>", nhan_goi_y)
    status.configure(text=SAN_SANG)
    cap_nhat_code()
    ve_cap()
    ve_goi_y()
    de.focus_set()
    root.mainloop()
    return 0


def main():
    try:
        import tkinter  # noqa: F401
    except Exception:
        return _run_terminal()
    if os.environ.get("DISPLAY") or sys.platform in ("win32", "darwin"):
        return _run_gui()
    return _run_terminal()


if __name__ == "__main__":
    sys.exit(main())
