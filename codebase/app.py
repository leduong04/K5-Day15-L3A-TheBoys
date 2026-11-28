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


def _run_gui():
    import tkinter as tk
    from tkinter import messagebox, ttk

    import tracing
    from agent import answer

    root = tk.Tk()
    root.title("Socratic Debugger · Python Mini Lab")
    root.geometry("920x820")
    root.minsize(700, 600)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)

    outer = ttk.Frame(root, padding=16)
    outer.grid(row=0, column=0, rowspan=2, sticky="nsew")
    outer.columnconfigure(0, weight=1)
    outer.rowconfigure(4, weight=2)
    outer.rowconfigure(7, weight=1)

    ttk.Label(outer, text="Python Mini Lab · Tìm lỗi bằng gợi ý từng bước",
              font=("TkDefaultFont", 16, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 12))
    ttk.Label(outer, text="Đề bài").grid(row=1, column=0, sticky="w")
    de = tk.Text(outer, height=4, wrap="word", undo=True)
    de.grid(row=2, column=0, sticky="nsew", pady=(4, 10))

    ttk.Label(outer, text="Code đang chạy sai (có thể dán nhiều dòng)").grid(row=3, column=0, sticky="w")
    code = tk.Text(outer, height=12, wrap="none", undo=True, font=("TkFixedFont", 10))
    code.grid(row=4, column=0, sticky="nsew", pady=(4, 10))

    ttk.Label(outer, text="Test: input, kết quả hiện tại và kết quả mong đợi").grid(row=5, column=0, sticky="w")
    test = tk.Text(outer, height=4, wrap="word", undo=True)
    test.grid(row=6, column=0, sticky="nsew", pady=(4, 10))

    row = ttk.Frame(outer)
    row.grid(row=7, column=0, sticky="ew")
    row.columnconfigure(1, weight=1)
    ttk.Label(row, text="Đã thử (tuỳ chọn)").grid(row=0, column=0, sticky="w", padx=(0, 8))
    tried = ttk.Entry(row)
    tried.grid(row=0, column=1, sticky="ew")
    level = tk.IntVar(value=1)
    level_label = ttk.Label(row, text="Cấp 1/4")
    level_label.grid(row=0, column=2, padx=10)

    ttk.Label(outer, text="Gợi ý").grid(row=8, column=0, sticky="w", pady=(12, 0))
    result_box = tk.Text(outer, height=4, wrap="word", state="disabled")
    result_box.grid(row=9, column=0, sticky="ew", pady=(4, 8))
    status = ttk.Label(outer, text="Sẵn sàng")
    status.grid(row=10, column=0, sticky="w")

    def set_result(value):
        result_box.configure(state="normal")
        result_box.delete("1.0", "end")
        result_box.insert("1.0", value)
        result_box.configure(state="disabled")

    def submit():
        raw = "[DE]\n%s\n[CODE]\n%s\n[TEST]\n%s\n[MUC] %d\n[DA_THU]\n%s" % (
            de.get("1.0", "end-1c"), code.get("1.0", "end-1c"), test.get("1.0", "end-1c"),
            level.get(), tried.get().strip())
        tracing.begin("app-level-%d" % level.get())
        start = time.perf_counter()
        try:
            output = answer(raw).get("output", "")
            summary, _ = tracing.end()
            set_result(output)
            status.configure(text="Model: %s · %d gọi · %d công cụ · token vào %d / ra %d · %.1fs" % (
                ", ".join(summary["models"]) or "không gọi", summary["model_calls"], summary["tool_calls"],
                summary["tokens_in"], summary["tokens_out"], time.perf_counter() - start))
        except Exception as exc:
            tracing.end()
            status.configure(text="Lỗi khi gọi trợ lý")
            messagebox.showerror("Không thể tạo gợi ý", "%s: %s" % (type(exc).__name__, exc))

    def next_level():
        if level.get() >= 4:
            messagebox.showinfo("Đã hết cấp gợi ý", "Bạn đã qua cấp 4. Hãy mang đề, code và những gì đã thử tới lab coach.")
            return
        level.set(level.get() + 1)
        level_label.configure(text="Cấp %d/4" % level.get())
        submit()

    buttons = ttk.Frame(outer)
    buttons.grid(row=11, column=0, sticky="e", pady=(8, 0))
    ttk.Button(buttons, text="Nhận gợi ý", command=submit).pack(side="left", padx=4)
    ttk.Button(buttons, text="Vẫn chưa ra → cấp tiếp theo", command=next_level).pack(side="left", padx=4)
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
