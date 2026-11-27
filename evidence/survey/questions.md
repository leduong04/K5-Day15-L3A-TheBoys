# Khảo sát — bộ câu hỏi, kênh gửi, thời gian

- Người làm: TV2 (Văn)
- Kênh đã gửi: Discord lớp, nhóm zalo 
- Giờ mở form: 18:00 27/11/2026 · giờ chốt: 19:00 27/11/2026. Câu trả lời đầu tiên lúc 18:04 27/11/2026, câu cuối lúc 18:54 27/11/2026 (theo cột dấu thời gian).
- Số câu trả lời: 20 (11 học viên L3A, 9 học viên L3B). Form không thu tên, email hay mã học viên; cột "Liên hệ follow-up" để trống ở cả 20 câu trả lời và đã bỏ khỏi `results.csv`.
- Bản gốc xuất từ Google Form **không** commit. `results.csv` khác bản gốc đúng 3 điểm, không sửa câu trả lời nào:
  1. **Thêm cột `id`** (S01–S20, theo đúng thứ tự dòng của bản xuất) do nhóm tự đánh để trích dẫn được từng câu trả lời mà không cần tên — cột này không có trong form.
  2. Đổi tiêu đề cột sang tên ngắn không dấu (bảng đối chiếu ở mục "Câu hỏi" bên dưới).
  3. Bỏ cột "Liên hệ follow-up" (trống ở cả 20 dòng).
- Đếm lại: `python evidence/survey/count_survey.py`.

## Câu hỏi

> Ghi theo tiêu đề cột của bản xuất. *(Văn kiểm lại: nếu câu trong form dài hơn tiêu đề cột thì chép nguyên văn câu trong form vào đây.)*

| # | Câu hỏi (tiêu đề cột) | Cột trong `results.csv` | Kiểu trả lời · các đáp án thấy trong kết quả |
|---|---|---|---|
| 1 | Bạn là | `ban_la` | Chọn một · Học viên L3A / Học viên L3B |
| 2 | Lần gần nhất gặp lỗi | `lan_gan_nhat` | Chọn một · Tuần này / Tuần trước |
| 3 | Số lần trong 1 tuần qua | `so_lan_1_tuan` | Số |
| 4 | Đã làm gì (chọn nhiều) | `da_lam_gi` | Chọn nhiều · Tự đọc lại code / In giá trị trung gian (print) / Chạy tay với input nhỏ / Dán code vào ChatGPT / AI khác / Hỏi bạn / Xem lời giải có sẵn / Bỏ qua / Chưa gặp trường hợp này |
| 5 | Thời gian xử lý | `thoi_gian` | Chọn một · Dưới 5 phút / 5–15 phút / 15–30 phút / Trên 30 phút |
| 6 | Kết quả | `ket_qua` | Chọn một · Xong / Xong một phần / Bỏ |
| 7 | Khó khăn mất thời gian nhất | `kho_nhat` | Chọn một + Other · Tìm chỗ sai trong logic / Hiểu đề / yêu cầu / Lỗi cú pháp, cài đặt, chạy file |
| 8 | Tự giải thích được vì sao code cũ sai? | `tu_giai_thich` | Chọn một · Có, giải thích được / Chỉ hiểu một phần / Không / Không dùng lời giải |
| 9 | Điều khó chịu nhất | `kho_chiu_nhat` | Đoạn văn |
| 10 | Liên hệ follow-up | *(đã bỏ)* | Tuỳ chọn · cả 20 câu để trống |

## Câu trả lời có vấn đề (giữ nguyên trong `results.csv`, xử lý khi đếm)

- **S18** chọn "Chưa gặp trường hợp này" → không tính vào các số về tình huống gặp lỗi (mẫu số còn 19).
- **S04, S11, S19**: câu 4 "Đã làm gì" ghi tên vai ("Học viên L3A" / "Học viên L3B") thay vì cách xoay xở → bỏ khỏi phép đếm cách xoay xở (mẫu số 16), các câu khác vẫn tính.
- **S10** chọn "Xem lời giải có sẵn" ở câu 4 nhưng câu 8 chọn "Không dùng lời giải" → hai câu mâu thuẫn, giữ nguyên, ghi chú khi đọc số.
