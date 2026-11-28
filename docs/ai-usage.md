# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Code bản chạy thử (rà soát CP2) | Codex | Rà hợp đồng một câu hỏi và sửa validator để loại output không có đúng một dấu `?`. | Đã kiểm nhanh với một câu có/không có dấu hỏi; chưa kiểm output model thật. | Lê Đoàn Dương |
| Prompt / thiết kế lời gọi mô hình | | | | |
| Đào data (viết script đếm, gợi ý nhãn) | Codex | Viết `evidence/count_preclass.py`, chạy phép đếm trên bảng BTC và soạn phần mô tả tổng hợp; không chép file gốc vào repo. | Script chạy lại cho cùng số; Dương/nhóm cần rà cách lọc và giới hạn suy luận trước khi nộp. | Lê Đoàn Dương |
| Rà câu hỏi phỏng vấn / khảo sát | Claude Code | Soạn mẫu câu hỏi phỏng vấn (`evidence/interviews/TEMPLATE.md`) và khảo sát (`evidence/survey/questions.md`), rà câu dẫn dắt; viết `create_form.gs` tạo Google Form. | Văn tự đi phỏng vấn P1–P4 và thu 20 câu trả lời khảo sát; AI không tạo người được hỏi, câu trả lời hay trích dẫn. | Kiều Đình Văn |
| Tổng hợp bằng chứng (đếm khảo sát, summary, canvas) | Claude Code | Viết `evidence/survey/count_survey.py`; gộp số và trích dẫn vào `evidence/summary.md`, canvas dòng 4, `spec.md` §0 (chèn ảnh chụp, che ảnh đại diện); soạn nháp `reflection/kieu-dinh-van.md` và kịch bản `validation/kich-ban-nguoi-dung-thu.md`. | Văn cần: chạy lại `python evidence/survey/count_survey.py` xem ra cùng số; đọc lại từng số trên canvas và slide trang 1–2 so với `summary.md`; tự viết lại reflection. | Kiều Đình Văn |
| Viết câu thử (benchmark) | Antigravity / Gemini | Hỗ trợ chuẩn hoá 24 câu thử theo nhãn `[DE] [CODE] [TEST] [MUC]` (14 câu biên/tấn công `tu_viet`, 10 câu `nguoi_dung` tái hiện trung thực từ biên bản `P1`–`P4` và khảo sát `S06, S12, S14, S16`), soạn 5 metric ở `eval/metric_spec.yaml` và rà lỗi `eval/run-1.csv`, `eval/run-3.csv`. | Tuấn rà lại từng câu thử, kiểm bằng `python run.py check` (0 cảnh báo) và đối chiếu từng điểm `pass` theo `eval/metric_spec.yaml` trước khi chạy `python run.py score`. | Bùi Lê Công Tuấn |
| Sinh data `synthetic` (nếu có) | Claude Code (theo data card) | Hỗ trợ soạn 5 bài Mini Lab mẫu và 10 mô tả lỗi; không dùng làm bằng chứng pain. | Theo `data/DATA_CARD.md`: Hiếu kiểm 5/5 bài, 15/15 test mẫu và 10/10 mô tả lỗi. | Nguyễn Cảnh Hiếu |
| Chấm cột `pass` bằng LLM (nếu có) | | | Kiểm tra thủ công __ câu thử, khớp __/__ | |
| Slide, spec và persona | Codex, Antigravity / Gemini | Codex: soạn nháp các mục CP3 spec từ P1–P4, tìm nguồn giá model và giả định persona. Antigravity: dựng bản HTML 8 trang (`slides/demo-slides.html`), xuất `demo-slides.pdf` và đồng bộ số liệu từ `evidence/summary.md`, `eval/report.md`, `cost/cost-estimate.md`. | Dương rà lại trích dẫn, phép tính, giả định persona; Tuấn kiểm lại toàn bộ 8 trang slide, kết luận ITERATE và đối chiếu khớp số liệu với repo. | Lê Đoàn Dương, Bùi Lê Công Tuấn |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
