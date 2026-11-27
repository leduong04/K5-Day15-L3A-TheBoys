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

## Dataset 2 · Căn cứ Mini Lab cho prototype

Chưa có bộ dữ liệu runtime được chốt ở CP2. Dự kiến nhóm tự viết 3–5 bài mẫu, gắn nhãn `synthetic`, kiểm tay trước khi dùng; đây không phải bằng chứng pain. Hiếu phụ trách tạo và cập nhật data này trong chặng CP2/CP3 theo phân công ở `spec.md` §10.

## Dataset 3 · Bộ câu thử Python Mini Lab (`eval/benchmark.csv`)

| | |
|---|---|
| Dùng để làm gì | Đánh giá chất lượng bản chạy thử Socratic Debugger qua `python run.py eval` (`thuong`, `kho`, `tu_choi`). |
| Từ đâu | Kết hợp: (1) nhóm tự viết chuẩn định dạng `[DE] [CODE] [TEST] [MUC]` (`tu_viet`, đã dựng 12 câu gồm 4 `thuong` đủ 4 cấp + 5 `kho` + 3 `tu_choi` trong đó có 2 câu tấn công); (2) lỗi Python Mini Lab thực tế thu thập từ phỏng vấn học viên L3A (`nguoi_dung`, đang chờ ghép bổ sung từ Văn trước CP2 và mở rộng lên 20–30 câu trước CP3). |
| Xử lý những bước gì | Chuẩn hoá đầu vào theo đúng nhãn `[DE]`, `[CODE]`, `[TEST]` (bắt buộc) và `[MUC]`, `[DA_THU]` (tuỳ chọn) ở `spec.md` §4; xoá thông tin cá nhân học viên; gắn nhãn `type`, `source` và `pass_criterion` kiểm chứng được. |
| Số dòng / số đoạn | Hiện có 12 câu khung `tu_viet` (mục tiêu CP2: ≥10 câu và ≥1/3 nguồn thật; CP3: 20–30 câu). |
| Phiên bản / ngày lấy | 27/11/2026 (bản đầu trước CP2). |
| Nhãn | Kết hợp thật (`nguoi_dung`) và tự biên soạn (`tu_viet`). |
| Giới hạn | Phần `tu_viet` tập trung kiểm tra 4 cấp gợi ý, hành vi biên, thiếu thông tin và chống ép giải hộ — **không dùng làm bằng chứng pain**. Cần bổ sung ≥1/3 số câu từ phỏng vấn người dùng thật trước khi chốt CP2. |
