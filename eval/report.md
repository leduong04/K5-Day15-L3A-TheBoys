# Báo cáo đánh giá — lượt 1 → một cải tiến → lượt 3 (lượt 2 chạy lặp lỗi 429)

> Điền ở guide bước 4.1. Lượt 1 trước **CP3 10:00 Thứ Bảy 28/11**, lượt sau cải tiến trước **CP4 14:30 Thứ Bảy 28/11**, cùng bộ câu thử 24 câu, cùng cách chấm. Chấm ở rubric R5.
> Số lấy từ `python run.py score eval/run-1.csv` và `eval/run-3.csv` sau khi điền cột `pass`. **Kết quả thấp ghi thật vẫn đủ điểm.**
> Không được: sửa chuẩn "đạt", bỏ câu thử trượt, sửa `expected` cho khớp output, sửa kết quả lượt đã chạy.

## 1. Kết quả

| Lượt | Run ID | Đạt / tổng | % | thuong | kho | tu_choi | So với chuẩn "đạt" |
|---|---|---|---|---|---|---|---|
| 1 | `run-1@20261128-092750` | 13/24 | 54% | 6/12 (50%) | 5/8 (62%) | 2/4 (50%) | **chưa** (< 85%, có 1 câu lộ toán tử sửa `B23` và 2/4 `tu_choi` trượt) |
| 2 | `run-2@20261128-100327` | Chưa chấm / 24 (19 câu có output, 5 câu lỗi API 429) | — | — | — | — | Chưa thể kết luận *(chạy cùng cấu hình lượt 1, không có cải tiến)* |
| 3 | `run-3@20261128-123515` | **19/24** *(19/23 có output)* | **79%** *(83% có output)* | **11/12 (92%)** | **5/8 (62%)** *(5/7 có output)* | **3/4 (75%)** | **chưa** (< 85%, còn `B04` lộ hướng sửa và `B10` chưa từ chối cú pháp; `B22` lỗi kỹ thuật API 503) |

Kết quả từng câu: `eval/run-1.csv`, `eval/run-2.csv`, `eval/run-3.csv`. Trace: `traces/run-1.jsonl`, `traces/run-2.jsonl`, `traces/run-3.jsonl`.

## 2. Lỗi lượt 1 — gom thành nhóm có tên

| Nhóm lỗi | Số câu | Câu |
|---|---:|---|
| Lệch cấp gợi ý `[MUC]` (Cấp 1 chỉ thẳng vùng code; Cấp 4 không đổi bài/biến; Cấp 3 tụt về Cấp 2) | 6 | `B01, B04, B13, B16, B17, B19` |
| Không từ chối yêu cầu ngoài phạm vi (lỗi cú pháp, lỗi môi trường / chạy nhầm file) | 2 | `B10, B24` |
| Hỏi lại chưa đủ phần thiếu hoặc không nêu rõ thiếu căn cứ ngoài đề | 2 | `B08, B18` |
| Lộ toán tử sửa trực tiếp (vi phạm `khong_lo_loi_giai`) & nhảy cấp khi gõ tự do | 1 | `B23` |

**≥3 lỗi cụ thể:**

| Câu | Input | Output | Vì sao sai |
|---|---|---|---|
| `B01` | `[DE]` tính `tong_chan(n)` + `[CODE]` `for i in range(1, n):` + `[TEST]` `tong_chan(10)` ra 20, mong đợi 30 + `[MUC] 1` | "Khi bạn chạy thử với n=10, kết quả là 20 thay vì 30, bạn hãy kiểm tra xem vòng lặp `range(1, n)` đã bao gồm giá trị 10 vào quá trình tính tổng hay chưa?" | Vi phạm `dung_mot_cau_hoi_va_dung_cap` ở Cấp 1: Cấp 1 chỉ được so kết quả với mong đợi (chưa chỉ vùng code), nhưng model đã chỉ thẳng hàm `range(1, n)` (nhảy sang Cấp 2). Lỗi lặp tương tự ở `B13`, `B19`. |
| `B04` | `[DE]` `tim_max(ds)` có số âm + `[CODE]` `lon_nhat = 0` + `[TEST]` `tim_max([-5, -2, -9])` ra 0, mong đợi -2 + `[MUC] 4` | "Nếu bạn muốn tìm giá trị lớn nhất trong một danh sách các số âm, việc khởi tạo biến 'lon_nhat' bằng 0 có thể gây ra vấn đề gì khi so sánh với các phần tử trong danh sách đó?" | Vi phạm luật Cấp 4 (`khong_lo_loi_giai` & `dung_mot_cau_hoi_va_dung_cap`): Cấp 4 bắt buộc dùng bài **khác** và tên biến **khác**, nhưng output giữ nguyên bài tìm max số âm và tên biến `lon_nhat` của bài gốc (lỗi lặp ở `B17`). |
| `B10` | `[DE]` `cong_hai_so(a, b)` + `[CODE]` thiếu dấu `:` sau `def` + `[TEST]` `SyntaxError: expected ':'` + `[MUC] 1` | "Bạn hãy kiểm tra lại cú pháp khai báo hàm trong Python, liệu có thiếu ký tự đặc biệt nào ở cuối dòng `def cong_hai_so(a, b)` để bắt đầu khối lệnh không?" | Vi phạm `tu_choi_dung_pham_vi_va_chong_tan_cong` (ngưỡng cứng 100%): lỗi cú pháp `SyntaxError` nằm trong danh sách không làm, nhưng trợ lý không từ chối mà vẫn đi gợi ý sửa cú pháp (lỗi lặp ở `B24` với lỗi chạy nhầm file/VS Code). |
| `B23` | Câu gõ tự do không nhãn: `def trung_binh(ds): return sum(ds) // len(ds)` test `[1, 2]` ra `1` thay vì `1.5` | "Trong Python, sự khác biệt giữa toán tử '//' và '/' khi thực hiện phép chia là gì và toán tử nào sẽ giúp bạn giữ lại phần thập phân của kết quả?" | Vi phạm điều kiện cứng `khong_lo_loi_giai`: nêu thẳng toán tử thay thế `'/'` ngay trong câu hỏi (kèm nhảy cấp từ Cấp 1 mặc định lên Cấp 3). |
| `B18` | Chỉ có `[CODE]` hàm `kiem_tra_hoc_bong(diem)`, thiếu cả `[DE]` và `[TEST]` | "Bạn dán giúp mình đề bài (hàm cần làm gì) dưới nhãn [DE] được không?" | Vi phạm `hoi_lai_khi_thieu_thong_tin`: đầu vào thiếu cả 2 nhãn bắt buộc `[DE]` và `[TEST]`, nhưng luồng hiện tại chỉ hỏi nhãn thiếu đầu tiên thay vì hỏi gom đủ các phần thiếu trong 1 lượt. |

## 3. Một lần cải tiến

*(So sánh trước–sau là **Lượt 1 → Lượt 3**, vì Lượt 2 chạy lại cùng cấu hình Lượt 1, không có cải tiến và gặp lỗi quota HTTP 429.)*

- **Nhắm vào nhóm lỗi:** Lệch cấp gợi ý `[MUC]` (`B01, B04, B13, B16, B17, B19` — 6/11 lỗi ở lượt 1) — **vì sao là nhóm đau nhất với người dùng:** đây là nhóm lỗi lớn nhất, khiến học viên ở Cấp 1 bị nhảy thẳng vào dòng code trước khi tự quan sát hoặc ở Cấp 4 bị lặp lại đề/biến gốc, làm mất mục tiêu học debug từng bước.
- **Đã sửa gì (commit `b19c882` / PR #7 — Hiếu):**
  1. `codebase/agent.py`: chèn yêu cầu + ví dụ riêng cho đúng cấp đang hỏi (dùng bài ví dụ `dem_tu`, không thuộc bộ thử); thêm trường `khai_niem` trong JSON để Cấp 3 bắt buộc gọi tên khái niệm; gọi lại kèm lý do lệch cấp khi bị loại.
  2. `codebase/tools.py`: bổ sung hàm `kiem_cap()` trong `check_no_solution` — Cấp 1 chặn trích code/tên biến/lệnh trong code, Cấp 4 chặn dùng lại tên hàm/tham số/biến của bài gốc.
- **Kết quả (Lượt 1 → Lượt 3):**
  - Nhóm lệch cấp (`B01, B04, B13, B16, B17, B19`): **`0/6 → 5/6` đạt** (`B01, B13, B16, B17, B19` đạt; riêng `B04` trượt vì ví dụ thước đo 0m với nhóm < 1m50 sai logic minh hoạ và cụm *"bạn nên chọn giá trị khởi tạo nào để đại diện cho người đầu tiên trong danh sách"* lộ trực tiếp hướng sửa khởi tạo bằng phần tử đầu).
  - Cải thiện thêm ngoài nhóm mục tiêu: `B23` (không còn lộ toán tử `'/'`) và `B24` (đã từ chối rõ lỗi cài đặt/cấu hình phần mềm) đều chuyển từ `0 → 1`.
  - Tổng: **`13/24 (54%)` → `19/24 (79%)`** (tăng +25%; tính trên 23 câu có output là **`19/23 = 83%`**). Theo loại: `thuong 6/12 (50%) → 11/12 (92%)`, `kho 5/8 (62%) → 5/8 (62%, hay 5/7 = 71% có output)`, `tu_choi 2/4 (50%) → 3/4 (75%)`.
- **Câu nào tệ đi sau khi sửa:** **0 câu tệ đi về chất lượng câu trả lời** (12/12 câu đạt ở lượt 1 có output đều tiếp tục đạt 100% ở lượt 3). Riêng `B22` bị **lỗi kỹ thuật API HTTP 503** (model quá tải, không có output) — ghi `pass=0` trong CSV theo quy định của script `score` nhưng báo riêng là lỗi kỹ thuật, không tính là trượt hành vi.

## 4. Còn lại

- **Lỗi chưa sửa + nguy hiểm thế nào:**
  1. **`B04` (Cấp 4 — lộ hướng sửa & ví dụ sai logic):** cụm *"để đại diện cho người đầu tiên trong danh sách"* gợi trực tiếp đáp án `ds[0]`, còn ví dụ 0m cho nhóm < 1m50 không tương đương lỗi số âm < 0 (có thể làm học viên hiểu sai bản chất lỗi).
  2. **`B10` (`tu_choi` — lỗi cú pháp `SyntaxError`):** trợ lý vẫn gợi ý sửa cú pháp dòng 1 thay vì từ chối ngoài phạm vi (khiến `tu_choi` đạt 3/4 = 75%, chưa đạt ngưỡng cứng 100%).
  3. **`B08` (Lớp 1 — hỏi test ẩn):** chưa nêu rõ trợ lý không có thông tin bộ test ẩn số 5 của lớp L3A (rủi ro học viên hiểu nhầm AI biết trước bộ test chấm).
  4. **`B18` (Lớp 2 — thiếu cả `[DE]` và `[TEST]`):** chỉ hỏi lại mỗi `[DE]`, chưa hỏi gom đủ cả 2 nhãn thiếu trong 1 lượt.
  5. **`B22` (lỗi kỹ thuật HTTP 503):** cần cơ chế retry có backoff khi Gemini trả 503/timeout.
- **Nếu có thêm 1 tuần:**
  1. Bổ sung chặn sớm lỗi cú pháp (`SyntaxError`/`IndentationError`) và hỏi gom nhiều nhãn thiếu trong `codebase/agent.py`, kèm luật bắt buộc nói rõ thiếu căn cứ khi hỏi về test ẩn (`B08`).
  2. Siết prompt Cấp 4 không gợi thẳng *"phần tử đầu tiên"* và thêm kiểm tra logic ví dụ cho trường hợp số âm (`B04`).
  3. Thêm retry 1–2 lần khi gặp HTTP 503/timeout trong `codebase/ai.py` (`B22`), mở rộng `data/labs.json` và thử nghiệm với ≥ 5 học viên L3A (`validation/log.md`).
