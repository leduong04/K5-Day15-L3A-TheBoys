# Ước tính simulate --try từ lượt eval thật

> Đây là phép chiếu theo token trung bình đo ở run eval, không phải lượt mô phỏng mới gọi API. Chạy `python run.py simulate --try` để đo thực tế từng phiên khi có API key.

- Run nguồn: `eval/run-1.csv` · Run ID: `run-1@20261128-092750` · model: `gemini-3.1-flash-lite` · 24 câu, không lỗi.
- Số đo nguồn: 15847 token vào · 1858 token ra · 21 lần gọi; trung bình 660.3 token vào / 77.4 token ra / 0.875 lần gọi mỗi câu (≈ 0.9).
- Kịch bản thử: 10 phiên theo `cost/personas.yaml`, seed 42; 16 lượt hỏi tổng cộng.
- Phân bổ persona: hoi_ban_vua 4 phiên / 8 lượt, tu_debug_it 4 phiên / 4 lượt, hoi_ai_nhieu 2 phiên / 4 lượt.
- Token dự phóng từ trung bình run nguồn: khoảng 10565 vào · 1239 ra · 14.0 lần gọi.

## Chi phí dự phóng cho 10 phiên

| Model dùng để tính giá | Giá vào / ra (USD / 1M token) | Chi phí ước tính |
|---|---:|---:|
| gemini-3.1-flash-lite (model đo token) | $0.25 / $1.5 | $0.004499 |
| gemini-3.8-flash (giá tham chiếu) | $0.75 / $3.75 | $0.012568 |

## Giới hạn

Run nguồn gồm đủ 24 câu benchmark, còn mô phỏng chọn ngẫu nhiên loại `thuong` và `kho`; dùng trung bình chung là ước tính gần đúng, không thay thế token đo riêng trên các đầu vào mô phỏng. Chi phí mỗi model dùng tokenization của model đo được và giá trong `cost/personas.yaml`.
