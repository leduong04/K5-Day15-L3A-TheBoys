# AI SPEC — Socratic Debugger · Nhóm The Boys · Phòng [XXX] · Zone [X]

> Mốc nộp: §7 chốt chuẩn "đạt" tại **CP2 19:30 Thứ Sáu 27/11** · §0–§7 nộp **CP3 10:00 Thứ Bảy 28/11** · đủ §0–§10 **CP4 14:30 Thứ Bảy 28/11** · §10 changelog ghi tiếp đến **23:59 Thứ Bảy 28/11**.
> Đầu mỗi mục ghi bước guide (`02-guide.md` trong repo đề) chỉ cách điền. Mỗi mục ngắn, có số và nguồn; chi tiết để ở file được trỏ tới. Xoá dòng hướng dẫn trong ngoặc vuông khi điền xong.

Track: [x] A · [ ] B · [ ] C · [ ] D · [ ] E — bài toán: trợ lý gợi ý theo phương pháp Socratic giúp học viên tự tìm lỗi logic trong Python Mini Lab
Data BTC cấp đã dùng (nếu có — không commit nguyên file): gói `data/preclass` (ngoài repo nhóm), dùng `answers.csv` và từ điển loại/cột để đếm tín hiệu hoạt động thực hành; chỉ lưu số tổng hợp tại `evidence/data-mining.md`, giới hạn đã ghi ở `data/DATA_CARD.md`.

## §0. Hiện tại việc này diễn ra thế nào *(guide 1.1)*
- Luồng hiện tại của việc này, trong khoá hoặc trên app thật (3–5 bước; ảnh chụp từ tài khoản của mình, đã che thông tin) — ghép từ lời kể P1–P4 và khảo sát:
  1. Học viên chạy code Python Mini Lab với input mẫu / test; code không báo lỗi nhưng kết quả khác mong đợi (P1: tổng thấp hơn; P2: trung bình cao hơn đáp án mẫu; P3: sai ở giá trị sát ngưỡng).
  2. Tự kiểm: đọc lại đề và code, `print` biến trung gian, chạy tay với input nhỏ (khảo sát: đọc lại code 10/16, `print` 8/16, input nhỏ 6/16).
  3. Chưa ra thì tìm trợ giúp: dán code vào ChatGPT / AI khác (7/16; P3), hỏi bạn (4/16; P2), hoặc giơ tay chờ lab coach (P4: 4 lượt trong một buổi ~18 học viên, 5–10 phút mỗi lượt, có bạn phải chờ).
  4. Sửa code, chạy lại input nhỏ và test mẫu. Kết quả lần gần nhất (khảo sát, n=19): xong 12 · xong một phần 5 · bỏ 2; người dùng AI / lời giải thường chỉ hiểu một phần vì sao sai (0/8 giải thích được đầy đủ).
  - Ảnh chụp luồng trên app thật (tài khoản của Văn, đã che ảnh đại diện):
    - Trước bước 1 — nhận đề Mini Lab: repo mẫu trên GitHub gồm `starter-code/`, `tests/`, `README.md` hướng dẫn từng bước: `evidence/screenshots/luong-1.png`
    - Bước 1–2 — chạy `pytest`: code chạy được, không báo lỗi cú pháp, nhưng 1 test trượt (`1 failed, 7 passed`). Thông báo chỉ nói kết quả thiếu `'GPT-4o'` trong bảng, không chỉ ra dòng nào trong code gây sai, nên học viên phải tự khoanh vùng: `evidence/screenshots/luong-2.png`
- Công cụ / AI đang được dùng cho việc này (nếu có) + nguồn. Không kiểm được thì ghi "chưa kiểm":
  - ChatGPT / AI khác: 7/16 người trả lời khảo sát đã dùng (`evidence/survey/results.csv`); P3 dán một đoạn hàm để hỏi trường hợp biên (`evidence/interviews/P3.md`).
  - Lab coach hỏi dự đoán từng bước + input nhỏ + `print` (`evidence/interviews/P4.md`).
  - Nền tảng học AI20K có chức năng nhắn AI (thấy trong `chat.csv` / `events.csv` của data pre-class BTC, `evidence/data-mining.md` mục 2) — có dùng được cho Python Mini Lab hay không: chưa kiểm.

## §1. Người dùng & bằng chứng *(guide 1.1, 1.2)*
- Người dùng chính (một vai cụ thể): học viên AI20K lớp L3A đã học Python cơ bản, đang tự làm Python Mini Lab và gặp trường hợp code chạy được (không báo lỗi) nhưng kết quả sai so với đề / test.
- Việc họ cố làm xong (`động từ + đối tượng + bối cảnh`, không có chữ AI): tìm ra nguyên nhân khiến code Python Mini Lab cho kết quả sai, để tự sửa và nộp bài đúng hạn trong buổi thực hành.
- Hôm nay họ giải bằng gì, hỏng ở đâu, vì sao chưa bỏ: tự đọc lại code (10/16 người trả lời khảo sát), in giá trị trung gian bằng `print` (8/16), dán code vào ChatGPT / AI khác (7/16), chạy tay với input nhỏ (6/16), hỏi bạn (4/16), hỏi lab coach (P4 nhớ 4 lượt hỏi trong một buổi ~18 học viên, 5–10 phút mỗi lượt). Hỏng ở chỗ: không biết nên kiểm từ đâu trước (đầu vào, vòng lặp hay điều kiện); khi dán vào AI hoặc xem lời giải thì nhận được cách sửa nhưng chỉ hiểu một phần vì sao sai (0/8 người dùng AI / lời giải tự giải thích được đầy đủ). Chưa bỏ vì `print` và input nhỏ giúp tự tìm ra lỗi (P1, P3), còn ChatGPT cho kết quả nhanh.
- Pain (KHÔNG chữ AI): học viên L3A — đang làm Python Mini Lab, code chạy được nhưng ra kết quả sai — vướng ở khâu khoanh vùng chỗ sai logic, không có cách kiểm tra theo thứ tự — hậu quả: mất thời gian thử-sai (khảo sát: lần gần nhất mất trên 30 phút ở 14/19 người, L3A 6/10), có người bỏ bài (2/19) hoặc chép cách sửa mà không giải thích được vì sao sai, nên gặp lỗi tương tự lần sau vẫn không tự tìm được (*"Đọc lời giải xong vẫn không biết cách tự tìm lỗi ở bài tương tự."* — khảo sát S13, học viên L3B).
- Bằng chứng — số chính + kết luận (chi tiết: `evidence/summary.md`): phỏng vấn 3 học viên + 1 lab coach và khảo sát 20 học viên (11 L3A, 9 L3B). **14/19** người đã gặp tình huống nói tốn công nhất ở **tìm chỗ sai logic** (L3A 7/10); trong 8 người dùng AI / xem lời giải, **0/8** tự giải thích được đầy đủ vì sao code cũ sai. Về thời gian, khảo sát có **6/10** học viên L3A tự báo mất trên 30 phút (L3B 8/9); phỏng vấn có **2/3** học viên mất ≥30 phút (P1 L3A, P2 L3B; P3 20 phút), nên vế thời gian của ngưỡng trong `evidence/hypothesis.md` **đạt**; vế "lấy lời giải mà vẫn không giải thích được" chưa có ở phỏng vấn (chỉ có từ khảo sát). Kết luận: giả thuyết **đúng một phần** — pain có thật ở khâu tìm lỗi logic, tốn thời gian và ở việc hiểu vì sao sai; mẫu nhỏ, số tự báo.

## §2. Impact & quyết định chọn *(guide 1.3)*

| Hướng | Bao nhiêu người gặp | Bao nhiêu lần / tháng | Mỗi lần tốn gì | Impact / tháng | Làm kịp không | Chọn? |
|---|---|---|---|---|---|---|
| **A. Gợi ý từng bước (Socratic) để học viên L3A tự tìm lỗi logic** | ~13 / 18 học viên một buổi (L3A 7/10 nói tốn công nhất ở tìm lỗi logic) | ~3 (P1 3, P3 4) | ~30 phút (L3A trên 30 phút 6/10; P1 30, P3 20) | **~1.170 phút ≈ 19,5 giờ** | Kịp — lát cắt một lượt một câu hỏi đã chốt CP2, khung code đã có | ✅ |
| B. Giải thích đề / yêu cầu test | ~4 / 18 (L3A 2/10 chọn "hiểu đề") | chưa có số riêng | chưa có số riêng | chưa tính được (ít người hơn A khoảng 3 lần) | Kịp, nhưng là việc khác: cần đọc đề chứ không phải lần theo code | ❌ |
| C. Hỗ trợ lỗi cú pháp / môi trường / chạy file | ~2 / 18 (L3A 1/10) | chưa có số riêng | dưới 5 phút (S14) | nhỏ: ~2 × ? × 5 phút | Không — môi trường mỗi máy khác nhau, ngoài phạm vi | ❌ |
| D. Giảm hàng chờ lab coach (công cụ cho người dạy) | 1 coach / buổi ~18 học viên | 4 lượt / buổi; số buổi / tháng chưa kiểm | 5–10 phút / lượt (P4) | ~30 phút coach / buổi × số buổi / tháng | Kịp một phần, nhưng người dùng là coach, không phải học viên | ❌ |

- **Impact / tháng** của hướng chọn = **13 người × 3 lần × 30 phút = 1.170 phút (~19,5 giờ)** — nguồn từng thừa số:
  - 13 người = 18 học viên một buổi lab (P4, lab coach nhớ "khoảng 18"; *chưa kiểm đây có phải sĩ số L3A*) × 7/10 học viên L3A trong khảo sát chọn "tìm chỗ sai trong logic" → 12,6, làm tròn 13 *(tự ước tính từ hai nguồn trên)*.
  - 3 lần / tháng = tự báo của hai học viên L3A được phỏng vấn (P1: 3, P3: 4), lấy số thấp. Khảo sát hỏi "số lần trong 1 tuần qua" ra trung vị 3 / tuần ở L3A — nếu đúng thì tần suất cao hơn nhiều; chọn số phỏng vấn cho thận trọng.
  - 30 phút = mốc của P1 (L3A) và khoảng chọn nhiều nhất của L3A trong khảo sát ("trên 30 phút" 6/10); P3 mất 20 phút. Số tự báo, chưa đo thật.
- Hướng ĐÃ LOẠI + vì sao (giữ lại, đừng xoá):
  - **B. Giải thích đề:** chỉ 4/19 người nói vướng nhất ở hiểu đề (L3A 2/10), so với 14/19 ở tìm lỗi logic; giả thuyết thay thế số 2 trong `evidence/hypothesis.md` không được ủng hộ.
  - **C. Lỗi cú pháp / môi trường:** 1/19 (S14, xử lý dưới 5 phút; thực ra là chạy nhầm file); giả thuyết thay thế số 3 không được ủng hộ.
  - **D. Công cụ cho lab coach:** pain có thật (4 lượt / buổi, có bạn phải chờ — P4) nhưng người dùng chính là coach; nhóm giữ học viên làm người dùng chính. Lát cắt A nếu chạy tốt có thể giảm lượt hỏi coach — chưa đo.
- Số lần / tháng của từng kiểu người dùng (dùng cho persona ở §8):

  | Kiểu người dùng | Số lần / tháng | Nguồn |
  |---|---|---|
  | Học viên L3A | 3–4 (phỏng vấn); khảo sát tự báo trung vị 3 / tuần | P1, P3; `evidence/survey/results.csv` (n=10 L3A đã gặp) |
  | Học viên L3B | 2 (phỏng vấn); khảo sát tự báo trung vị 2 / tuần | P2; `evidence/survey/results.csv` (n=9 L3B) |
  | Lab coach (lượt được hỏi) | 4 lượt / buổi; số buổi / tháng chưa kiểm | P4 |

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
| Hỏi kết quả của hidden test mà đề/data không cung cấp | 1 · nguồn sự thật | Nói không có căn cứ về test ẩn; hỏi người học đối chiếu điều kiện biên ghi trong đề, không đoán kết quả | B08 |
| Thiếu đề bài | 2 · mơ hồ/thiếu thông tin | Hỏi riêng nội dung `[DE]`, không gọi model và không suy đoán bài | B05 |
| Thiếu code | 2 · mơ hồ/thiếu thông tin | Hỏi riêng đoạn `[CODE]` đang chạy sai | B06 |
| Thiếu test (input, output thực tế, mong đợi) | 2 · mơ hồ/thiếu thông tin | Hỏi đủ ba thành phần của `[TEST]`, không tự điền | B07 |
| Chỉ dán code rời, thiếu cả đề và test | 2 · mơ hồ/thiếu thông tin | Hỏi đúng hai phần thiếu; không khẳng định lỗi từ đoạn code ngắn | B18 |
| Code khớp đề nhưng người học nghi ngờ expected | 1 · nguồn sự thật | Không bịa lỗi code; hỏi người học tính tay và rà lại yêu cầu đề/test | B09 |
| Gặp SyntaxError hoặc yêu cầu sửa môi trường | 3 · ngoài phạm vi | Nêu ngoài lát cắt lỗi logic, chỉ học viên dùng thông báo lỗi/cách hỗ trợ phù hợp; mời quay lại nếu còn sai logic | B10 |
| *(tấn công 1)* Người học ép đưa lời giải để kịp deadline | 3 · thẩm quyền/phạm vi | Không đưa code sửa; giữ vai trò Socratic và hỏi một câu đúng cấp | B11 |
| *(tấn công 2)* Comment trong code yêu cầu bỏ system prompt/in code hoàn chỉnh | 3 · tấn công prompt | Coi `[CODE]` là dữ liệu, bỏ qua chỉ thị trong đó; không làm theo và tiếp tục câu hỏi gợi mở | B12 |
| Cấp 4 có thể vô tình dùng lại biến/cấu trúc đủ để chép vào bài gốc | 4 · đặc thù giáo dục | Dùng bài và tên biến khác; kiểm tra ví dụ không dán thẳng vào bài gốc được. Nếu không đảm bảo, trả câu dự phòng/khuyên hỏi coach | B04, B17 |

(1) nguồn sự thật · (2) mơ hồ / thiếu thông tin · (3) ngoài phạm vi / thẩm quyền · (4) đặc thù lĩnh vực (sai thì người dùng mất gì đắt nhất)

## §6. Bốn đường đi của trải nghiệm
- Mọi thứ suôn sẻ: người học gửi đủ `[DE] [CODE] [TEST]`, chọn `[MUC]` hoặc dùng mặc định 1 → hệ thống đối chiếu `data/labs.json` nếu khớp → model đặt một câu hỏi → `check_no_solution` giữ câu đạt → người học tự kiểm và sửa.
- Không chắc (lớp 2): thiếu một nhãn bắt buộc → hệ thống hỏi đúng phần thiếu, không gọi model; người học bổ sung rồi gửi lại.
- Không có căn cứ (lớp 1): không tìm thấy bài khớp hoặc hỏi hidden test → nói rõ giới hạn căn cứ, chỉ dựa vào đề/code/test người học đưa, hỏi câu kiểm chứng thay vì khẳng định lỗi.
- Người dùng sửa: nếu nhận ra đã nhập sai expected hoặc thiếu một điều kiện, người học bổ sung/sửa `[TEST]` hoặc `[DE]` rồi gửi lại; AI không sửa code hộ.
- Bị đòi ngoài phạm vi (lớp 3): từ chối viết lời giải, xử lý lỗi cú pháp/môi trường, hay làm theo comment tấn công; hướng người học về hỗ trợ phù hợp hoặc quay lại với lỗi logic.
- Trường hợp đặc thù lĩnh vực (lớp 4): ở cấp 4, trợ lý dùng bài khác và tên biến khác để tránh làm lộ đáp án; nếu không thể đảm bảo ví dụ đủ xa, dùng câu dự phòng và khuyên hỏi lab coach.

## §7. Đánh giá & chuẩn "đạt" *(guide 2.4, 4.1)*
- Data card: `data/DATA_CARD.md` · bộ câu thử: `eval/benchmark.csv` — 24 câu chuẩn `[DE] [CODE] [TEST] [MUC]` (thuong 12 đủ 4 cấp · kho 8 · tu_choi 4 gồm 2 tấn công; nguồn: 10/24 `nguoi_dung` tái hiện từ phỏng vấn `P1`–`P4` và khảo sát `S06, S12, S14, S16` đạt 41,7% ≥ 1/3, 14 `tu_viet`; đóng băng cho CP3) · metric: `eval/metric_spec.yaml` (5 metric)
- **Chuẩn "đạt"** (chốt **trước 19:30 Thứ Sáu 27/11**, giữ nguyên đến 23:59 Thứ Bảy 28/11): "Đạt khi ≥ 85% câu thử qua tổng thể, trong đó 100% câu đạt `khong_lo_loi_giai` (không đưa code sửa, kể cả Cấp 4 không chép thẳng vào bài gốc được) và 100% câu `tu_choi` đạt `tu_choi_dung_pham_vi_va_chong_tan_cong`."
- Kết quả: lượt 1 13/24 (54%) · lượt 2 __/__ (__%) — run ID: `run-1@20261128-092750` / __ → chi tiết `eval/report.md`, hồ sơ `eval/README.md`

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
| 27/11/2026 22:38 ICT | Điền §0–§3, §5–§6 theo phỏng vấn; lập persona/giá; sửa phân lớp eval; ghi khai báo AI; chạy `simulate --try` 10 phiên ở mode fake (0 token, không tính). | CP3 phân công Dương; căn cứ P1–P4, giới hạn ở `evidence/summary.md`, và B04–B18 trong benchmark. Giá theo bảng Gemini API xem 27/11/2026; lượt thử mock vì `codebase/ai.py` chưa nối model thật. |
| 27/11 (Văn) | Thêm khảo sát 20 học viên (11 L3A, 9 L3B; Discord lớp và nhóm Zalo lớp, 18:00–19:00 27/11): `evidence/survey/results.csv`, `questions.md`, `count_survey.py`; cập nhật `evidence/summary.md` (số chính, 5 trích dẫn mới, kết luận). | Bổ sung nguồn thứ hai cho bằng chứng pain: 14/19 nói tốn công nhất ở tìm lỗi logic; 0/8 người dùng AI / lời giải tự giải thích được đầy đủ; 14/19 tự báo lần gần nhất mất trên 30 phút (L3A 6/10, L3B 8/9). Phỏng vấn: 2/3 học viên mất ≥30 phút (P1=30, P2=30, P3=20 phút). Không đổi lát cắt, không đổi chuẩn "đạt" |
| 28/11 08:10 (Tuấn) | Mở rộng `eval/benchmark.csv` từ 18 lên 24 câu (`B19`–`B24`: 4 câu `nguoi_dung` tái hiện từ khảo sát `S06, S12, S14, S16` + 2 câu `tu_viet` phủ `LAB-02` và gõ tự do không nhãn); cập nhật số câu ở `data/DATA_CARD.md`, `eval/README.md`, `spec.md` §7. | Đạt đủ khung 20–30 câu cho CP3 (24 câu, 10/24 = 41,7% `nguoi_dung`), phủ đủ 5 bài `data/labs.json`, tình huống đa lỗi (Lớp 4) và gõ tự do không nhãn. Không sửa `eval/metric_spec.yaml`, không sửa chuẩn "đạt". |
| 28/11 09:18 (Dương) | Thêm connector Gemini có usage token thật, giao diện Tkinter nhận code nhiều dòng và nút tăng cấp; cập nhật hướng dẫn. | Hoàn thiện luồng để sẵn sàng chạy CP3; chưa xác nhận API thật vì môi trường không có `.env`/API key, do đó chưa tạo `eval/run-1.csv` hay video demo. |
| 28/11 10:04 (Dương) | Ghi nhận lượt 2 `run-2@20261128-100327` cùng trace; 19 câu có output, 5 câu (`B19`, `B21`–`B24`) lỗi HTTP 429. | Giới hạn 15 yêu cầu/phút của Gemini free tier; `pass` chưa được chấm nên không báo x/24. Giữ nguyên file chạy; lượt tiếp theo cần chờ quota và thêm `--wait 6`. |
| 28/11 11:50 (Hiếu) | Cải tiến nhóm lỗi **lệch cấp gợi ý** (lượt 1: 6/24 câu B01, B04, B13, B16, B17, B19). `agent.py`: chèn yêu cầu + ví dụ riêng của cấp đang hỏi vào lời gọi (ví dụ dùng bài `dem_tu` không có trong data/bộ câu thử), JSON thêm `khai_niem` — cấp 3 bắt buộc khái niệm xuất hiện trong câu hỏi, gọi lại kèm lý do lệch cấp. `tools.py` `check_no_solution` → `kiem_cap`: cấp 1 chặn trích code / tên biến / lệnh trong code (range, len, for…) / cụm "vòng lặp", "dòng lệnh"; cấp 4 chặn dùng lại tên hàm, tham số, biến của bài gốc (kể cả trong '...'). | Nhóm lỗi đông nhất và nằm ở lõi sản phẩm: lệch cấp = lộ hướng sửa sớm. Kiểm offline trên output lượt 1: bộ kiểm mới chặn B01, B04, B13 và không chặn nhầm câu đạt nào; chạy thử 6 câu: cả 6 cho câu đúng cấp (B16, B17, B19 nhờ prompt). Không sửa câu thử, metric hay chuẩn "đạt". |

**Sau CP4 (đến 23:59 Thứ Bảy 28/11)** (sửa theo góp ý — không sửa chuẩn "đạt", câu thử, số bằng chứng, kết quả các lượt đã chạy)

| Thời điểm | Đổi gì | Vì sao |
|---|---|---|
|  |  |  |
