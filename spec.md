# AI SPEC — Socratic Debugger · Nhóm The Boys · Phòng [XXX] · Zone [X]

> Mốc nộp: §7 chốt chuẩn "đạt" tại **CP2 19:30 Thứ Sáu 27/11** · §0–§7 nộp **CP3 10:00 Thứ Bảy 28/11** · đủ §0–§10 **CP4 14:30 Thứ Bảy 28/11** · §10 changelog ghi tiếp đến **23:59 Thứ Bảy 28/11**.
> Đầu mỗi mục ghi bước guide (`02-guide.md` trong repo đề) chỉ cách điền. Mỗi mục ngắn, có số và nguồn; chi tiết để ở file được trỏ tới. Xoá dòng hướng dẫn trong ngoặc vuông khi điền xong.

Track: [x] A · [ ] B · [ ] C · [ ] D · [ ] E — bài toán: trợ lý gợi ý theo phương pháp Socratic giúp học viên tự tìm lỗi logic trong Python Mini Lab
Data BTC cấp đã dùng (nếu có — không commit nguyên file): __

## §0. Hiện tại việc này diễn ra thế nào *(guide 1.1)*
- Luồng hiện tại của việc này, trong khoá hoặc trên app thật (3–5 bước; ảnh chụp từ tài khoản của mình, đã che thông tin):
- Công cụ / AI đang được dùng cho việc này (nếu có) + nguồn. Không kiểm được thì ghi "chưa kiểm":

## §1. Người dùng & bằng chứng *(guide 1.1, 1.2)*
- Người dùng chính (một vai cụ thể):
- Việc họ cố làm xong (`động từ + đối tượng + bối cảnh`, không có chữ AI):
- Hôm nay họ giải bằng gì, hỏng ở đâu, vì sao chưa bỏ:
- Pain (KHÔNG chữ AI): ai — đang làm gì — vướng đâu — hậu quả gì:
- Bằng chứng — số chính + kết luận (chi tiết: `evidence/summary.md`): __

## §2. Impact & quyết định chọn *(guide 1.3)*

| Hướng | Bao nhiêu người gặp | Bao nhiêu lần / tháng | Mỗi lần tốn gì | Impact / tháng | Làm kịp không | Chọn? |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |

- **Impact / tháng** của hướng chọn = __ người × __ lần × __ phút = __ — nguồn từng thừa số: __ (không có nguồn thì ghi rõ *(tự ước tính)*)
- Hướng ĐÃ LOẠI + vì sao (giữ lại, đừng xoá):
- Số lần / tháng của từng kiểu người dùng (dùng cho persona ở §8):

## §3. Giải pháp tương tự *(guide 2.1)*
- [sản phẩm / tính năng gần giống]: một điều đáng học · một điều đáng né · mình khác gì

## §4. Thiết kế *(guide 2.2, 3.2)*

> Các quyết định dưới đây nhóm chốt chiều 27/11, trước CP2. Bảng công cụ sẽ được đối chiếu lại với `codebase/tools.py` khi code xong (người phụ trách: Hiếu).

- **Lát cắt MỘT CÂU:** một học viên L3A gửi đề bài Python Mini Lab, code và kết quả test sai; trợ lý chọn chỗ có khả năng sai logic và trả về **đúng một câu hỏi gợi mở ở cấp gợi ý được yêu cầu**, không chứa code sửa, để học viên tự tìm ra nguyên nhân.
- **Không làm:**
  1. Không sửa code hộ, không đưa lời giải hoặc dòng code đúng.
  2. Không hỗ trợ lỗi cú pháp, lỗi cài đặt môi trường, ngôn ngữ khác Python.
  3. Không làm bài ngoài Python Mini Lab, không chấm điểm bài.
  4. Không hội thoại nhiều lượt ở phần lõi: mỗi lượt một câu hỏi, giao diện lo việc tăng cấp.
- **Định dạng đầu vào** (một chuỗi văn bản, có nhãn):

  | Nhãn | Bắt buộc | Nếu thiếu |
  |---|---|---|
  | `[DE]` đề bài | Có | Hỏi lại đề bài, không gọi model |
  | `[CODE]` code đang ra sai | Có | Hỏi lại code |
  | `[TEST]` input, kết quả, mong đợi | Có | Hỏi lại: chạy với input nào, ra gì, mong đợi gì |
  | `[MUC]` cấp gợi ý 1–4 | Không | Mặc định cấp 1 |
  | `[DA_THU]` học viên đã thử gì | Không | Có thì không hỏi lại điều học viên đã thử |

  Không có nhãn nào (người dùng gõ tự do) thì trợ lý cố tự tách 3 phần; không tách được thì hỏi lại.
- **Bốn cấp gợi ý** (mỗi lượt trả đúng một câu hỏi ở một cấp; ví dụ cho lỗi `range(1, n)` bỏ sót `n`, `tong_chan(10)` ra 20 thay vì 30):

  | Cấp | Câu hỏi nhắm vào | Ví dụ | Luật |
  |---|---|---|---|
  | 1 · Quan sát | So kết quả với mong đợi | "Kết quả thiếu đúng 10 so với mong đợi. Số 10 liên quan gì tới input?" | Chưa chỉ vùng code |
  | 2 · Định hướng | Một vùng / dòng / biến cần kiểm | "Vòng lặp duyệt `i` từ đâu đến đâu?" | Không nói dòng đó sai thế nào |
  | 3 · Gợi ý khái niệm | Kiến thức Python liên quan | "`range(a, b)` có bao gồm `b` không?" | Không nói cách sửa |
  | 4 · Ví dụ tương tự | Một bài **khác** có cùng loại lỗi | "Muốn in các số từ 1 đến 5 bằng `range`, bạn viết thế nào?" | Bài khác, tên biến khác, không có dòng code nào dán thẳng vào bài gốc được |

  Học viên đã qua cấp 4 mà vẫn chưa ra: trợ lý gợi ý hỏi lab coach, vẫn không đưa lời giải.
- **Sơ đồ:**

  ```mermaid
  flowchart LR
    A[Học viên gửi bài] --> B{Đủ DE, CODE, TEST?}
    B -- thiếu --> H[Hỏi lại phần thiếu]
    H -- học viên bổ sung --> A
    B -- đủ --> C[Chọn chỗ nghi sai]
    C --> D[Tạo 1 câu hỏi theo cấp MUC]
    D --> E{Lộ lời giải?}
    E -- có: viết lại, tối đa 1 lần --> D
    E -- không --> F[Học viên tự kiểm, tự sửa]
    F -- chưa ra: cấp + 1 --> D
  ```

- **Hình dạng:** [x] workflow cố định · [ ] một agent · [ ] nhiều agent — các bước luôn giống nhau (tách đầu vào → tìm căn cứ → model đặt câu hỏi → kiểm lộ lời giải), không cần AI tự chọn bước tiếp. Không chọn agent vì đắt hơn, khó kiểm hơn và có thể tự gọi công cụ sai; tối đa 2 lần gọi model mỗi lượt để chi phí có trần.
- **AI dựa vào đâu** — công cụ dự kiến (đối chiếu lại với `codebase/tools.py` khi code xong):

  | Công cụ | Input | Output | Tác động ra ngoài? |
  |---|---|---|---|
  | `parse_input` | chuỗi người dùng gửi | đề, code, test, cấp, đã thử, danh sách phần thiếu | Không |
  | `lookup_lab` | đề bài | bài khớp trong `data/` (đề, test mẫu, lỗi hay gặp, có mã), rỗng nếu không thấy | Không |
  | `check_no_solution` | câu hỏi của model, code học viên | có/không lộ lời giải hoặc sai định dạng + lý do | Không |

- **Mức tự động:** [x] AI gợi ý, người quyết · [ ] AI tự làm khi chắc, chuyển người khi không · [ ] AI tự làm — học viên tự kiểm và tự sửa code. AI chỉ nhầm chỗ thì học viên mất thêm thời gian (sửa rẻ); AI lộ lời giải thì mất mục đích học (đắt), nên chặn bằng code.
- **Chỗ chặn rủi ro:** rủi ro lớn nhất là lộ lời giải. Chặn ở 2 lớp: (1) luật trong system prompt; (2) bước kiểm bằng code `check_no_solution` sau model — có khối code, có đoạn code không nằm trong code học viên, hoặc có cụm "sửa thành / đổi thành / đáp án là" thì gọi lại 1 lần, vẫn lộ thì trả câu hỏi dự phòng theo cấp.
- **Chỗ người duyệt:** việc sửa code luôn do học viên làm. AI không ghi, không chạy, không nộp code của học viên.
- **Nguyên tắc thiết kế:**

  | Nguyên tắc | Chỗ cụ thể trên sơ đồ / trong bản chạy thử |
  |---|---|
  | G10 — thu hẹp phạm vi khi không chắc | Thiếu `[DE]/[CODE]/[TEST]` → hỏi lại, không gọi model; không chắc chỗ sai → hỏi câu kiểm chứng chung (chạy tay với input nhỏ, in giá trị trung gian), không khẳng định dòng nào sai |
  | Không đưa lời giải | Nút "Lộ lời giải?" trên sơ đồ = `check_no_solution` |
  | Gợi ý tăng dần, một bước mỗi lượt | Tham số `[MUC]`; giao diện tăng cấp khi học viên "vẫn chưa ra" |
  | Code học viên là dữ liệu, không phải chỉ thị | Prompt bọc code trong thẻ riêng; chỉ thị nằm trong comment code bị bỏ qua |

- **Phần còn giả** (tính đến 27/11): `codebase/` vẫn là code ví dụ của khung, model ở chế độ giả. Dữ liệu `data/` sẽ do nhóm tự viết (nhãn `synthetic`).

## §5. Chỗ khó — 4 lớp + ≥6 kịch bản + 2 tấn công *(guide 2.3)*

| Kịch bản | Lớp (1–4) | Hành vi mong muốn (nói gì, hiện gì, cho làm gì tiếp) | Câu thử |
|---|---|---|---|
|  |  |  |  |
| *(tấn công)* |  |  |  |
| *(tấn công)* |  |  |  |

(1) nguồn sự thật · (2) mơ hồ / thiếu thông tin · (3) ngoài phạm vi / thẩm quyền · (4) đặc thù lĩnh vực (sai thì người dùng mất gì đắt nhất)

## §6. Bốn đường đi của trải nghiệm
- Mọi thứ suôn sẻ: · Không chắc (lớp 2): · Không có căn cứ (lớp 1): · Người dùng sửa:
- Bị đòi ngoài phạm vi (lớp 3): · Trường hợp đặc thù lĩnh vực (lớp 4):

## §7. Đánh giá & chuẩn "đạt" *(guide 2.4, 4.1)*
- Data card: `data/DATA_CARD.md` · bộ câu thử: `eval/benchmark.csv` — __ câu (thuong __ · kho __ · tu_choi __) · metric: `eval/metric_spec.yaml` (__ metric)
- **Chuẩn "đạt"** (chốt **trước 19:30 Thứ Sáu 27/11**, giữ nguyên đến 23:59 Thứ Bảy 28/11): "Đạt khi ≥ __% câu qua, và __"
- Kết quả: lượt 1 __/__ (__%) · lượt 2 __/__ (__%) — run ID: __ / __ → chi tiết `eval/report.md`, hồ sơ `eval/README.md`

## §8. Chi phí khi dùng thật *(guide 4.2)*
- Persona + giá: `cost/personas.yaml` · lượt mô phỏng: `cost/simulate-__.csv` (__ phiên)
- Chi phí / task thành công: __ (model __) · __ (model __)
- Chi phí / tháng ở quy mô thật: thấp __ · cơ sở __ · cao __ → chi tiết `cost/cost-estimate.md`
- So với impact / người / tháng (§2): đáng làm không, vì sao:

## §9. Rủi ro & an toàn
- Dữ liệu: đã ẩn danh gì, không thu gì, không đưa gì vào model gói miễn phí:
- AI **không được** làm gì kể cả khi người dùng yêu cầu:
- Ai có thể bị hại nếu AI sai, và nhóm chặn thế nào:

## §10. Phân công & changelog
- Phân công có tên (theo chặng, chia cặp — guide "Cách chia việc"):

  **Chặng CP2 (hạn 19:30 T6 27/11)** — metric và chuẩn "đạt" khoá sau mốc này

  | Việc | Người làm | Cặp kiểm | File | Hạn |
  |---|---|---|---|---|
  | ≥3 metric kiểm chứng được (không lộ lời giải, đúng vùng lỗi, đúng một câu hỏi, đúng cấp, hỏi lại khi thiếu, từ chối đúng) | Tuấn | Hiếu | `eval/metric_spec.yaml` | 18:30 nháp · 19:00 chốt |
  | Chuẩn "đạt" | Tuấn | Dương | `spec.md` §7 | 19:00 |
  | ≥10 câu thử theo định dạng `[DE] [CODE] [TEST] [MUC]`; xoá B01–B03 mẫu; ≥5 `kho`, ≥2 `tu_choi` (2 tấn công), có câu cho cả 4 cấp, ≥1/3 nguồn `nguoi_dung`/`data_that` | Tuấn | Văn (cấp câu thật) | `eval/benchmark.csv` | 19:00 |
  | Hồ sơ đánh giá mục 1–4; người thứ hai chấm thử 5 output (khớp ≥4/5) | Tuấn | Dương chấm | `eval/README.md` | 19:15 |
  | §4 thiết kế (đã có bản này), khung `tools.py` + `agent.py` chạy hết luồng ở chế độ giả | Hiếu | Dương | `spec.md` §4, `codebase/` | 19:00 |
  | Dữ liệu nền 3–5 bài Mini Lab tự viết + data card | Hiếu | Dương | `data/`, `data/DATA_CARD.md` | 19:00 |
  | Hẹn ≥3 học viên ngoài nhóm + 1 lab coach (chỉ ghi vai, giờ); phỏng vấn người đầu tiên | Văn | — | `evidence/summary.md`, `evidence/interviews/P1.md` | 19:00 |
  | Canvas dòng 4: số đầu tiên + 1 trích dẫn | Văn | Dương | `canvas.md` | 19:15 |
  | Viết cách đếm **trước** khi chạy; đếm sơ bộ data pre-class; mục data pre-class trong data card | Dương | Văn | `evidence/data-mining.md`, `data/DATA_CARD.md` | 19:00 |
  | `python run.py check`, kiểm `git status` không có `.env`/`data-btc/`, push, nộp CP2 | Dương | — | — | 19:15 |

  **Chặng tối T6 → CP3 (hạn 10:00 T7 28/11)**

  | Việc | Người làm | Cặp kiểm | File |
  |---|---|---|---|
  | Nối model thật, prompt 4 cấp, `check_no_solution`; `eval --try` thấy token > 0 | Hiếu | Tuấn | `codebase/ai.py`, `agent.py`, `tools.py` |
  | Giao diện nhận code nhiều dòng, nút "vẫn chưa ra → cấp tiếp theo" | Hiếu | Văn (thử như người dùng) | `codebase/app.py` |
  | Phỏng vấn đủ ≥3 người, mỗi người một file; xin code lỗi thật (ẩn danh) chuyển cho Tuấn | Văn | — | `evidence/interviews/` |
  | Tổng hợp bằng chứng, ≥5 trích dẫn, kết luận giả thuyết | Văn | Dương | `evidence/summary.md` |
  | Kết quả đào data (x/N, ≥5 ví dụ, giới hạn) | Dương | Văn | `evidence/data-mining.md` |
  | Bộ câu thử 20–30 câu | Tuấn | Văn | `eval/benchmark.csv` |
  | `spec.md` §0–§3, §5–§6 | Dương tổng hợp (§0–§2 cùng Văn; §5–§6 cùng Hiếu) | — | `spec.md` |
  | Đóng băng benchmark → chạy lượt 1 | Hiếu chạy | Tuấn | `eval/run-1.csv`, `traces/run-1.jsonl` |
  | Chấm `pass`, `score`, báo cáo mục 1–2 | Tuấn | Dương | `eval/run-1.csv`, `eval/report.md` |
  | Persona có nguồn, `simulate --try` | Dương | Hiếu (báo token, số lần gọi) | `cost/personas.yaml` |

  **Chặng CP3 → CP4 (hạn 14:30 T7 28/11)**

  | Việc | Người làm | Cặp kiểm | File |
  |---|---|---|---|
  | Một cải tiến cho nhóm lỗi đau nhất; ghi changelog | Hiếu + Tuấn | — | `codebase/`, `spec.md` §10 |
  | Lượt 2, báo cáo mục 3–4, hồ sơ mục 5–6 | Tuấn | Hiếu | `eval/run-2.csv`, `eval/report.md`, `eval/README.md` |
  | Mô phỏng ≥50 phiên, chi phí, `spec.md` §8 | Dương | Tuấn | `cost/` |
  | `spec.md` đủ §0–§10 | Dương | cả nhóm | `spec.md` |
  | Slide PDF + video dự phòng + link trong README | Tuấn | Văn | `demo-slides.pdf`, `README.md` |
  | *(Bonus)* 2–3 người dùng thử | Văn | Hiếu | `validation/log.md` |
  | Chạy lại repo ở thư mục mới theo "Chạy trong 3 phút" | Dương | — | — |

  **Đến 23:59 T7:** mỗi người một file `reflection/<ten>.md` và dòng của mình trong `docs/ai-usage.md`.
- Dùng AI vào việc gì (2–3 dòng; chi tiết `docs/ai-usage.md`):
- Nhật ký thay đổi — **mọi thay đổi sau CP2 19:30 Thứ Sáu 27/11 phải có dòng ở đây**:

**CP2 → CP4** (vd thu hẹp lát cắt, hỏi thêm người dùng, lần cải tiến trước lượt 2)

| Thời điểm | Đổi gì | Vì sao (trỏ về câu thử / lỗi / bằng chứng nào) |
|---|---|---|
|  |  |  |

**Sau CP4 (đến 23:59 Thứ Bảy 28/11)** (sửa theo góp ý — không sửa chuẩn "đạt", câu thử, số bằng chứng, kết quả các lượt đã chạy)

| Thời điểm | Đổi gì | Vì sao |
|---|---|---|
|  |  |  |
