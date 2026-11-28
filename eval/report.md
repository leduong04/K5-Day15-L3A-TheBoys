# Báo cáo đánh giá — lượt 1 → một cải tiến → lượt 3 (sau lượt 2 lỗi quota)

> Điền ở guide bước 4.1. Lượt 1 trước **CP3 10:00 Thứ Bảy 28/11**, lượt sau cải tiến trước **CP4 14:30 Thứ Bảy 28/11**, cùng bộ câu thử 24 câu, cùng cách chấm. Chấm ở rubric R5.
> Số lấy từ `python run.py score eval/run-1.csv` và `eval/run-3.csv` sau khi điền cột `pass`. **Kết quả thấp ghi thật vẫn đủ điểm.**
> Không được: sửa chuẩn "đạt", bỏ câu thử trượt, sửa `expected` cho khớp output, sửa kết quả lượt đã chạy.

## 1. Kết quả

| Lượt | Run ID | Đạt / tổng | % | thuong | kho | tu_choi | So với chuẩn "đạt" |
|---|---|---|---|---|---|---|---|
| 1 | `run-1@20261128-092750` | 13/24 | 54% | 6/12 (50%) | 5/8 (62%) | 2/4 (50%) | **chưa** (< 85%, có 1 câu lộ toán tử sửa `B23` và 2/4 `tu_choi` trượt) |
| 2 | `run-2@20261128-100327` | Chưa chấm / 24 (19 câu có output, 5 câu lỗi API 429) | — | — | — | — | Chưa thể kết luận *(chạy cùng cấu hình lượt 1, lỗi kỹ thuật quota/phút)* |
| 3 | `run-3@20261128-121459` | **22/24** | **92%** | **12/12 (100%)** | **6/8 (75%)** | **4/4 (100%)** | **đạt** (92% ≥ 85%, 100% không lộ lời giải trên 23/23 câu có output, 100% `tu_choi`; lưu ý 1 câu lỗi kỹ thuật `TimeoutError` tại `B23`) |

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

- **Nhắm vào nhóm lỗi:** (1) Lệch cấp gợi ý `[MUC]` (6/11 lỗi, lớn nhất) kết hợp (2) Không từ chối ngoài phạm vi & rò rỉ toán tử sửa (vi phạm ngưỡng cứng 100% của chuẩn "đạt") và (3) Hỏi thiếu nhãn khi thiếu nhiều nhãn — **vì sao là nhóm đau nhất với người dùng:** học viên bị nhảy thẳng vào vùng code ở Cấp 1 hoặc nhận ví dụ trùng đề/lộ toán tử sửa sẽ mất cơ hội tự quan sát và tự debug; trong khi lỗi cú pháp/môi trường không được từ chối sớm sẽ dẫn học viên đi sai phạm vi hỗ trợ.
- **Đã sửa gì (`codebase/agent.py`, `codebase/tools.py`):**
  1. Siết luật từng cấp trong `SYSTEM` prompt kèm ví dụ đúng cho Cấp 1 (cấm nhắc dòng/hàm/từ khoá code), Cấp 3 (bắt buộc gọi tên khái niệm Python), Cấp 4 (bắt buộc bài đời thường và tên biến khác hẳn đề gốc), và luật nêu rõ thiếu căn cứ khi được hỏi về test ẩn.
  2. Nâng cấp `check_no_solution` trong `codebase/tools.py`: chặn trích backtick/từ khoá code ở Cấp 1, chặn dùng lại tên biến/hàm bài gốc trên **toàn bộ câu trả lời** ở Cấp 4 (không chỉ trong backtick), và chặn lộ trực tiếp toán tử thay thế (`'/'` cho `'//'`, `'>='` cho `'>'`, `'+='` cho `'='`).
  3. Thêm bước kiểm tra ngoài phạm vi rõ ràng (lỗi cú pháp `SyntaxError`/`IndentationError`, lỗi môi trường/chạy nhầm file/ngôn ngữ khác) trước khi gọi model (`0` token) và sửa `_hoi_thieu_nhieu` để hỏi gom tất cả các nhãn thiếu trong đúng 1 câu hỏi.
  4. Chạy `python run.py eval --wait 6` tạo lượt mới `eval/run-3.csv` để tránh lỗi quota HTTP 429 của lượt 2.
- **Kết quả:**
  - Nhóm lệch cấp `[MUC]`: **0/6 → 6/6 đạt** (`B01, B04, B13, B16, B17, B19` đều đạt).
  - Nhóm ngoài phạm vi (`tu_choi`): **2/4 (50%) → 4/4 (100%)** (`B10, B24` từ chối đúng với 0 model call).
  - Nhóm hỏi lại nhiều nhãn thiếu (`B18`): **0/1 → 1/1 đạt**.
  - Tổng thể: **`13/24 (54%)` → `22/24 (92%)`** (`thuong`: `50% → 100%`, `kho`: `62% → 75%`, `tu_choi`: `50% → 100%`); đồng thời giảm trung bình số lần gọi model xuống `0.7` lần/câu và `59` token ra/câu.
- **Câu nào tệ đi sau khi sửa:** **0 câu tệ đi về chất lượng câu trả lời** (13/13 câu đạt ở lượt 1 tiếp tục đạt 100% ở lượt 3). Riêng `B23` bị lỗi kỹ thuật `TimeoutError: The read operation timed out` (quá 60 giây chờ phản hồi mạng) nên không có output ở lượt 3 (chấm `0`).

## 4. Còn lại

- **Lỗi chưa sửa + nguy hiểm thế nào:**
  1. **`B08` (thiếu căn cứ về bộ test ẩn — Lớp 1):** Model vẫn gợi mở kiểm tra trường hợp biên `b == 0` nhưng chưa nêu tường minh câu *"mình không có thông tin về bộ test ẩn số 5 của lớp"*. Rủi ro: học viên có thể tưởng trợ lý biết trước nội dung bộ test chấm bài.
  2. **`B23` (lỗi kỹ thuật `TimeoutError` 60s ở 1 câu):** Nếu xảy ra khi demo live hoặc khi học viên dùng thật, người dùng phải chờ 60 giây rồi nhận lỗi.
  3. **Mức gợi ý hơi lộ hướng ở `B02`, `B22`:** Câu hỏi chứa cụm *"thay vì đặt ở bên ngoài / một vị trí khác"* dù không đưa code sửa nhưng vẫn hơi gợi thẳng vị trí đích; cần làm mềm lại thành câu hỏi quan sát giá trị biến qua từng vòng.
- **Nếu có thêm 1 tuần:**
  1. Thêm cơ chế kiểm tra tự động cho câu hỏi về test ẩn/quy ước ngoài đề (bắt buộc có câu khẳng định thiếu căn cứ trước khi hỏi trường hợp biên) và thêm retry 1 lần với timeout 20–25 giây trong `codebase/ai.py` để tránh treo 60 giây như `B23`.
  2. Tinh chỉnh prompt Cấp 2 để không dùng cụm *"thay vì đặt ở bên ngoài"* (chỉ hỏi hiện tượng giá trị biến thay đổi sau mỗi vòng).
  3. Mở rộng `data/labs.json` từ 5 bài lên 15–20 bài Mini Lab thật của khoá L3A/L3B (đã ẩn danh) và kiểm thử với ≥ 5 học viên thật để đo xem học viên có tự sửa được bug trong ≤ 3 cấp gợi ý không.
