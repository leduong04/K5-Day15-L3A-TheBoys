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


# ---------------------------------------------------------------- check_syntax
@tool
def check_syntax(code: str) -> dict:
    """check_syntax · Input: code học viên (str) · Output: {"ok": bool, "dong": int|None} ·
    Không tác động ra ngoài — chỉ biên dịch (compile) để kiểm cú pháp, KHÔNG chạy code.

    Lỗi cú pháp nằm ngoài phạm vi (chỉ hỗ trợ lỗi logic: code chạy được nhưng ra kết quả sai).
    """
    try:
        compile(code, "<code_hoc_vien>", "exec")
        return {"ok": True, "dong": None}
    except SyntaxError as e:
        return {"ok": False, "dong": e.lineno}
    except ValueError:
        return {"ok": True, "dong": None}


# ---------------------------------------------------------------- check_no_solution
def _ten(s: str) -> set:
    """Các tên (biến, hàm) trong một đoạn, bỏ tên có sẵn của Python."""
    return {t for t in re.findall(r"[A-Za-z_]\w*", s) if t not in TEN_CO_SAN}


def _gon(s: str) -> str:
    return re.sub(r"\s+", "", s)


TU_KHOA_CAU_TRUC = {"for", "while", "if", "elif", "else", "return", "def", "lambda"}
# Cụm tiếng Việt chỉ vào vùng code — cấp 1 chưa được dùng ("điều kiện" không chặn vì đề bài cũng có điều kiện)
CUM_CHI_VUNG_CODE = ["vòng lặp", "dòng code", "dòng lệnh", "câu lệnh", "biến "]
# Cụm khuyên cách sửa — cấp 4 (ví dụ tương tự) chỉ được hỏi về tình huống ví dụ, không quay lại khuyên sửa bài gốc
CUM_KHUYEN_SUA = ["bạn nên", "nên chọn", "nên dùng", "nên đặt", "nên đổi", "nên sửa", "nên khởi tạo",
                  "giá trị khởi tạo nào", "khởi tạo bằng"]


def _co_tu(a: str, ten: str) -> bool:
    """`ten` xuất hiện như một từ riêng trong câu trả lời (không dính chữ khác)."""
    return re.search(r"(?<!\w)%s(?!\w)" % re.escape(ten), a) is not None


def _doan_trich(a: str) -> list:
    """Các đoạn học viên/model đặt trong `...`, '...' hoặc "..." — nơi model hay trích code."""
    return re.findall(r"`([^`]+)`|'([^']+)'|\"([^\"]+)\"", a)


def _ten_dung_lai(a: str, ten: set) -> set:
    """Tên của bài bị nhắc lại trong câu trả lời.
    Tên có '_' (tong_chan, lon_nhat) thì bắt ở bất cứ đâu; tên ngắn không '_' (so, dem, tong)
    chỉ bắt khi nằm trong dấu trích — vì dễ trùng chữ tiếng Việt không dấu ("so sánh")."""
    trich = " ".join(" ".join(g) for g in _doan_trich(a))
    thay = set()
    for t in ten:
        if len(t) < 2:
            continue
        if ("_" in t and _co_tu(a, t)) or _co_tu(trich, t):
            thay.add(t)
    return thay


def _ten_ham_va_tham_so(code: str) -> set:
    m = re.search(r"def\s+(\w+)\s*\(([^)]*)\)", code)
    if not m:
        return set()
    return {m.group(1)} | {p.split("=")[0].strip() for p in m.group(2).split(",") if p.strip()}


def kiem_cap(a: str, student_code: str, muc: int, test: str = "") -> str:
    """Kiểm câu hỏi có đúng cấp không. Trả lý do nếu lệch cấp, "" nếu ổn.

    Cấp 1 (quan sát): chưa được chỉ vùng code → không trích code, không nhắc tên biến
      (trừ tên hàm và tham số — vì test của học viên cũng dùng), không nhắc hàm/lệnh có trong code
      (range, len, for, if…).
    Cấp 4 (ví dụ tương tự): phải là bài khác → không dùng lại tên hàm, tham số, biến của bài gốc.
    Cấp 2, 3 không kiểm bằng code được (cấp 3 cần hiểu ý) → để prompt lo.
    """
    ten_bai = _ten(student_code)
    if muc == 1:
        test_gon = _gon(test)
        for g in re.findall(r"`([^`]+)`", a):
            if _gon(g) not in test_gon:
                return "cấp 1 không được trích code (`%s`) — chỉ so kết quả với mong đợi" % g
        cho_phep = _ten_ham_va_tham_so(student_code)
        bien = _ten_dung_lai(a, ten_bai - cho_phep)
        if bien:
            return "cấp 1 chưa được chỉ vào biến: %s" % ", ".join(sorted(bien))
        dung_trong_code = set(re.findall(r"[A-Za-z_]\w*", student_code))
        lenh = {t for t in dung_trong_code & (TEN_CO_SAN - set(keyword.kwlist) | TU_KHOA_CAU_TRUC)
                if len(t) >= 2 and _co_tu(a, t)}
        if lenh:
            return "cấp 1 chưa được chỉ vào lệnh/hàm trong code: %s" % ", ".join(sorted(lenh))
        vung = [c for c in CUM_CHI_VUNG_CODE if c in a.lower()]
        if vung:
            return "cấp 1 chưa được chỉ vào vùng code ('%s')" % vung[0]
    if muc >= 4:
        dung_lai = _ten_dung_lai(a, ten_bai | _ten_ham_va_tham_so(student_code))
        if dung_lai:
            return "cấp 4 phải là bài khác, không dùng lại tên của bài gốc: %s" % ", ".join(sorted(dung_lai))
        khuyen = [c for c in CUM_KHUYEN_SUA if c in a.lower()]
        if khuyen:
            return "cấp 4 chỉ hỏi về tình huống ví dụ, không khuyên cách sửa ('%s')" % khuyen[0]
    return ""


@tool
def check_no_solution(answer: str, student_code: str, muc: int = 1, test: str = "") -> dict:
    """check_no_solution · Input: câu trả lời của model, code học viên, cấp gợi ý, kết quả test (tuỳ chọn) ·
    Output: {"ok": bool, "ly_do": str} · Không tác động ra ngoài.

    Không đạt khi:
    1. có khối code ``` ;
    2. có cụm kiểu "sửa thành", "đáp án là"…;
    3. có đoạn trong `...` dùng tên biến/hàm của bài mà KHÔNG phải trích nguyên văn code học viên
       (dấu hiệu code đã sửa, vd `range(1, n+1)`);
    4. lệch cấp (kiem_cap): cấp 1 trích code / nhắc biến / nhắc lệnh; cấp 4 dùng lại tên bài gốc;
    5. sai định dạng: rỗng, không có đúng 1 dấu "?", hoặc dài hơn MAX_TU từ.
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

    ten_bai = _ten(student_code)
    code_gon = _gon(student_code)
    for doan in re.findall(r"`([^`]+)`", a):
        dung_ten_bai = _ten(doan) & ten_bai
        if not dung_ten_bai:
            continue                                   # vd `range(a, b)`: khái niệm chung, không phải code sửa
        if muc >= 4:
            return {"ok": False, "ly_do": "cấp 4 dùng lại tên của bài gốc: %s" % ", ".join(sorted(dung_ten_bai))}
        if _gon(doan) not in code_gon:
            return {"ok": False, "ly_do": "đoạn `%s` không phải trích từ code học viên (có thể là code sửa)" % doan}

    lech = kiem_cap(a, student_code, muc, test)
    if lech:
        return {"ok": False, "ly_do": lech}
    if a.count("?") != 1:
        return {"ok": False, "ly_do": "không có đúng một câu hỏi"}
    if len(a.split()) > MAX_TU:
        return {"ok": False, "ly_do": "dài hơn %d từ" % MAX_TU}
    return {"ok": True, "ly_do": ""}
