"""Đếm số chính từ evidence/survey/results.csv (chỉ thư viện chuẩn).

Chạy:  python evidence/survey/count_survey.py
"""
import csv
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")  # cửa sổ lệnh Windows in được tiếng Việt

PATH = Path(__file__).with_name("results.csv")

# Đáp án hợp lệ của câu "Đã làm gì" (form cho chọn nhiều)
CACH_LAM = {
    "Tự đọc lại code", "In giá trị trung gian (print)", "Chạy tay với input nhỏ",
    "Dán code vào ChatGPT / AI khác", "Hỏi bạn", "Xem lời giải có sẵn", "Bỏ qua",
}

rows = list(csv.DictReader(PATH.open(encoding="utf-8")))
n = len(rows)


def dem(rs, cot):
    return Counter(r[cot] for r in rs)


def in_bang(tieu_de, c, mau):
    print(f"\n{tieu_de} (mẫu số {mau})")
    for k, v in c.most_common():
        print(f"  {v:>2}/{mau}  {k}")


print(f"Tổng số câu trả lời: {n}")
in_bang("Vai", dem(rows, "ban_la"), n)

chua_gap = [r for r in rows if r["da_lam_gi"] == "Chưa gặp trường hợp này"]
da_gap = [r for r in rows if r not in chua_gap]
print(f"\nĐã gặp tình huống: {len(da_gap)}/{n} · chưa gặp: {len(chua_gap)}/{n}")

for vai in ("tat_ca", "Học viên L3A", "Học viên L3B"):
    rs = da_gap if vai == "tat_ca" else [r for r in da_gap if r["ban_la"] == vai]
    m = len(rs)
    print(f"\n===== Nhóm: {vai} (đã gặp, n={m}) =====")
    in_bang("Khó khăn mất thời gian nhất", dem(rs, "kho_nhat"), m)
    in_bang("Thời gian xử lý", dem(rs, "thoi_gian"), m)
    in_bang("Kết quả", dem(rs, "ket_qua"), m)
    in_bang("Tự giải thích được vì sao sai", dem(rs, "tu_giai_thich"), m)
    so_lan = sorted(int(r["so_lan_1_tuan"]) for r in rs)
    if so_lan:
        print(f"\nSố lần / 1 tuần qua: trung vị {so_lan[len(so_lan) // 2]} "
              f"(giá trị: {so_lan})")

# Cách xoay xở: bỏ câu trả lời không hợp lệ (người trả lời chọn nhầm vai)
hop_le, khong_hop_le = [], []
for r in da_gap:
    lua_chon = [x.strip() for x in r["da_lam_gi"].split(";")]
    (hop_le if all(x in CACH_LAM for x in lua_chon) else khong_hop_le).append((r, lua_chon))
c = Counter(x for _, ls in hop_le for x in ls)
in_bang("Cách xoay xở (chọn nhiều, chỉ câu hợp lệ)", c, len(hop_le))
print(f"  Câu 'Đã làm gì' không hợp lệ: {len(khong_hop_le)} "
      f"({', '.join(r['id'] for r, _ in khong_hop_le)})")

ai = [r for r, ls in hop_le if "Dán code vào ChatGPT / AI khác" in ls
      or "Xem lời giải có sẵn" in ls]
in_bang("Trong số dùng AI / xem lời giải: tự giải thích được?",
        dem(ai, "tu_giai_thich"), len(ai))
