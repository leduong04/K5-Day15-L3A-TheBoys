# Data card — dữ liệu bản chạy thử dùng

> Điền ở guide bước 2.4 (bản đầu ở CP2, đủ ở CP3). Ôn lại: ngày 6 · lab ngày 6. Chấm ở rubric R4.
> Một trang. Mỗi dataset một mục. Dữ liệu chạy thử (bài mẫu, thông báo mẫu, đoạn transcript…) để trong thư mục `data/` này.
> Không commit nguyên tài liệu khoá, dữ liệu cá nhân thật hay nguyên file data BTC cấp — chỉ đoạn trích ngắn, bản viết lại, hoặc số đã tổng hợp.

## Dataset 1 · Dữ liệu hành vi pre-class (BTC cấp — Track A)

| | |
|---|---|
| Dùng để làm gì | Đào bằng chứng khó khăn học tập (`evidence/data-mining.md`) và tham chiếu ngữ cảnh dựng câu thử `data_that` |
| Từ đâu | Data BTC cấp trong repo đề (bảng `events`, `answers`, `chat` — không commit nguyên file vào repo) |
| Xử lý những bước gì | Lọc các bản ghi liên quan câu hỏi / bài tập thực hành · ẩn danh mã/tên học viên · tổng hợp số liệu *(đang chờ Dương bổ sung tên script và chi tiết lọc)* |
| Số dòng / số đoạn | __ *(chờ Dương cập nhật sau khi phân tích)* |
| Phiên bản / ngày lấy | 27/11/2026 |
| Nhãn | thật |
| Giới hạn | Dữ liệu hành vi pre-class chỉ cho thấy dấu hiệu khó khăn trong quá trình học, không mặc định toàn bộ là lỗi logic Python (như đã lưu ý ở `canvas.md` dòng 4); cần đối chiếu thêm phỏng vấn học viên lớp L3A. |

## Dataset 2 · Bộ câu thử Python Mini Lab (`eval/benchmark.csv`)

| | |
|---|---|
| Dùng để làm gì | Đánh giá chất lượng bản chạy thử Socratic Debugger qua `python run.py eval` (`thuong`, `kho`, `tu_choi`) |
| Từ đâu | Kết hợp: (1) nhóm tự viết chuẩn định dạng `[DE] [CODE] [TEST] [MUC]` (`tu_viet`, đã dựng 12 câu gồm 4 `thuong` đủ 4 cấp + 5 `kho` + 3 `tu_choi` trong đó có 2 câu tấn công); (2) lỗi Python Mini Lab thực tế thu thập từ phỏng vấn học viên L3A (`nguoi_dung`) và dữ liệu BTC (`data_that`) *(đang chờ ghép bổ sung từ Văn/Dương trước CP2 và mở rộng lên 20–30 câu trước CP3)* |
| Xử lý những bước gì | Chuẩn hoá đầu vào theo đúng nhãn `[DE]`, `[CODE]`, `[TEST]` (bắt buộc) và `[MUC]`, `[DA_THU]` (tuỳ chọn) ở `spec.md` §4; xoá thông tin cá nhân học viên; gắn nhãn `type`, `source` và `pass_criterion` kiểm chứng được |
| Số dòng / số đoạn | Hiện có 12 câu khung `tu_viet` (mục tiêu CP2: ≥10 câu và ≥1/3 nguồn thật; CP3: 20–30 câu) |
| Phiên bản / ngày lấy | 27/11/2026 (bản đầu trước CP2) |
| Nhãn | kết hợp thật (`nguoi_dung`, `data_that`) và tự biên soạn (`tu_viet`) |
| Giới hạn | Phần `tu_viet` tập trung kiểm tra hành vi biên, thiếu thông tin và chống ép giải hộ — **không dùng làm bằng chứng pain**. Cần bổ sung ≥1/3 số câu từ người dùng/dữ liệu thật trước khi chốt CP2. |
