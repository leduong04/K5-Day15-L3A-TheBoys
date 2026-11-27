# Tổng hợp bằng chứng pain

> Tổng hợp ban đầu từ phỏng vấn CP2 ngày 27/11/2026. Phỏng vấn 4 người (3 học viên, 1 lab coach); mẫu nhỏ, chỉ ghi vai và mã phỏng vấn.

## 1. Nguồn đã dùng

| Nguồn | Đạt ngưỡng? | File |
|---|---|---|
| Đào data (x/N, %, cách đếm chạy lại được, ≥5 ví dụ) | Chưa đạt cho pain đã chọn; bộ pre-class không ghi trực tiếp Python Mini Lab | `evidence/data-mining.md` |
| Phỏng vấn (≥3 người ngoài nhóm, đúng người dùng) | Có 3 học viên ngoài nhóm, nhưng chỉ 2 thuộc cohort mục tiêu L3A; ngưỡng giả thuyết về thời gian chưa đạt | `evidence/interviews/P1.md`–`P4.md` |
| Khảo sát (≥20 người ngoài nhóm, đúng người dùng) | Chưa thực hiện | `evidence/survey/` |

## 2. Số chính

- Phỏng vấn học viên: **3/3** kể được lần gần đây code chạy nhưng cho kết quả sai; trong đó **2/2 học viên L3A** (P1, P3) và 1 học viên L3B (P2). Cả ba nói phần tốn công nhất là tìm lỗi logic.
- Thời gian lần gần nhất: P1 **15 phút**, P2 **30 phút**, P3 **20 phút**. Tần suất tự báo trong một tháng: P1 **3**, P2 **2**, P3 **4** lần. P2 là L3B; không gộp để suy ra tỉ lệ cho L3A.
- Lab coach P4 nhớ khoảng **4 lượt hỏi trong một buổi khoảng 18 học viên**, mỗi lượt tốn **5–10 phút**; không nhớ số học viên phải chờ chính xác.
- Đào data: **23/519 (4,4%)** dòng trả lời thực hành bị chấm sai; **16/503 (3,2%)** cặp học viên–bài có từ hai lượt. Đây là dữ liệu nội dung AI/agent, không đo lỗi Python Mini Lab; không dùng làm bằng chứng trực tiếp cho pain.
- Khảo sát: chưa có.

| | Vai | Gặp pain? | Số lần / 1 tháng qua | Lần gần nhất mất | Đang xoay xở bằng |
|---|---|---:|---:|---:|---|
| P1 | Học viên L3A | Có | 3 | 15 phút | Đọc lại code, `print`, input nhỏ |
| P2 | Học viên L3B | Có | 2 | 30 phút | Tự rà rồi hỏi bạn, thử giá trị |
| P3 | Học viên L3A | Có | 4 | 20 phút | Thử input biên, hỏi ChatGPT rồi đối chiếu đề |
| P4 | Lab coach | Có gặp ca tương tự | 4 lượt trong buổi gần nhất | 5–10 phút/lượt | Hỏi dự đoán từng bước, input nhỏ, `print` |

**Đối chiếu với ngưỡng đã ghi trước ở `evidence/hypothesis.md`:** chưa đạt. Ngưỡng yêu cầu ≥2/3 học viên mất ≥30 phút; ghi chép hiện có P1=15, P2=30, P3=20 phút, nên chỉ một người ở mốc 30 phút (và người đó thuộc L3B). Chưa có bằng chứng trực tiếp rằng học viên sau khi nhận lời giải vẫn không giải thích được lỗi của mình; P1–P3 đều nói cuối cùng hiểu nguyên nhân. P4 kể một trường hợp ban đầu chưa giải thích được sau khi dùng lời giải AI, nhưng sau khi coach cùng chạy từng bước thì học viên giải thích lại được.

## 3. Trích dẫn nguyên văn (đã bỏ tên)

1. “Em thử input nhỏ thì thấy tổng bị thiếu đúng lượt cuối.” — P1, học viên L3A.
2. “In biến ra từng vòng là em tìm được chỗ lệch.” — P1, học viên L3A.
3. “Em cứ nhìn vào công thức mà không để ý danh sách đã bị lọc bớt phần tử.” — P2, học viên L3B.
4. “Bạn em chỉ bảo kiểm tra mẫu số, rồi em tự thấy chỗ sai.” — P2, học viên L3B.
5. “Lúc thấy giá trị đúng ngay ở ngưỡng thì em hiểu vì sao dấu so sánh bị lệch.” — P3, học viên L3A.
6. “Có bạn chép được cách sửa nhưng chưa nói được vì sao; đổi input là lộ ra ngay.” — P4, lab coach.

## 4. Các nguồn có khớp nhau không

Phỏng vấn và coach đều kể các trường hợp lỗi logic; người học dùng input nhỏ, `print`, hỏi bạn hoặc ChatGPT để khoanh vùng và cuối cùng tự giải thích được nguyên nhân. Điều này ủng hộ hướng gợi ý từng bước hơn là đưa lời giải, nhưng chưa chứng minh nhu cầu mạnh hoặc mức tiết kiệm thời gian. Data pre-class không khớp trực tiếp với bài Python nên chỉ được xem là ngữ cảnh, không phải xác nhận độc lập.

## 5. Kết luận

Giả thuyết ban đầu: **đúng một phần**. Có tình huống code chạy nhưng kết quả sai ở học viên L3A, và các em tự báo tốn thời gian tìm lỗi logic. Tuy nhiên, ngưỡng ≥30 phút ở ≥2/3 học viên không đạt; hai người L3A báo 15 và 20 phút, đều tự tìm được cách kiểm chứng. Chưa có bằng chứng rằng người học vẫn không hiểu sau khi nhận trợ giúp. Giữ lát cắt gợi ý Socratic như giả thuyết sản phẩm cần kiểm thêm; không tuyên bố đây là pain phổ biến hoặc đã được chứng minh.

Điều còn chưa biết: thời gian trung vị trên mẫu lớn hơn; tỉ lệ học viên L3A gặp tình huống này; các em có muốn dùng một công cụ riêng thay cho `print`/bạn/ChatGPT không; ảnh hưởng đến việc hoàn thành bài.

## Lịch hẹn CP2

| Vai | Giờ hẹn | Đã xong? |
|---|---|---|
| Học viên L3A (P1) | 18:00 27/11 | ✅ |
| Học viên L3B (P2) | 18:15 27/11 | ✅ |
| Học viên L3A (P3) | 18:30 27/11 | ✅ |
| Lab coach (P4) | 18:45 27/11 | ✅ |
