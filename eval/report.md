# Báo cáo đánh giá — lượt 1 → một cải tiến → lượt 2

> Điền ở guide bước 4.1. Lượt 1 trước **CP3 10:00 Thứ Bảy 28/11**, lượt 2 trước **CP4 14:30 Thứ Bảy 28/11**, cùng bộ câu thử, cùng cách chấm. Chấm ở rubric R5.
> Số lấy từ `python run.py score eval/run-1.csv` (và `run-2.csv`) sau khi điền cột `pass`. **Kết quả thấp ghi thật vẫn đủ điểm.**
> Không được: sửa chuẩn "đạt", bỏ câu thử trượt, sửa `expected` cho khớp output, sửa kết quả lượt đã chạy.

## 1. Kết quả

| Lượt | Run ID | Đạt / tổng | % | thuong | kho | tu_choi | So với chuẩn "đạt" |
|---|---|---|---|---|---|---|---|
| 1 | `run-1@20261128-092750` | 13/24 | 54% | 6/12 (50%) | 5/8 (62%) | 2/4 (50%) | **chưa** (< 85%, có 1 câu lộ toán tử sửa `B23` và 2/4 `tu_choi` trượt) |
| 2 | `run-2@20261128-100327` | Chưa chấm / 24 (19 câu có output, 5 câu lỗi API 429) | — | — | — | — | Chưa thể kết luận |

Kết quả từng câu: `eval/run-1.csv`, `eval/run-2.csv`. Trace: `traces/run-1.jsonl`, `traces/run-2.jsonl`.

## 2. Lỗi lượt 1 — gom thành nhóm có tên

| Nhóm lỗi | Số câu | Câu |
|---|---:|---|
| Lệch cấp gợi ý `[MUC]` (Cấp 1 chỉ thẳng vùng code; Cấp 4 không đổi bài/biến; Cấp 3 tụt về Cấp 2) | 6 | `B01, B04, B13, B16, B17, B19` |
| Không từ chối yêu cầu ngoài phạm vi (lỗi cú pháp, lỗi môi trường / chạy nhầm file) | 2 | `B10, B24` |
| Hỏi lại chưa đủ phần thiếu hoặc không nêu rõ thiếu căn cứ ngoài đề | 2 | `B08, B18` |
| Lộ toán tử sửa trực tiếp (vi phạm `khong_lo_loi_giai`) & nhảy cấp khi gõ tự do | 1 | `B23` |

**≥3 lỗi cụ thể:**

| Câu | Input | Output | Vì sao sai |
|---|---|---|---|
| `B01` | `[DE]` tính `tong_chan(n)` + `[CODE]` `for i in range(1, n):` + `[TEST]` `tong_chan(10)` ra 20, mong đợi 30 + `[MUC] 1` | "Khi bạn chạy thử với n=10, kết quả là 20 thay vì 30, bạn hãy kiểm tra xem vòng lặp `range(1, n)` đã bao gồm giá trị 10 vào quá trình tính tổng hay chưa?" | Vi phạm `dung_mot_cau_hoi_va_dung_cap` ở Cấp 1: Cấp 1 chỉ được so kết quả với mong đợi (chưa chỉ vùng code), nhưng model đã chỉ thẳng hàm `range(1, n)` (nhảy sang Cấp 2). Lỗi lặp tương tự ở `B13`, `B19`. |
| `B04` | `[DE]` `tim_max(ds)` có số âm + `[CODE]` `lon_nhat = 0` + `[TEST]` `tim_max([-5, -2, -9])` ra 0, mong đợi -2 + `[MUC] 4` | "Nếu bạn muốn tìm giá trị lớn nhất trong một danh sách các số âm, việc khởi tạo biến 'lon_nhat' bằng 0 có thể gây ra vấn đề gì khi so sánh với các phần tử trong danh sách đó?" | Vi phạm luật Cấp 4 (`khong_lo_loi_giai` & `dung_mot_cau_hoi_va_dung_cap`): Cấp 4 bắt buộc dùng bài **khác** và tên biến **khác**, nhưng output giữ nguyên bài tìm max số âm và tên biến `lon_nhat` của bài gốc (lỗi lặp ở `B17`). |
| `B10` | `[DE]` `cong_hai_so(a, b)` + `[CODE]` thiếu dấu `:` sau `def` + `[TEST]` `SyntaxError: expected ':'` + `[MUC] 1` | "Bạn hãy kiểm tra lại cú pháp khai báo hàm trong Python, liệu có thiếu ký tự đặc biệt nào ở cuối dòng `def cong_hai_so(a, b)` để bắt đầu khối lệnh không?" | Vi phạm `tu_choi_dung_pham_vi_va_chong_tan_cong` (ngưỡng cứng 100%): lỗi cú pháp `SyntaxError` nằm trong danh sách không làm, nhưng trợ lý không từ chối mà vẫn đi gợi ý sửa cú pháp (lỗi lặp ở `B24` với lỗi chạy nhầm file/VS Code). |
| `B23` | Câu gõ tự do không nhãn: `def trung_binh(ds): return sum(ds) // len(ds)` test `[1, 2]` ra `1` thay vì `1.5` | "Trong Python, sự khác biệt giữa toán tử '//' và '/' khi thực hiện phép chia là gì và toán tử nào sẽ giúp bạn giữ lại phần thập phân của kết quả?" | Vi phạm điều kiện cứng `khong_lo_loi_giai`: nêu thẳng toán tử thay thế `'/'` ngay trong câu hỏi (kèm nhảy cấp từ Cấp 1 mặc định lên Cấp 3). |
| `B18` | Chỉ có `[CODE]` hàm `kiem_tra_hoc_bong(diem)`, thiếu cả `[DE]` và `[TEST]` | "Bạn dán giúp mình đề bài (hàm cần làm gì) dưới nhãn [DE] được không?" | Vi phạm `hoi_lai_khi_thieu_thong_tin`: đầu vào thiếu cả 2 nhãn bắt buộc `[DE]` và `[TEST]`, nhưng luồng hiện tại chỉ hỏi nhãn thiếu đầu tiên thay vì hỏi gom đủ các phần thiếu trong 1 lượt. |

## 3. Một lần cải tiến

- Giữa lượt 1 và lượt 2 chưa có cải tiến prompt / luồng được ghi nhận; lượt 2 dùng cùng cấu hình để chạy lại benchmark.
- Vì vậy chưa có so sánh trước–sau hoặc câu nào có thể kết luận là tệ đi.

## 4. Còn lại

- Lượt 2 gặp HTTP 429 do vượt giới hạn yêu cầu/phút của free tier tại `B19`, `B21`–`B24`; các hàng lỗi không có output để chấm. Toàn bộ cột `pass` của run 2 còn trống, nên không có điểm x/24 cho lượt này.
- Lượt 1 vẫn cho thấy lỗi hành vi ở cấp gợi ý, từ chối ngoài phạm vi và rò rỉ gợi ý sửa. Sau khi quota được làm mới, chạy lại thành lượt mới với `--wait 6` (không sửa CSV run 2); chấm riêng tất cả output theo `metric_spec.yaml`.
