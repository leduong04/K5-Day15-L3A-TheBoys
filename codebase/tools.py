"""Công cụ của Socratic Debugger — khớp bảng công cụ ở spec.md §4.

Mỗi công cụ là một hàm có @tool (khung tự ghi vào trace). Không công cụ nào tác động ra ngoài:
không ghi file, không chạy code của học viên, không gửi tin.
"""
import builtins
import json
import keyword
import os
import re

from tracing import tool, TOOLS  # noqa: F401

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LABS_PATH = os.path.join(ROOT, "data", "labs.json")

NHAN = ["DE", "CODE", "TEST", "MUC", "DA_THU"]   # nhãn đầu vào đã chốt (spec.md §4)
BAT_BUOC = ["DE", "CODE", "TEST"]
MUC_TOI_DA = 4
MAX_TU = 60                                       # câu hỏi tối đa ~60 từ
NGUONG_TU_KHOA = 3                                # lookup_lab: không trùng tên hàm thì cần ≥3 từ khoá

# Tên có sẵn của Python (range, len, print, for, if…) — trùng tên này không tính là "dùng lại tên của bài"
TEN_CO_SAN = set(keyword.kwlist) | set(dir(builtins))
CUM_LO_LOI_GIAI = ["sửa thành", "đổi thành", "thay bằng", "thay thành", "đáp án là", "lời giải là", "code đúng là"]
TU_KHOA_CODE_CAP1 = [
    r"\brange\s*\(", r"\bfor\s+", r"\bwhile\s+", r"\bif\s+", r"\breturn\b",
    r"\bdef\s+", r"\blen\s*\(", r"\belse\b", r"\belif\b",
]
TOAN_TU_THAY_THE = [
    ("//", r"(?<![/\\])['`\"]/(?![/\\])['`\"]", "'/' thay cho '//'"),
    (">", r"['`\"]>=\s*['`\"]", "'>=' thay cho '>'"),
    ("<", r"['`\"]<=\s*['`\"]", "'<=' thay cho '<'"),
    ("=", r"['`\"]\+=['`\"]", "'+=' thay cho '='"),
]


# ---------------------------------------------------------------- parse_input
@tool
def parse_input(text: str) -> dict:
    """parse_input · Input: chuỗi người dùng gửi (định dạng [DE] [CODE] [TEST] [MUC] [DA_THU]) ·
    Output: {"de","code","test","muc","da_thu","co_nhan","thieu":[...]} · Không tác động ra ngoài.

    - co_nhan = False khi không có nhãn nào (người dùng gõ tự do) → để model tự hiểu.
    - thieu = các nhãn bắt buộc còn thiếu (chỉ xét khi co_nhan = True).
    - muc: số nguyên ≥1; không có hoặc không đọc được thì 1. Có thể > 4 (đã qua hết cấp).
    """
    pattern = re.compile(r"^\s*\[(%s)\]" % "|".join(NHAN), re.IGNORECASE | re.MULTILINE)
    matches = list(pattern.finditer(text))
    phan = {k: "" for k in NHAN}
    for idx, m in enumerate(matches):
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        phan[m.group(1).upper()] = text[m.end():end].strip("\n").strip()

    muc_so = re.search(r"\d+", phan["MUC"])
    muc = int(muc_so.group()) if muc_so else 1
    co_nhan = bool(matches)
    thieu = [k for k in BAT_BUOC if co_nhan and not phan[k]]
    return {
        "de": phan["DE"], "code": phan["CODE"], "test": phan["TEST"],
        "muc": max(1, muc), "da_thu": phan["DA_THU"],
        "co_nhan": co_nhan, "thieu": thieu,
    }


# ---------------------------------------------------------------- lookup_lab
def _doc_labs():
    with open(LABS_PATH, encoding="utf-8") as f:
        return json.load(f)


@tool
def lookup_lab(de: str, code: str = "") -> list:
    """lookup_lab · Input: đề bài (str), code học viên (str, tuỳ chọn) ·
    Output: tối đa 1 bài khớp trong data/labs.json {"code","de","test_mau","loi_hay_gap"}, [] nếu không thấy ·
    Không tác động ra ngoài.

    Khớp khi: tên hàm của bài xuất hiện trong đề/code, HOẶC trùng ≥ NGUONG_TU_KHOA từ khoá.
    Ngưỡng cao để tránh khớp nhầm bài khác (vd "tổng số lẻ" ≠ LAB-01 "tổng số chẵn"):
    khớp nhầm còn tệ hơn không khớp, vì model sẽ dựa vào đề và test của bài khác.
    """
    noi_dung = (de + "\n" + code).lower()
    tot_nhat, diem_cao = None, 0
    for lab in _doc_labs():
        diem = 0
        if lab["ten_ham"].lower() in noi_dung:
            diem += 10
        diem += sum(1 for k in lab["tu_khoa"] if k.lower() in noi_dung)
        if diem > diem_cao:
            tot_nhat, diem_cao = lab, diem
    if not tot_nhat or diem_cao < NGUONG_TU_KHOA:   # khớp yếu thì coi như không có căn cứ
        return []
    return [{k: tot_nhat[k] for k in ("code", "de", "test_mau", "loi_hay_gap")}]


# ---------------------------------------------------------------- check_no_solution
def _ten(s: str) -> set:
    """Các tên (biến, hàm) trong một đoạn, bỏ tên có sẵn của Python."""
    return {t for t in re.findall(r"[A-Za-z_]\w*", s) if t not in TEN_CO_SAN}


def _gon(s: str) -> str:
    return re.sub(r"\s+", "", s)


@tool
def check_no_solution(answer: str, student_code: str, muc: int = 1) -> dict:
    """check_no_solution · Input: câu trả lời của model, code học viên, cấp gợi ý ·
    Output: {"ok": bool, "ly_do": str} · Không tác động ra ngoài.

    Không đạt khi:
    1. có khối code ``` ;
    2. có cụm kiểu "sửa thành", "đáp án là"… hoặc lộ toán tử thay thế trực tiếp ('/' thay '//', '>=' thay '>'…);
    3. cấp 1: chỉ vào vùng code (có backtick `...`, tên hàm/từ khoá code như range/for/if/return/len);
    4. có đoạn trong `...` dùng tên biến/hàm của bài mà KHÔNG phải trích nguyên văn code học viên;
    5. cấp 4: dùng lại tên biến/hàm bài gốc (ở cả `...`, '...' hoặc trong câu trả lời);
    6. sai định dạng: rỗng, không có đúng 1 dấu "?", hoặc dài hơn MAX_TU từ.
    """
    a = (answer or "").strip()
    if not a:
        return {"ok": False, "ly_do": "câu trả lời rỗng"}
    if "```" in a:
        return {"ok": False, "ly_do": "có khối code"}
    thap = a.lower()
    for cum in CUM_LO_LOI_GIAI:
        if cum in thap:
            return {"ok": False, "ly_do": "có cụm '%s'" % cum}

    # Chặn lộ toán tử thay thế trực tiếp (vd code dùng // mà câu hỏi nhắc '/')
    for goc, mau_thay, mo_ta in TOAN_TU_THAY_THE:
        if goc in student_code and re.search(mau_thay, a):
            if goc == ">" and ">=" in student_code:
                continue
            if goc == "<" and "<=" in student_code:
                continue
            if goc == "=" and "+=" in student_code:
                continue
            return {"ok": False, "ly_do": "lộ toán tử thay thế trực tiếp (%s)" % mo_ta}

    ten_bai = _ten(student_code)
    code_gon = _gon(student_code)

    # Cấp 1 (Quan sát): chưa được chỉ tên dòng/hàm/vùng code
    if muc == 1:
        if "`" in a:
            return {"ok": False, "ly_do": "cấp 1 không được trích dẫn code trong dấu `...`"}
        for mau in TU_KHOA_CODE_CAP1:
            if re.search(mau, a):
                return {"ok": False, "ly_do": "cấp 1 không được chỉ vào cấu trúc/hàm code"}

    # Cấp 4 (Ví dụ tương tự): không được dùng lại tên biến/hàm dài >= 3 ký tự của bài gốc ở bất kỳ đâu
    if muc >= 4:
        ten_bai_dai = {t for t in ten_bai if len(t) >= 3}
        trung_toan_cau = _ten(a) & ten_bai_dai
        if trung_toan_cau:
            return {"ok": False, "ly_do": "cấp 4 dùng lại tên của bài gốc: %s" % ", ".join(sorted(trung_toan_cau))}

    for doan in re.findall(r"`([^`]+)`", a):
        dung_ten_bai = _ten(doan) & ten_bai
        if not dung_ten_bai:
            continue                                   # vd `range(a, b)`: khái niệm chung, không phải code sửa
        if muc >= 4:
            return {"ok": False, "ly_do": "cấp 4 dùng lại tên của bài gốc: %s" % ", ".join(sorted(dung_ten_bai))}
        if _gon(doan) not in code_gon:
            return {"ok": False, "ly_do": "đoạn `%s` không phải trích từ code học viên (có thể là code sửa)" % doan}

    if a.count("?") != 1:
        return {"ok": False, "ly_do": "không có đúng một câu hỏi"}
    if len(a.split()) > MAX_TU:
        return {"ok": False, "ly_do": "dài hơn %d từ" % MAX_TU}
    return {"ok": True, "ly_do": ""}
