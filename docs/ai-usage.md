# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Code bản chạy thử (rà soát CP2) | Codex | Rà hợp đồng một câu hỏi và sửa validator để loại output không có đúng một dấu `?`. | Đã kiểm nhanh với một câu có/không có dấu hỏi; chưa kiểm output model thật. | Lê Đoàn Dương |
| Prompt / thiết kế lời gọi mô hình | | | | |
| Đào data (viết script đếm, gợi ý nhãn) | Codex | Viết `evidence/count_preclass.py`, chạy phép đếm trên bảng BTC và soạn phần mô tả tổng hợp; không chép file gốc vào repo. | Script chạy lại cho cùng số; Dương/nhóm cần rà cách lọc và giới hạn suy luận trước khi nộp. | Lê Đoàn Dương |
| Rà câu hỏi phỏng vấn / khảo sát | | Chỉ rà câu dẫn dắt | | |
| Viết câu thử (benchmark) | | | Mỗi câu thử có `source`; câu thử AI viết được ghi rõ | |
| Sinh data `synthetic` (nếu có) | Claude Code (theo data card) | Hỗ trợ soạn 5 bài Mini Lab mẫu và 10 mô tả lỗi; không dùng làm bằng chứng pain. | Theo `data/DATA_CARD.md`: Hiếu kiểm 5/5 bài, 15/15 test mẫu và 10/10 mô tả lỗi. | Nguyễn Cảnh Hiếu |
| Chấm cột `pass` bằng LLM (nếu có) | | | Kiểm tra thủ công __ câu thử, khớp __/__ | |
| Slide, spec và persona | Codex | Soạn nháp các mục CP3 spec từ P1–P4; tìm nguồn chính thức cho giải pháp tương tự và giá model; chuyển tần suất phỏng vấn thành giả định persona, ghi rõ giới hạn mẫu. | Nhóm cần rà lại trích dẫn, phép tính và giả định mở rộng từ n nhỏ trước khi nộp. | Lê Đoàn Dương |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
