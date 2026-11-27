# Đào data — cách đếm và kết quả

> Bản sơ bộ CP2. Script tổng hợp: `evidence/count_preclass.py`. Dữ liệu gốc ở thư mục BTC cấp bên ngoài repo, không commit.

## 1. Cách đếm

- **Nguồn:** `data/preclass/answers.csv` của BTC; thời gian trong `created_at` từ 2026-11-05 đến 2026-11-25 (UTC). Đọc `column_dictionary.csv` và `event_types.csv` để hiểu nghĩa trường và loại hoạt động.
- **Chỉ báo mô tả:** số dòng thực hành (`nguon = thuc_hanh`) có nhãn chấm `was_correct` là `True` hoặc `False`, chia cho tổng số dòng thực hành có nhãn chấm hợp lệ. Đơn vị là lượt trả lời, không phải học viên.
- **Chỉ báo thử lại:** gom theo mã học viên đã giả danh hoá + `lesson_id` + `ref`; đếm cặp học viên–bài có ít nhất 2 dòng trả lời trên tổng số cặp có dòng thực hành. Báo riêng số cặp thử lại có ít nhất một dòng sai.
- **Lọc:** không lọc theo ngày học, không suy ra lỗi logic từ nhãn sai; các bảng dữ liệu này không xác định trực tiếp bài Python Mini Lab.
- **Script:** `python evidence/count_preclass.py [đường_dẫn_đến_data/preclass]`. Mặc định là `../data/preclass`. Script chỉ in số tổng hợp và mẫu theo bài; không in mã học viên.

## 2. Đọc trước, đếm sau

Đã đọc từ điển cột và ý nghĩa loại sự kiện. Bản dữ liệu có bảng `answers.csv`, `events.csv`, `chat.csv` và các bảng hỗ trợ; dấu thời gian của dữ liệu trả lời trải từ 2026-11-05 đến 2026-11-25 UTC. Các loại hành vi có thể quan sát gồm trả lời câu hỏi thực hành, nhắn AI, và hoạt động xem bài/video. Những hành vi này chỉ là dấu hiệu hoạt động học, không cho biết nguyên nhân học viên gặp khó.

## 3. Kết quả sơ bộ

| Đếm gì | x / N | % | Ghi chú |
|---|---:|---:|---|
| Dòng trả lời thực hành bị chấm sai | 23 / 519 | 4.4% | Mẫu số là các dòng thực hành có nhãn đúng/sai hợp lệ; đơn vị là lượt trả lời. |
| Cặp học viên–bài có từ 2 lượt trả lời | 16 / 503 | 3.2% | Ghép bằng mã học viên giả danh hoá, bài và mã câu; không phải 16 học viên riêng biệt. |
| Cặp có từ 2 lượt, trong đó có ít nhất một lượt sai | 2 / 503 | 0.4% | Chỉ báo thận trọng về thử lại kèm một lượt sai; không chứng minh lỗi logic hay đau điểm. |

## 4. Ví dụ cụ thể đã ẩn danh

Các mẫu sau là nhóm theo bài và mã bước; không chứa mã học viên. Mỗi mẫu ghi số lượt trả lời trong một cặp học viên–bài và số lượt bị chấm sai.

1. `program-day01:ai-llm-foundation` · `lab:d01-lab-ban-la-llm:doan-roi-chay` — 2 lượt, 0 lượt sai.
2. `program-day01:ai-llm-foundation` · `lab:d01-lab-ban-la-llm:tu-sinh-cau` — mỗi cặp 2 lượt, 0 lượt sai.
3. `program-day01:ai-llm-foundation` · `lab:d01-lab-xep-ban-context:vong-1` — mỗi cặp 2 lượt, 0 lượt sai.
4. `program-day01:ai-llm-foundation` · `lab:d01-lab-xep-ban-context:vong-2` — mỗi cặp 2 lượt, 0 lượt sai.
5. `program-day03:chatbot-to-agentic-agent` · `lab:d03-lab-ban-la-agent:khi-cong-cu-loi` — 2 lượt, 0 lượt sai.

Các mẫu trên minh hoạ việc có một số lượt làm lại; không dùng chúng để nhận diện cá nhân hoặc khẳng định có pain.

## 5. Giới hạn của data

Data là hành vi trong chương trình AI20K, với các bài về AI/agent; không phải nhật ký Python Mini Lab nên không thể xác nhận giả thuyết về lỗi logic Python. Điểm đúng/sai không cho biết vì sao câu trả lời sai; một lượt lặp cũng có thể là thao tác bình thường. Kết quả sơ bộ này **chưa đủ bằng chứng** cho pain đã chọn và không được ngoại suy thành tỷ lệ lỗi Python.

→ Kiểm lại bằng phỏng vấn ít nhất 3 học viên L3A ngoài nhóm và một lab coach, hỏi về lần gần nhất gặp lỗi logic Python Mini Lab; xin ví dụ code/test đã ẩn danh nếu họ đồng ý. Bổ sung cách đếm riêng nếu BTC có dữ liệu trực tiếp về Python Mini Lab.
