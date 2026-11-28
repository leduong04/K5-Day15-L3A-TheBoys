// Tạo Google Form khảo sát từ evidence/survey/questions.md
// Cách chạy: script.google.com → Dự án mới → dán toàn bộ file này → Lưu → chọn hàm createForm → Chạy.
// Link form in ra ở "Nhật ký thực thi". Form nằm trong Google Drive của bạn.

function createForm() {
  var form = FormApp.create('Khi code Python chạy được mà ra kết quả sai — bạn xử lý thế nào?');
  form.setDescription(
    'Nhóm The Boys (AI20K) đang tìm hiểu cách học viên xử lý khi code Python Mini Lab chạy không báo lỗi ' +
    'nhưng ra kết quả sai. Form mất khoảng 2 phút, không giới thiệu sản phẩm, không thu tên hay email. Cảm ơn bạn!'
  );
  form.setCollectEmail(false);

  // 1
  form.addMultipleChoiceItem()
    .setTitle('Bạn là:')
    .setChoiceValues(['Học viên L3A', 'Học viên L3B', 'Lab coach / TA'])
    .showOtherOption(true)
    .setRequired(true);

  // 2
  form.addMultipleChoiceItem()
    .setTitle('Lần gần nhất bạn gặp code Python (Mini Lab hoặc bài tập) chạy được, không báo lỗi, nhưng ra kết quả sai là khi nào?')
    .setChoiceValues(['Hôm nay', 'Tuần này', 'Tuần trước', 'Lâu hơn', 'Chưa bao giờ'])
    .setRequired(true);

  // 3
  form.addTextItem()
    .setTitle('Trong 1 tuần qua, bạn gặp chuyện đó mấy lần? (nhập số)')
    .setValidation(FormApp.createTextValidation()
      .requireNumberGreaterThanOrEqualTo(0)
      .setHelpText('Nhập một số, ví dụ 0, 1, 2…')
      .build())
    .setRequired(true);

  // 4
  form.addCheckboxItem()
    .setTitle('Lần gần nhất đó, bạn đã làm gì? (chọn tất cả việc đã làm)')
    .setChoiceValues([
      'Tự đọc lại code',
      'In giá trị trung gian (print)',
      'Chạy tay với input nhỏ',
      'Hỏi bạn',
      'Hỏi lab coach / TA',
      'Dán code vào ChatGPT / AI khác',
      'Xem lời giải có sẵn',
      'Bỏ qua'
    ])
    .showOtherOption(true)
    .setRequired(true);

  // 5
  form.addMultipleChoiceItem()
    .setTitle('Từ lúc thấy sai đến lúc sửa xong (hoặc bỏ) mất khoảng bao lâu?')
    .setChoiceValues(['Dưới 5 phút', '5–15 phút', '15–30 phút', 'Trên 30 phút'])
    .setRequired(true);

  // 6
  form.addMultipleChoiceItem()
    .setTitle('Lần đó có sửa xong không?')
    .setChoiceValues(['Xong', 'Xong một phần', 'Bỏ'])
    .setRequired(true);

  // 7
  form.addMultipleChoiceItem()
    .setTitle('Lần đó, chỗ nào làm bạn mất thời gian nhất?')
    .setChoiceValues(['Hiểu đề / yêu cầu', 'Lỗi cú pháp, cài đặt, chạy file', 'Tìm chỗ sai trong logic'])
    .showOtherOption(true)
    .setRequired(true);

  // 8
  form.addMultipleChoiceItem()
    .setTitle('Nếu lần đó bạn có lời giải (từ ChatGPT, bạn bè, đáp án), sau đó bạn có tự giải thích được vì sao code cũ sai không?')
    .setChoiceValues(['Có, giải thích được', 'Chỉ hiểu một phần', 'Không', 'Không dùng lời giải'])
    .setRequired(true);

  // 9
  form.addParagraphTextItem()
    .setTitle('Điều gì khó chịu nhất ở lần đó?')
    .setRequired(false);

  // 10
  form.addTextItem()
    .setTitle('(Tuỳ chọn) Bạn có sẵn lòng cho nhóm hỏi thêm 10 phút không? Nếu có, để lại cách liên hệ.')
    .setRequired(false);

  Logger.log('Link gửi cho mọi người: ' + form.getPublishedUrl());
  Logger.log('Link sửa form (chỉ mình bạn): ' + form.getEditUrl());
}
