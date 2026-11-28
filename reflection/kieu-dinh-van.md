# Reflection — Kiều Đình Văn


1. **Vai trò + phần mình làm (trỏ tới file / commit):**
   Mình là TV2, phụ trách nghiên cứu người dùng. Mình phỏng vấn 3 học viên ngoài nhóm và 1 lab coach (`evidence/interviews/P1.md`–`P4.md`, commit `e8ee0a0`), làm khảo sát 20 học viên qua Discord và nhóm Zalo lớp (`evidence/survey/`, commit `ebaaa84`), rồi tổng hợp thành `evidence/summary.md`. Mình cùng Dương viết `spec.md` §0–§2, chụp ảnh luồng làm bài hiện tại (`evidence/screenshots/`, commit `0048fa3`) và cập nhật canvas dòng 4 (commit `f56c4ad`). Ở CP4 mình soạn nội dung slide trang 1–2 và chuẩn bị buổi người dùng thử.

2. **AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):**
   Mình dùng Claude Code để: soạn mẫu câu hỏi phỏng vấn và khảo sát, viết script `count_survey.py` đếm số từ `results.csv`, viết `create_form.gs` tạo Google Form, gộp số vào `summary.md` và canvas, xử lý xung đột git khi kéo code của nhóm. Người phỏng vấn, câu trả lời và trích dẫn là mình tự thu, AI không tạo ra.

3. **Một câu thử trượt của nhóm và mình học được gì từ nó:**
   Câu `B19` (bài năm nhuận) được tái hiện từ câu trả lời khảo sát S12 của một học viên L3A: "Đề có nhiều điều kiện nên mình bỏ sót một trường hợp đặc biệt." Ở lượt 1, trợ lý được yêu cầu Cấp 1 (chỉ cho học viên quan sát kết quả sai) nhưng lại chỉ thẳng vào điều kiện trong hàm bỏ sót trường hợp chia hết cho 400 — tức là nhảy cấp, gần như nói luôn chỗ sai (`eval/run-1.csv`, `eval/report.md`). Mình học được: chính tình huống người dùng thật kể lại là chỗ AI dễ "giúp quá tay" nhất, vì lỗi rõ ràng nên model muốn nói luôn. Bằng chứng từ người dùng không chỉ để chứng minh pain mà còn là câu thử tốt nhất để bắt lỗi của sản phẩm.
