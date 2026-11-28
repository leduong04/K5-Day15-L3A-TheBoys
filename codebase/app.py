"""Tk interface for the Socratic Debugger, with a terminal fallback."""
import os
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

MAU = {
    "nen": "#F4F6FB", "the": "#FFFFFF", "vien": "#DDE3EE", "chu": "#1F2937", "phu": "#6B7280",
    "chinh": "#4F46E5", "chinh_dam": "#4338CA", "chinh_nhat": "#EEF2FF",
    "xong": "#10B981", "cho": "#E5E7EB", "code_nen": "#1E1E2E", "code_chu": "#E5E7EB",
    "loi": "#DC2626", "header": "#312E81",
}


def _run_gui():
    import queue
    import threading
    import tkinter as tk
    from tkinter import messagebox

    import tracing
    from agent import answer

    ui = "Segoe UI" if sys.platform == "win32" else "Helvetica"
    mono = "Consolas" if sys.platform == "win32" else "Menlo"

    root = tk.Tk()
    root.title("Socratic Debugger · Python Mini Lab")
    root.geometry("1180x780")
    root.minsize(980, 660)
    root.configure(bg=MAU["nen"])
    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)

    # ------------------------------------------------------------ header
    header = tk.Frame(root, bg=MAU["header"], padx=24, pady=14)
    header.grid(row=0, column=0, sticky="ew")
    tk.Label(header, text="Socratic Debugger", bg=MAU["header"], fg="white",
             font=(ui, 18, "bold")).pack(side="left")
    tk.Label(header, text="Không đưa đáp án — chỉ hỏi đúng một câu để bạn tự tìm ra lỗi",
             bg=MAU["header"], fg="#C7D2FE", font=(ui, 10)).pack(side="left", padx=16, pady=(6, 0))

    body = tk.Frame(root, bg=MAU["nen"], padx=20, pady=16)
    body.grid(row=1, column=0, sticky="nsew")
    body.columnconfigure(0, weight=5, uniform="c")
    body.columnconfigure(1, weight=4, uniform="c")
    body.rowconfigure(0, weight=1)

    def the(parent, **grid):
        f = tk.Frame(parent, bg=MAU["the"], highlightbackground=MAU["vien"], highlightthickness=1, padx=16, pady=14)
        f.grid(**grid)
        return f

    def nhan(parent, text, sub=None):
        row = tk.Frame(parent, bg=MAU["the"])
        row.pack(fill="x", pady=(8, 4))
        tk.Label(row, text=text, bg=MAU["the"], fg=MAU["chu"], font=(ui, 10, "bold")).pack(side="left")
        if sub:
            tk.Label(row, text=sub, bg=MAU["the"], fg=MAU["phu"], font=(ui, 9)).pack(side="left", padx=6)

    def o_nhap(parent, height, **kw):
        t = tk.Text(parent, height=height, wrap=kw.pop("wrap", "word"), undo=True, relief="flat",
                    highlightthickness=1, highlightbackground=MAU["vien"], highlightcolor=MAU["chinh"],
                    padx=10, pady=8, font=kw.pop("font", (ui, 10)), **kw)
        return t

    # ------------------------------------------------------------ cột trái: đầu vào
    trai = the(body, row=0, column=0, sticky="nsew", padx=(0, 10))
    top = tk.Frame(trai, bg=MAU["the"])
    top.pack(fill="x")
    tk.Label(top, text="Bài của bạn", bg=MAU["the"], fg=MAU["chu"], font=(ui, 13, "bold")).pack(side="left")

    nhan(trai, "Đề bài", "hàm cần làm gì")
    de = o_nhap(trai, 3)
    de.pack(fill="x")

    nhan(trai, "Code đang chạy sai", "dán nhiều dòng được")
    code = o_nhap(trai, 11, wrap="none", font=(mono, 11), bg=MAU["code_nen"], fg=MAU["code_chu"],
                  insertbackground="white")
    code.pack(fill="both", expand=True)

    nhan(trai, "Test", "input · ra kết quả gì · mong đợi gì")
    test = o_nhap(trai, 2)
    test.pack(fill="x")

    nhan(trai, "Đã thử", "tuỳ chọn — để gợi ý không lặp lại")
    tried = o_nhap(trai, 2)
    tried.pack(fill="x")

    # ------------------------------------------------------------ cột phải: cấp + gợi ý
    phai = tk.Frame(body, bg=MAU["nen"])
    phai.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
    phai.columnconfigure(0, weight=1)
    phai.rowconfigure(1, weight=1)

    the_cap = the(phai, row=0, column=0, sticky="ew")
    tk.Label(the_cap, text="Cấp gợi ý", bg=MAU["the"], fg=MAU["chu"], font=(ui, 13, "bold")).pack(anchor="w")
    buoc = tk.Frame(the_cap, bg=MAU["the"])
    buoc.pack(fill="x", pady=(10, 6))
    o_cap = {}
    for n in range(1, 5):
        buoc.columnconfigure(n - 1, weight=1)
        o = tk.Frame(buoc, bg=MAU["the"])
        o.grid(row=0, column=n - 1, sticky="ew", padx=3)
        thanh = tk.Frame(o, height=6, bg=MAU["cho"])
        thanh.pack(fill="x")
        so = tk.Label(o, text="%d" % n, bg=MAU["the"], fg=MAU["phu"], font=(ui, 12, "bold"))
        so.pack(pady=(6, 0))
        ten = tk.Label(o, text=CAP[n], bg=MAU["the"], fg=MAU["phu"], font=(ui, 9))
        ten.pack()
        o_cap[n] = (thanh, so, ten)
    mo_ta = tk.Label(the_cap, text="", bg=MAU["chinh_nhat"], fg=MAU["chinh_dam"], font=(ui, 10),
                     anchor="w", justify="left", padx=10, pady=6)
    mo_ta.pack(fill="x", pady=(6, 0))

    the_goi_y = the(phai, row=1, column=0, sticky="nsew", pady=(14, 0))
    tk.Label(the_goi_y, text="Câu hỏi gợi mở", bg=MAU["the"], fg=MAU["chu"], font=(ui, 13, "bold")).pack(anchor="w")
    goi_y = tk.Text(the_goi_y, wrap="word", relief="flat", bg=MAU["the"], fg=MAU["chu"],
                    font=(ui, 12), padx=4, pady=8, height=8, cursor="arrow")
    goi_y.tag_configure("cap", foreground=MAU["chinh"], font=(ui, 9, "bold"), spacing1=10)
    goi_y.tag_configure("hoi", font=(ui, 12), spacing3=6, lmargin1=2, lmargin2=2)
    goi_y.tag_configure("cu", foreground=MAU["phu"], font=(ui, 10))
    goi_y.tag_configure("loi", foreground=MAU["loi"], font=(ui, 10))
    goi_y.tag_configure("trong", foreground=MAU["phu"], font=(ui, 10, "italic"))
    goi_y.pack(fill="both", expand=True, pady=(4, 8))
    goi_y.configure(state="disabled")

    nut = tk.Frame(the_goi_y, bg=MAU["the"])
    nut.pack(fill="x")

    def tao_nut(parent, text, cmd, chinh=True):
        b = tk.Button(parent, text=text, command=cmd, relief="flat", cursor="hand2", padx=14, pady=8,
                      font=(ui, 10, "bold"),
                      bg=MAU["chinh"] if chinh else MAU["chinh_nhat"],
                      fg="white" if chinh else MAU["chinh_dam"],
                      activebackground=MAU["chinh_dam"] if chinh else MAU["vien"],
                      activeforeground="white" if chinh else MAU["chinh_dam"], disabledforeground="#A5B4FC")
        return b

    status = tk.Label(root, text="Sẵn sàng · Ctrl+Enter để nhận gợi ý", bg=MAU["nen"], fg=MAU["phu"],
                      font=(ui, 9), anchor="w", padx=22, pady=6)
    status.grid(row=2, column=0, sticky="ew")

    # ------------------------------------------------------------ trạng thái
    st = {"muc": 1, "lich_su": [], "dang_chay": False, "bai": None}
    kq = queue.Queue()

    def ve_cap():
        for n, (thanh, so, ten) in o_cap.items():
            if n < st["muc"]:
                mau, chu = MAU["xong"], MAU["chu"]
            elif n == st["muc"]:
                mau, chu = MAU["chinh"], MAU["chinh"]
            else:
                mau, chu = MAU["cho"], MAU["phu"]
            thanh.configure(bg=mau)
            so.configure(fg=chu)
            ten.configure(fg=chu, font=(ui, 9, "bold" if n == st["muc"] else "normal"))
        mo_ta.configure(text="Cấp %d · %s" % (st["muc"], MO_TA_CAP[st["muc"]]))
        nut_tiep.configure(state="disabled" if st["muc"] >= 4 or not st["lich_su"] or st["dang_chay"] else "normal")
        nut_hoi.configure(state="disabled" if st["dang_chay"] else "normal")

    def ve_goi_y(dang_cho=False, loi=None):
        goi_y.configure(state="normal")
        goi_y.delete("1.0", "end")
        if not st["lich_su"] and not dang_cho and not loi:
            goi_y.insert("end", "Điền đề, code và test bên trái rồi bấm \"Nhận gợi ý\".\n"
                                "Mỗi lần trợ lý chỉ hỏi một câu — chưa ra thì xin cấp tiếp theo.", "trong")
        for i, (m, q) in enumerate(st["lich_su"]):
            moi = i == len(st["lich_su"]) - 1
            goi_y.insert("end", "CẤP %d · %s\n" % (m, CAP.get(m, "").upper()), "cap")
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
        if st["bai"] is not None and st["bai"] != (d, c, t) and muc > 1:
            muc = 1                                    # đổi bài / sửa code → bắt đầu lại từ cấp 1
        if st["bai"] != (d, c, t):
            st["lich_su"] = []
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
            status.configure(text="Model: %s · %d lần gọi · %d công cụ · token vào %d / ra %d · %.1fs" % (
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
        ve_cap()
        ve_goi_y()
        status.configure(text="Sẵn sàng · Ctrl+Enter để nhận gợi ý")

    def dan_vi_du():
        bai_moi()
        de.insert("1.0", VI_DU["de"])
        code.insert("1.0", VI_DU["code"])
        test.insert("1.0", VI_DU["test"])

    nut_hoi = tao_nut(nut, "Nhận gợi ý", nhan_goi_y)
    nut_hoi.pack(side="left")
    nut_tiep = tao_nut(nut, "Vẫn chưa ra → cấp tiếp theo", cap_tiep, chinh=False)
    nut_tiep.pack(side="left", padx=8)
    tao_nut(top, "Bài mới", bai_moi, chinh=False).pack(side="right")
    tao_nut(top, "Dán ví dụ", dan_vi_du, chinh=False).pack(side="right", padx=6)

    for o in (de, code, test, tried):              # gắn vào từng ô để chặn xuống dòng khi bấm Ctrl+Enter
        o.bind("<Control-Return>", nhan_goi_y)
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
