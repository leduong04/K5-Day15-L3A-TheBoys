# Khảo sát — bộ câu hỏi Google Form

- Kênh đã gửi: __ (vd nhóm chat lớp L3A, L3B)
- Giờ mở: __ · giờ chốt: __ (trước 10:00 T7 28/11)
- Ngưỡng: ≥20 người ngoài nhóm, đúng người dùng. Không thu tên, email, mã học viên.
- Google Form: tắt "Thu thập địa chỉ email" (Cài đặt → Câu trả lời).

## Tiêu đề form

Khi code Python chạy được mà ra kết quả sai — bạn xử lý thế nào?

## Mô tả form

Nhóm The Boys (AI20K) đang tìm hiểu cách học viên xử lý khi code Python Mini Lab chạy không báo lỗi nhưng ra kết quả sai. Form mất khoảng 2 phút, không giới thiệu sản phẩm, không thu tên hay email. Cảm ơn bạn!

## Câu hỏi

| # | Câu hỏi | Kiểu trong Google Form | Lựa chọn |
|---|---|---|---|
| 1 | Bạn là: | Trắc nghiệm (chọn một) · bắt buộc | Học viên L3A · Học viên L3B · Lab coach / TA · Khác |
| 2 | Lần gần nhất bạn gặp code Python (Mini Lab hoặc bài tập) chạy được, không báo lỗi, nhưng ra kết quả sai là khi nào? | Trắc nghiệm · bắt buộc | Hôm nay · Tuần này · Tuần trước · Lâu hơn · Chưa bao giờ |
| 3 | Trong 1 tuần qua, bạn gặp chuyện đó mấy lần? | Trả lời ngắn (chỉ nhập số) · bắt buộc | Xác thực câu trả lời: Số, ≥ 0 |
| 4 | Lần gần nhất đó, bạn đã làm gì? (chọn tất cả việc đã làm) | Hộp kiểm (chọn nhiều) · bắt buộc | Tự đọc lại code · In giá trị trung gian (print) · Chạy tay với input nhỏ · Hỏi bạn · Hỏi lab coach / TA · Dán code vào ChatGPT / AI khác · Xem lời giải có sẵn · Bỏ qua · Khác |
| 5 | Từ lúc thấy sai đến lúc sửa xong (hoặc bỏ) mất khoảng bao lâu? | Trắc nghiệm · bắt buộc | Dưới 5 phút · 5–15 phút · 15–30 phút · Trên 30 phút |
| 6 | Lần đó có sửa xong không? | Trắc nghiệm · bắt buộc | Xong · Xong một phần · Bỏ |
| 7 | Lần đó, chỗ nào làm bạn mất thời gian nhất? | Trắc nghiệm · bắt buộc | Hiểu đề / yêu cầu · Lỗi cú pháp, cài đặt, chạy file · Tìm chỗ sai trong logic · Khác |
| 8 | Nếu lần đó bạn có lời giải (từ ChatGPT, bạn bè, đáp án), sau đó bạn có tự giải thích được vì sao code cũ sai không? | Trắc nghiệm · bắt buộc | Có, giải thích được · Chỉ hiểu một phần · Không · Không dùng lời giải |
| 9 | Điều gì khó chịu nhất ở lần đó? | Đoạn văn · không bắt buộc | — |
| 10 | (Tuỳ chọn) Bạn có sẵn lòng cho nhóm hỏi thêm 10 phút không? | Trả lời ngắn · không bắt buộc | Để lại cách liên hệ nếu đồng ý |

## Khi chốt form

- Xuất kết quả: tab Câu trả lời → biểu tượng Sheets → Tải xuống CSV.
- **Xoá cột câu 10 và cột dấu thời gian** trước khi lưu thành `evidence/survey/results.csv`. Bản gốc có liên hệ thì **không** commit.
- Đếm theo vai (câu 1), không cộng chung học viên với lab coach. Dưới 10 người thì chỉ ghi x/n, không ghi %.
- Số chính và ≥3 câu trả lời nguyên văn (câu 9) chép sang `evidence/summary.md`.
