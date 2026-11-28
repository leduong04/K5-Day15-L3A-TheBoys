# Tóm tắt mô phỏng simulate-1@20261128-114845

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| tu_debug_it | 16 | 1 | 683 | 81 | 0.9 | 2.7 |
| hoi_ban_vua | 13 | 2 | 1077 | 127 | 1.5 | 4.9 |
| hoi_ai_nhieu | 17 | 2 | 1494 | 172 | 1.9 | 5.7 |

Tỉ lệ đạt dùng để tính: 13/24 (54%) — lượt run-1@20261128-092750

- Tự chọn: lượt run-N mới nhất đã chấm xong, chạy bằng đúng model đang đo (run-1.csv). Muốn dùng lượt khác (vd lượt 2): thêm `--rate-from eval/run-2.csv`. Lượt mới hơn nhưng chưa chấm xong hoặc khác model, nên KHÔNG dùng: run-2.

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (500 người) | Chi phí / tháng — cơ sở (721 người) | Chi phí / tháng — cao (1.000 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gemini-3.1-flash-lite (vào 0.25 · ra 1.5 $/1M) | $0.00046 | $0.00086 | $0.00052 | $0.7253 | $1.05 | $1.45 | $0.0015 |
| gemini-3.8-flash (vào 0.75 · ra 3.75 $/1M) | $0.0013 | $0.0024 | $0.0015 | $2.03 | $2.92 | $4.05 | $0.0041 |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (1.7) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: gemini-3.1-flash-lite. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 4/50.
