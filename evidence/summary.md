# Tổng hợp bằng chứng pain

> Tổng hợp từ phỏng vấn CP2 ngày 27/11/2026 (4 người: 3 học viên, 1 lab coach) và khảo sát 20 học viên (Discord lớp và nhóm Zalo lớp, 18:00–19:00 27/11/2026; đưa vào repo sau CP2). Chỉ ghi vai và mã, không ghi tên.

## 1. Nguồn đã dùng

| Nguồn | Đạt ngưỡng? | File |
|---|---|---|
| Đào data (x/N, %, cách đếm chạy lại được, ≥5 ví dụ) | Chưa đạt cho pain đã chọn; bộ pre-class không ghi trực tiếp Python Mini Lab | `evidence/data-mining.md` |
| Phỏng vấn (≥3 người ngoài nhóm, đúng người dùng) | Có 3 học viên ngoài nhóm, nhưng chỉ 2 thuộc cohort mục tiêu L3A; vế thời gian của ngưỡng đạt (2/3 mất ≥30 phút), vế "lấy lời giải vẫn không giải thích được" chưa đạt | `evidence/interviews/P1.md`–`P4.md` |
| Khảo sát (≥20 người ngoài nhóm, đúng người dùng) | Vừa đủ số lượng: 20 câu trả lời (11 L3A, 9 L3B), 19 người đã gặp tình huống; nhưng chỉ 11 thuộc cohort mục tiêu L3A; cả 20 người ở ngoài nhóm (Văn xác nhận 28/11) | `evidence/survey/results.csv`, `questions.md`, `count_survey.py` |

## 2. Số chính

- Phỏng vấn học viên: **3/3** kể được lần gần đây code chạy nhưng cho kết quả sai; trong đó **2/2 học viên L3A** (P1, P3) và 1 học viên L3B (P2). Cả ba nói phần tốn công nhất là tìm lỗi logic.
- Thời gian lần gần nhất: P1 **30 phút**, P2 **30 phút**, P3 **20 phút**. Tần suất tự báo trong một tháng: P1 **3**, P2 **2**, P3 **4** lần. P2 là L3B; không gộp để suy ra tỉ lệ cho L3A.
- Lab coach P4 nhớ khoảng **4 lượt hỏi trong một buổi khoảng 18 học viên**, mỗi lượt tốn **5–10 phút**; không nhớ số học viên phải chờ chính xác.
- Đào data: **23/519 (4,4%)** dòng trả lời thực hành bị chấm sai; **16/503 (3,2%)** cặp học viên–bài có từ hai lượt. Đây là dữ liệu nội dung AI/agent, không đo lỗi Python Mini Lab; không dùng làm bằng chứng trực tiếp cho pain.
- Khảo sát (n=20; 19 người đã gặp tình huống, 1 người L3A chưa gặp; đếm bằng `python evidence/survey/count_survey.py`):
  - Chỗ mất thời gian nhất là **tìm chỗ sai logic: 14/19** (L3A 7/10, L3B 7/9); hiểu đề 4/19; lỗi cú pháp / môi trường 1/19.
  - Thời gian lần gần nhất: dưới 5 phút 2/19 · 5–15 phút 3/19 · **trên 30 phút 14/19** (không ai chọn 15–30 phút). Riêng L3A: trên 30 phút **6/10** (5–15 phút 2/10, dưới 5 phút 2/10). L3B: trên 30 phút **8/9**.
  - Kết quả: xong 12/19 · xong một phần 5/19 · bỏ 2/19.
  - Tự giải thích được vì sao code cũ sai: có 8/19 · chỉ hiểu một phần 7/19 · không 2/19 · không dùng lời giải 2/19. L3A: có 6/10.
  - **Trong 8 người đã dán code vào ChatGPT/AI hoặc xem lời giải có sẵn: 0/8 trả lời "Có, giải thích được"** (6 chỉ hiểu một phần, 1 không, 1 ghi "không dùng lời giải" — mâu thuẫn với câu trước, xem `questions.md`).
  - Số lần gặp trong 1 tuần qua: trung vị 3 (L3A), 2 (L3B) — tự báo.
  - Cách xoay xở (chọn nhiều, 16 câu hợp lệ): tự đọc lại code 10 · `print` 8 · ChatGPT/AI 7 · chạy tay input nhỏ 6 · hỏi bạn 4 · xem lời giải 2 · bỏ qua 1.

| | Vai | Gặp pain? | Số lần / 1 tháng qua | Lần gần nhất mất | Đang xoay xở bằng |
|---|---|---:|---:|---:|---|
| P1 | Học viên L3A | Có | 3 | 30 phút | Đọc lại code, `print`, input nhỏ |
| P2 | Học viên L3B | Có | 2 | 30 phút | Tự rà rồi hỏi bạn, thử giá trị |
| P3 | Học viên L3A | Có | 4 | 20 phút | Thử input biên, hỏi ChatGPT rồi đối chiếu đề |
| P4 | Lab coach | Có gặp ca tương tự | 4 lượt trong buổi gần nhất | 5–10 phút/lượt | Hỏi dự đoán từng bước, input nhỏ, `print` |

**Đối chiếu với ngưỡng đã ghi trước ở `evidence/hypothesis.md`:** đạt một vế. Vế thời gian (≥2/3 học viên mất ≥30 phút) **đạt**: P1=30, P2=30, P3=20 phút → 2/3; nhưng trong hai học viên L3A chỉ P1 ở mốc 30 phút (P2 thuộc L3B). Vế thứ hai **chưa đạt**: chưa có bằng chứng trực tiếp rằng học viên sau khi nhận lời giải vẫn không giải thích được lỗi của mình; P1–P3 đều nói cuối cùng hiểu nguyên nhân. P4 kể một trường hợp ban đầu chưa giải thích được sau khi dùng lời giải AI, nhưng sau khi coach cùng chạy từng bước thì học viên giải thích lại được.

## 3. Trích dẫn nguyên văn (đã bỏ tên)

1. “Em thử input nhỏ thì thấy tổng bị thiếu đúng lượt cuối.” — P1, học viên L3A.
2. “In biến ra từng vòng là em tìm được chỗ lệch.” — P1, học viên L3A.
3. “Em cứ nhìn vào công thức mà không để ý danh sách đã bị lọc bớt phần tử.” — P2, học viên L3B.
4. “Bạn em chỉ bảo kiểm tra mẫu số, rồi em tự thấy chỗ sai.” — P2, học viên L3B.
5. “Lúc thấy giá trị đúng ngay ở ngưỡng thì em hiểu vì sao dấu so sánh bị lệch.” — P3, học viên L3A.
6. “Có bạn chép được cách sửa nhưng chưa nói được vì sao; đổi input là lộ ra ngay.” — P4, lab coach.
7. “Đọc lời giải xong vẫn không biết cách tự tìm lỗi ở bài tương tự.” — khảo sát S13, học viên L3B.
8. “Không biết nên kiểm tra từ đầu vào, vòng lặp hay điều kiện trước.” — khảo sát S06, học viên L3A.
9. “AI gợi ý sửa được nhưng mình chưa hiểu hết vì sao kết quả ban đầu lệch.” — khảo sát S02, học viên L3B.
10. “Có đáp án nhanh nhưng đôi khi AI giải thích dài và khó biết phần nào cần chú ý.” — khảo sát S05, học viên L3A.
11. “Bạn chỉ ra biến bị ghi đè; muốn có cách tự phát hiện lần sau.” — khảo sát S16, học viên L3A.

## 4. Các nguồn có khớp nhau không

Phỏng vấn và coach đều kể các trường hợp lỗi logic; người học dùng input nhỏ, `print`, hỏi bạn hoặc ChatGPT để khoanh vùng và cuối cùng tự giải thích được nguyên nhân. Điều này ủng hộ hướng gợi ý từng bước hơn là đưa lời giải, nhưng chưa chứng minh nhu cầu mạnh hoặc mức tiết kiệm thời gian. Data pre-class không khớp trực tiếp với bài Python nên chỉ được xem là ngữ cảnh, không phải xác nhận độc lập.

Khảo sát khớp với phỏng vấn ở hai điểm: chỗ tốn công nhất là tìm lỗi logic (14/19), và người học dùng đọc lại code, `print`, input nhỏ. Khảo sát bổ sung điều phỏng vấn chưa có: người dùng AI / lời giải thường chỉ hiểu một phần (0/8 tự giải thích được đầy đủ). Về thời gian, khảo sát và phỏng vấn **cùng hướng**: trong khảo sát, 6/10 học viên L3A và 8/9 học viên L3B tự báo lần gần nhất mất trên 30 phút; trong phỏng vấn, P1 (L3A) và P2 (L3B) mất 30 phút, P3 (L3A) 20 phút. Cả hai đều là số tự báo, khảo sát chỉ cho chọn theo khoảng.

## 5. Kết luận

Giả thuyết ban đầu: **đúng một phần**. Có tình huống code chạy nhưng kết quả sai ở học viên L3A, và các em tự báo tốn thời gian tìm lỗi logic. Vế thời gian của ngưỡng đạt: 2/3 học viên được phỏng vấn mất ≥30 phút (P1 L3A, P2 L3B; P3 L3A mất 20 phút), và cả ba đều tự tìm được cách kiểm chứng. Từ phỏng vấn, chưa có bằng chứng rằng người học vẫn không hiểu sau khi nhận trợ giúp (khảo sát bổ sung bên dưới). Giữ lát cắt gợi ý Socratic như giả thuyết sản phẩm cần kiểm thêm; không tuyên bố đây là pain phổ biến hoặc đã được chứng minh.

Bổ sung từ khảo sát (sau CP2): vế thứ hai của giả thuyết — có người lấy lời giải mà vẫn không tự giải thích được — **có dấu hiệu ủng hộ**: trong 8 người dùng AI / lời giải, không ai tự giải thích được đầy đủ (S13 trả lời "Không"). Về thời gian, khảo sát cho thấy **6/10 học viên L3A** (và 8/9 L3B) tự báo trên 30 phút — cùng hướng với phỏng vấn (vế thời gian đạt 2/3). Khảo sát là tự báo, gửi một lần, chưa có ngưỡng đặt trước riêng cho khảo sát trong `evidence/hypothesis.md`, nên chỉ dùng làm bằng chứng bổ sung.

Điều còn chưa biết: thời gian xử lý đo thật (khảo sát chỉ là tự báo theo khoảng); tỉ lệ học viên L3A gặp tình huống này; các em có muốn dùng một công cụ riêng thay cho `print`/bạn/ChatGPT không; ảnh hưởng đến việc hoàn thành bài.

## Lịch hẹn CP2

| Vai | Giờ hẹn | Đã xong? |
|---|---|---|
| Học viên L3A (P1) | 18:00 27/11 | ✅ |
| Học viên L3B (P2) | 18:15 27/11 | ✅ |
| Học viên L3A (P3) | 18:30 27/11 | ✅ |
| Lab coach (P4) | 18:45 27/11 | ✅ |
