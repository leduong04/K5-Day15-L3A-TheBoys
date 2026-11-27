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
