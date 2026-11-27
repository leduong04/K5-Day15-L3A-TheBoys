# Data card — dữ liệu bản chạy thử và dữ liệu phân tích

> CP2 bản đầu. Dữ liệu BTC gốc không được chép vào repo và không được dùng làm căn cứ runtime cho prototype.

## Dataset 1 · Dữ liệu hành vi pre-class của BTC (chỉ phân tích bằng chứng)

| | |
|---|---|
| Dùng để làm gì | Đếm mô tả hoạt động học để kiểm tra sơ bộ pain; **không** cấp dữ liệu cho `lookup_lab` và không dùng để tạo câu trả lời prototype. |
| Từ đâu | Gói BTC cấp ở `../data/preclass/` (ngoài repo nhóm). Phân tích chính dùng `answers.csv`; diễn giải dựa trên `column_dictionary.csv` và `event_types.csv`. |
| Xử lý những bước gì | Lọc các dòng `nguon = thuc_hanh`, tách các dòng có nhãn chấm đúng/sai; đếm lượt sai và cặp học viên–bài thử lại. Mã học viên chỉ dùng trong phép nhóm; script không in mã. Không sao chép dữ liệu gốc. Script: `evidence/count_preclass.py`. |
| Số dòng / số đoạn | `answers.csv` có 3.776 dòng; trong đó 519 dòng thực hành có nhãn đúng/sai hợp lệ. Kết quả đếm sơ bộ ở `evidence/data-mining.md`. |
| Phiên bản / ngày lấy | Gói BTC cấp; thời gian `created_at` trong bảng trả lời: 2026-11-05–2026-11-25 (UTC); phân tích sơ bộ 2026-11-27. |
| Nhãn | Dữ liệu hành vi khoá học, mã học viên đã giả danh hoá theo từ điển BTC. |
| Giới hạn | Bài trong gói là nội dung AI/agent, không đại diện trực tiếp cho Python Mini Lab; đúng/sai và số lần trả lời không giải thích nguyên nhân, không chứng minh lỗi logic hoặc pain. Chỉ dùng như tín hiệu thăm dò, cần kiểm lại qua phỏng vấn đúng người dùng. |

## Dataset 2 · Căn cứ Mini Lab cho prototype (`data/labs.json`)

| | |
|---|---|
| Dùng để làm gì | Nguồn cho công cụ `lookup_lab` (`codebase/tools.py`): đưa đề, test mẫu và lỗi hay gặp cho model làm căn cứ khi chọn chỗ nghi sai |
| Từ đâu | Nhóm tự viết theo kiểu bài Python cơ bản; **không** chép nguyên văn đề của khoá |
| Xử lý những bước gì | Mỗi bài gồm mã (`LAB-01`…), tên hàm, đề, 3 test mẫu, từ khoá để tìm, 2 lỗi hay gặp có mã (`LAB-01-E1`…). Lỗi hay gặp chỉ **mô tả** hiện tượng, **không** có code đã sửa, để model không có lời giải mà chép |
| Số dòng / số đoạn | 5 bài · 10 lỗi hay gặp (off-by-one ở `range`, điều kiện chẵn/lẻ, biến đếm khởi tạo trong vòng lặp, phân biệt hoa thường, giá trị khởi tạo sai, `return` trong vòng lặp, chia lấy nguyên, sai mẫu số, nhầm `and`/`or`, thiếu điều kiện chia hết cho 400) |
| Phiên bản / ngày lấy | v1 · 27/11/2026 |
| Nhãn | `synthetic` |
| Giới hạn | Chỉ 5 dạng bài ngắn một hàm; chưa phủ hết Mini Lab thật; lệch về lỗi vòng lặp và điều kiện. Không tìm thấy bài thì `lookup_lab` trả rỗng và trợ lý chỉ dựa vào đề học viên dán. Sẽ bổ sung bài từ code lỗi thật (đã ẩn danh) khi có từ phỏng vấn |

**Cách sinh:** viết tay với hỗ trợ của AI (Claude Code) theo danh sách lỗi logic hay gặp ở `spec.md` §4; không dùng seed. **Người kiểm:** Hiếu (có AI hỗ trợ) — **5/5 bài** đạt: đề rõ, có tên hàm; **15/15 test mẫu đúng** (đối chiếu bằng lời giải tham chiếu chạy riêng, không đưa vào repo); **10/10 mô tả lỗi** không chứa code hay cách sửa. Khi kiểm phát hiện từ khoá `range` ở LAB-01 làm `lookup_lab` khớp nhầm bài khác → đã bỏ và nâng ngưỡng khớp (trùng tên hàm hoặc ≥3 từ khoá). Data tự dựng **không phải bằng chứng pain**.

## Dataset 3 · Bộ câu thử Python Mini Lab (`eval/benchmark.csv`)

| | |
|---|---|
| Dùng để làm gì | Đánh giá chất lượng bản chạy thử Socratic Debugger qua `python run.py eval` (`thuong`, `kho`, `tu_choi`). |
| Từ đâu | Kết hợp 12 câu nhóm tự viết (`tu_viet`, `B01`–`B12`) và 6 câu nguồn `nguoi_dung` (`B13`–`B18`) tái hiện từ mô tả tình huống lỗi logic Python Mini Lab và cách hỏi thực tế trong 4 biên bản phỏng vấn `evidence/interviews/P1.md`–`P4.md` (do người được phỏng vấn không lưu file code gốc). |
| Xử lý những bước gì | Chuẩn hoá đầu vào theo đúng nhãn `[DE]`, `[CODE]`, `[TEST]` (bắt buộc) và `[MUC]`, `[DA_THU]` (tuỳ chọn) ở `spec.md` §4; ẩn danh người học; gắn nhãn `type`, `source` (ghi rõ tái hiện từ mô tả phỏng vấn) và `pass_criterion` kiểm chứng được. |
| Số dòng / số đoạn | 18 câu: 9 `thuong`, 6 `kho`, 3 `tu_choi` (gồm 2 câu tấn công `B11`, `B12`). Nguồn: 6 `nguoi_dung` (6/18 = 33,3% ≥ 1/3) · 12 `tu_viet`. |
| Phiên bản / ngày lấy | v2 CP2 · 27/11/2026. |
| Nhãn | Kết hợp `nguoi_dung` (tái hiện từ mô tả phỏng vấn `P1`–`P4`) và `tu_viet`. |
| Giới hạn | Bộ câu đã đạt ngưỡng CP2 (≥10 câu, ≥5 `kho`, ≥2 `tu_choi`, ≥1/3 nguồn `nguoi_dung`), nhưng các câu `nguoi_dung` được tái hiện từ mô tả lời kể do học viên không lưu bản code gốc; cần tiếp tục mở rộng lên 20–30 câu cho CP3 (và ưu tiên xin code lỗi gốc đã ẩn danh nếu có thêm người dùng gửi). |
