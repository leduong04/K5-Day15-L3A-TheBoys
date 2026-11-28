# Dàn slide → lấy số từ file nào

> Làm ở guide bước 5.1. Luật: **không có bằng chứng thì không có slide** — mỗi trang ≥1 con số / trích dẫn có nguồn / kết quả đo.
> Xuất PDF thành `demo-slides.pdf` ở thư mục gốc repo, nộp tại CP4 14:30 Thứ Bảy 28/11. Nộp PDF, không nộp link.

| # | Trang | Nội dung & số liệu chính | Số lấy từ | Xong |
|---|---|---|---|---|
| 1 | Người dùng & pain | Học viên L3A làm Python Mini Lab: code chạy được nhưng ra sai kết quả. **14/19** (L3A **7/10**) nói tốn công nhất ở tìm lỗi logic; **6/10** L3A mất trên 30 phút (P1 30', P3 20'); **0/8** người dùng AI/lời giải tự giải thích được đầy đủ. Trích dẫn S13: *"Đọc lời giải xong vẫn không biết cách tự tìm lỗi ở bài tương tự."* | `evidence/summary.md` | ☑ |
| 2 | Vì sao chọn bài này | Impact hướng A (Socratic lỗi logic): **~13 người × 3 lần × 30 phút = 1.170 phút (~19,5 giờ/tháng)** *(tự ước tính từ P1, P3, P4 và khảo sát)*. Đã loại: B (hiểu đề: 4/19), C (lỗi cú pháp/môi trường: 1/19, dưới 5'), D (công cụ cho coach: khác người dùng chính). | `spec.md` §2 | ☑ |
| 3 | Giải pháp | Lát cắt: `[DE][CODE][TEST][MUC]` → **đúng 1 câu hỏi Socratic theo 4 cấp** (Quan sát → Định hướng → Khái niệm → Ví dụ bài khác). Workflow cố định (`parse_input` → `lookup_lab` → `call_model` → `check_no_solution`, tối đa 2 lần gọi model). AI chỉ gợi ý, học viên tự sửa code. | `spec.md` §4 | ☑ |
| 4 | Demo live | • **Trường hợp `thuong` (`B14` — P2):** `trung_binh_dat` chia sai mẫu số `len(ds)` → demo `[MUC] 1` rồi bấm tăng cấp lên `[MUC] 2` + `[DA_THU]`.<br>• **Trường hợp `kho`/`tu_choi` (`B12` prompt injection trong `[CODE]` hoặc `B18` thiếu `[DE]` & `[TEST]`):** chống chèn lệnh / hỏi gom đủ nhãn thiếu.<br>• Mạng hỏng → phát video dự phòng (link ở `README.md`). | `eval/benchmark.csv` | ☐ |
| 5 | **Đánh giá thế nào** | 24 câu (`thuong 12 · kho 8 · tu_choi 4`; **10/24 = 41,7%** `nguoi_dung` từ P1–P4 & khảo sát) · 5 metric chốt trước CP2 · chuẩn đạt: ≥85%, 100% không lộ lời giải, 100% `tu_choi`.<br>• **Lượt 1** (`run-1@20261128-092750`): **13/24 (54%)** — lệch cấp (6 câu), không từ chối cú pháp/môi trường (`B10, B24`), lộ toán tử (`B23`), hỏi thiếu nhãn (`B18`).<br>• **Lượt 2** (`run-2@20261128-100327`): lỗi HTTP 429 free tier (5 câu, giữ nguyên log).<br>• **Lượt 3 sau cải tiến** (`run-3@20261128-121459`): **22/24 (92%)** — `thuong 12/12 (100%)`, `tu_choi 4/4 (100%)`, `kho 6/8 (75%)` (**đạt chuẩn**, 1 câu `B23` `TimeoutError`). | `eval/README.md`, `eval/report.md` | ☑ |
| 6 | **Chi phí khi dùng thật** | `simulate-1@20261128-114845` (50 phiên, seed 42, 46 phiên không lỗi, chuẩn hoá theo tỉ lệ đạt lượt 1 `54%`):<br>• **`gemini-3.1-flash-lite` (đo thật):** **$0.00046**/phiên · **$0.00086**/task thành công · **$0.7253 / $1.05 / $1.45**/tháng (500 / 721 / 1.000 user proxy) ≈ **$0.0015**/người/tháng.<br>• **`gemini-3.8-flash` (tham chiếu):** **$0.0024**/task thành công · **$2.03 / $2.92 / $4.05**/tháng.<br>• Rất nhỏ so với impact giả định ~90 phút/người/tháng (chưa gồm hosting/vận hành). | `cost/cost-estimate.md`, `cost/simulate-1-summary.md` | ☑ |
| 7 | Kết luận | **Go (tiếp tục thử nghiệm lớp thật L3A):** giải quyết đúng pain tìm lỗi logic (14/19, ~19,5 giờ/tháng), đã đạt chuẩn đánh giá **92% (22/24)** với 0% lộ lời giải sau cải tiến, chi phí mỗi phiên rất nhỏ so với thời gian tiết kiệm. | Trang 1, 5, 6 | ☑ |
| 8 | Nếu có thêm 1 tuần | (1) Xử lý triệt để câu hỏi test ẩn (`B08`) & thêm retry/timeout 25s trong `codebase/ai.py` để tránh treo 60s như `B23`; (2) Làm mềm câu hỏi Cấp 2 ở `B02, B22`; (3) Mở rộng `data/labs.json` lên 15–20 bài thật & đo thực tế với ≥5 học viên L3A (`validation/log.md`). | `eval/report.md` mục 4 · `validation/log.md` | ☑ |

**Trước khi lên:** tải repo về một máy khác (hoặc thư mục mới), chạy theo mục "Chạy trong 3 phút" của `README.md` · `.env` có trên máy demo, đã gọi thử 1 câu trong vòng 1 giờ trước giờ demo · video dự phòng mở được bằng cửa sổ ẩn danh · biết bản chạy thử sẽ làm gì với **1 câu thử lạ** của giám khảo.

Ai nói trang nào (mỗi người ≥1 phần — dự kiến, chốt lại trước 14:00):

| Trang | Người nói |
|---|---|
| 1–2 (Pain & Impact) | Kiều Đình Văn |
| 3 (Thiết kế giải pháp) | Nguyễn Cảnh Hiếu |
| 4–5 (Demo live & Đánh giá Lượt 1 → Lượt 3) | Bùi Lê Công Tuấn |
| 6–8 (Chi phí, Kết luận & Hướng tiếp theo) | Lê Đoàn Dương |
