# Chi phí khi dùng thật

> Điền ở guide bước 4.2, nộp ở CP4 14:30 Thứ Bảy 28/11. Ôn lại: ngày 13, ngày 1, ngày 14 · lab ngày 13, lab ngày 14. Chấm ở rubric R6.
> Số **không điền tay**: điền `cost/personas.yaml` → `python run.py simulate` → chép bảng trong `cost/simulate-N-summary.md` vào đây.
> Lúc build dùng gói miễn phí vẫn tính theo **giá gói trả phí** — đây là chi phí cho lúc đưa vào dùng thật.

## 1. Đầu vào

- **Persona** (`cost/personas.yaml`): 3 kiểu với share 0.33/0.33/0.34; tần suất lấy từ P1–P3, số lượt/phiên là giả định được ghi rõ trong file.
- **Quy mô người dùng**: thấp 500 · cơ sở 721 · cao 1.000. 721 là số mã học viên giả danh trong data BTC, chỉ là proxy toàn khoá, không phải sĩ số L3A; thấp/cao là kịch bản tự ước tính.
- **Giá** (USD/1M token, nguồn và ngày xem trong `cost/personas.yaml`): Gemini 3.1 Flash-Lite $0.25 vào / $1.50 ra; Gemini 3.8 Flash $0.75 vào / $3.75 ra.
- **Tỉ lệ đạt** dùng để tính: 13/24 (54%) — lượt `run-1@20261128-092750` (Gemini 3.1 Flash-Lite). Lượt 2 có lỗi API và chưa chấm, không dùng để tính.
- Đo token trên `gemini-3.1-flash-lite`; dòng Gemini 3.8 Flash là tính theo giá tham chiếu, không phải model đã đo.

## 2. Kết quả mô phỏng

Lượt mô phỏng: `cost/simulate-1.csv` · run ID `simulate-1@20261128-114845` · 50 phiên · seed 42. Có 4 phiên lỗi API trên 50; bảng chi phí/phiên loại 4 phiên lỗi và tính từ 46 phiên không lỗi (`cost/simulate-1-summary.md`).

*(dán bảng từ `cost/simulate-N-summary.md`)*

| Model | Chi phí / phiên | Chi phí / task thành công | / tháng — thấp | / tháng — cơ sở | / tháng — cao | / người / tháng (cơ sở) |
|---|---|---|---|---|---|---|
| gemini-3.1-flash-lite (giá đã đo) | $0.00046 | $0.00086 | $0.7253 | $1.05 | $1.45 | $0.0015 |
| gemini-3.8-flash (giá tham chiếu) | $0.0013 | $0.0024 | $2.03 | $2.92 | $4.05 | $0.0041 |

Chi phí / task thành công = chi phí trung bình mỗi phiên ÷ tỉ lệ đạt — **không coi như đạt 100%**.

## 3. So với impact

- Impact tiềm năng / người / tháng (`spec.md` §2): khoảng 90 phút (3 lần × 30 phút), suy từ mẫu nhỏ và tự báo; chưa đo thời gian tiết kiệm thực tế.
- Chi phí model / người / tháng (cơ sở, Gemini 3.1 Flash-Lite): khoảng $0.0015 theo proxy 721 người.
- **Kết luận:** token model có chi phí rất thấp so với impact thời gian giả định, nhưng chưa chứng minh sản phẩm tiết kiệm được thời gian; chưa gồm hosting, giám sát hay hỗ trợ người dùng.

**Giới hạn đo:** 4/50 phiên có lỗi (một timeout, ba HTTP 503 do model bận). Bộ tóm tắt loại các phiên có lỗi khỏi trung bình; nếu phiên lỗi đã có một lượt gọi thành công trước khi lỗi, token của lượt đó không được tính vào bảng chi phí. Số tháng dựa trên quy mô toàn khoá proxy, share persona và giả định tần suất trong `cost/personas.yaml`; không phải dự báo riêng cho L3A.

## 4. *(Muốn sâu hơn, không bắt buộc)*

- Bảng độ nhạy: model rẻ hơn · cache · cắt ngữ cảnh · giới hạn bước — mỗi cần gạt đổi chi phí bao nhiêu
- Chi phí ngoài model: hosting, lưu trữ, giờ công người duyệt
- Quy mô nào thì bài toán còn đáng làm
