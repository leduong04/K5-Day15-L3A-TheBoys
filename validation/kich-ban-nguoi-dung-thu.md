# Kịch bản người dùng thử — dùng khi điền `validation/log.md`

> Người hỏi: Văn · Người ghi: Văn. Mỗi người ~10 phút. 2–3 học viên **ngoài nhóm**, ưu tiên L3A.
> Chỉ ghi điều thật sự thấy / nghe. Không ghi tên — ghi vai (vd "Học viên L3A, T1").

## Chuẩn bị (trước khi gặp người thử)

- [ ] Máy có file `.env` chứa key Gemini; chạy thử `python run.py` thấy cửa sổ app mở và trả lời được 1 câu.
- [ ] Mở sẵn bài lỗi ở dưới (copy được ngay).
- [ ] Mở `validation/log.md` để ghi, hoặc giấy bút.

## Bài lỗi đưa cho người thử

Bài này nhóm tự viết riêng cho buổi thử, **không** nằm trong `eval/benchmark.csv`.

```
[DE]
Viết hàm dem_so_duong(ds) trả về số phần tử lớn hơn 0 trong danh sách ds.
[CODE]
def dem_so_duong(ds):
    dem = 0
    for x in ds:
        if x >= 0:
            dem += 1
    return dem
[TEST]
dem_so_duong([3, 0, -2, 5]) ra 3, mong đợi 2
```

(Lỗi: `>=` đếm cả số 0. **Không nói lỗi cho người thử.**)

## 5 nhịp (~10 phút)

| Nhịp | Thời gian | Văn nói / làm |
|---|---|---|
| 1. Làm quen | 1 phút | "Mình đang thử một công cụ của nhóm, không phải thử bạn. Bạn làm sai cũng không sao, công cụ sai mới là cái mình cần tìm. Bạn vừa làm vừa nói to suy nghĩ giúp mình nhé." |
| 2. Bối cảnh | 1 phút | "Lần gần nhất code Python của bạn chạy được mà ra kết quả sai, bạn đã làm gì?" (nghe, ghi 1 câu) |
| 3. Giao việc | 30 giây | Đưa bài lỗi ở trên: **"Bạn hãy tìm ra vì sao kết quả sai và tự sửa cho đúng, dùng công cụ này."** — giao theo kết quả, **không** chỉ nút nào bấm. |
| 4. Quan sát | 5–6 phút | **Im lặng, không giúp.** Ghi: họ làm gì đầu tiên · chỗ dừng lại lâu / do dự · chỗ hiểu sai câu hỏi của app · có bấm "vẫn chưa ra" không, bấm mấy lần · cuối cùng có tự sửa được không, mất bao lâu. Nếu kẹt quá 2 phút: chỉ hỏi "Bạn đang nghĩ gì?" |
| 5. Hỏi sau | 2 phút | (a) "Câu hỏi nào của app giúp bạn nhất? Câu nào khó hiểu?" (b) "So với cách bạn hay làm (print, ChatGPT, hỏi bạn) thì thế nào?" (c) **"Nếu mai không được dùng nữa, bạn thấy: rất tiếc / hơi tiếc / không sao?"** |

Nếu người thử giải xong quá nhanh (dưới 1 phút) hoặc chỉ khen: đưa thêm bài khó hơn — ví dụ đổi test thành `dem_so_duong([0, 0, 0])` ra 3, mong đợi 0 và hỏi họ giải thích vì sao.

## Ghi gì vào `validation/log.md`

Mỗi người một dòng:
- **Người thử (vai):** Học viên L3A / L3B, T1–T3.
- **Việc giao:** "Tìm vì sao `dem_so_duong` sai và tự sửa".
- **Quan sát:** hành vi thấy được (làm gì đầu tiên, chỗ do dự, chỗ hiểu sai, có sửa được không, mất mấy phút).
- **Trích nguyên văn:** 1 câu họ nói, chép đúng từng chữ.
- **Mức nghiêm trọng:** cao (không làm tiếp được) / vừa (lúng túng nhưng vượt qua) / thấp (khó chịu nhỏ).

Ghi xong → đưa ghi chép cho Claude sắp xếp vào bảng và phần "Tổng hợp"; điều sửa trước demo thì ghi thêm ở `spec.md` §10.
