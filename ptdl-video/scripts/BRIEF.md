# Brief: lời giảng lồng tiếng AI cho học phần "Phân tích dữ liệu Marketing" (BM6110)

Bối cảnh: Khoa Kinh doanh số, Trường Kinh tế – Đại học Công nghiệp Hà Nội (HaUI). Video bài giảng cho chương trình đào tạo Marketing từ xa.
Mỗi slide sẽ có một file audio riêng, đọc bằng giọng AI (mô hình F5-TTS tiếng Việt, nhân bản giọng nữ phát thanh).
Slide tự chuyển khi đọc xong, nên lời của mỗi slide phải tự đứng được.

## Đầu vào
- `bN_slides.txt`: chữ trên từng slide (+ `[GHI CHÚ GV]` nếu có, là gợi ý giảng của giảng viên — tận dụng).
- `b10_slides.txt` + mẫu lời giảng thật của bài 10 (dưới đây) để bắt văn phong.

## Văn phong (bám theo bài 9–10 do giảng viên thật đã ghi)
- Ngôi giảng viên nói với sinh viên: "các bạn", "chúng ta", "mình cùng nhau…". Không xưng tên giảng viên.
- Tự nhiên, rõ ràng, như đang giảng, không đọc lại nguyên văn slide. Giải thích ý, nêu ví dụ, nối mạch giữa các slide ("vậy thì…", "tiếp theo…", "các bạn để ý…").
- Mở đầu slide 1: "Xin chào các bạn và chào mừng các bạn đã đến với bài số [N] của học phần Phân tích dữ liệu marketing. Trong bài học hôm nay, chúng ta sẽ cùng nhau tìm hiểu …"
- Kết thúc ở slide cuối: tóm ý ngắn + "Cảm ơn các bạn đã theo dõi, và hẹn gặp lại các bạn trong video tiếp theo."
- Không nhắc subscribe/kênh YouTube. Không dùng từ đệm thừa kiểu "nhá", "à", "ừm".
- Bảng số liệu/bài tập: không đọc từng ô, chỉ nói bảng thể hiện gì, cách đọc, 1–2 ví dụ.
- Slide đánh dấu (HIDDEN): bỏ qua, ghi "text": "".

Mẫu lời thật bài 10: "Xin chào các bạn và chào mừng mọi người đã đến với bài học lý thuyết cuối cùng, bài số 10 trong học phần phân tích dữ liệu marketing. Bài học ngày hôm nay chúng ta sẽ tiếp tục cùng nhau qua phần đánh giá hiệu quả và xây dựng marketing KPI phần 2." … "Vậy thì ở trên màn hình thì chúng ta đang có Dashboard phân tích giá trị vòng đời khách hàng, hay còn gọi là Customer Lifetime Value, CLV. Vậy thì nhìn ở trên màn hình này thì các bạn có thể thấy là chúng ta đang có…"

## Độ dài
Tổng bài khoảng 22–28 phút ≈ 4.500–5.800 âm tiết tiếng Việt (đếm bằng `wc -w`). Phân bổ theo độ nặng slide: slide tiêu đề/agenda 40–90 âm tiết; slide khái niệm/bảng/case 150–450 âm tiết. Không slide nào quá 600 âm tiết.

## Chuẩn hoá cho máy đọc (BẮT BUỘC — sai là máy đọc sai)
- Viết số bằng chữ: "2018" → "năm hai nghìn không trăm mười tám"; "32%" → "ba mươi hai phần trăm"; "3.000" → "ba nghìn"; "5×5×5 = 125" → "năm nhân năm nhân năm bằng một trăm hai mươi lăm"; "3.2.1" → "ba chấm hai chấm một"; "Bài 4" → "bài bốn".
- Ký hiệu: "ε" → "ép-xi-lon", "≥" → "lớn hơn hoặc bằng", "→" bỏ hoặc nói "dẫn tới", "/" → "trên" hoặc "hoặc" theo nghĩa, "&" → "và", "%" như trên.
- Viết tắt tiếng Anh: đánh vần theo cách người Việt đọc, tách bằng gạch nối: RFM → "a-rờ ép em", CLV → "xê eo vê", KPI → "kây pi ai", MDS → "em đê ét", SEM → "ét e em", PLS → "pi eo ét", MMM → "em em em", BCG → "bê xê giê", ROI → "a-rờ âu ai", CTR → "xê tê a-rờ", AI → "ây ai". Lần đầu xuất hiện có thể nói thêm nghĩa tiếng Việt.
- Thuật ngữ tiếng Anh thông dụng giữ nguyên nhưng chỉ khi phổ biến (marketing, dashboard, K-means → "cây min", cluster → nói "cụm"). Ưu tiên nói tiếng Việt.
- Câu ngắn–vừa (≤ 35 âm tiết/câu), có dấu phẩy chỗ cần ngắt hơi. Không dùng ngoặc, gạch đầu dòng, emoji, markdown, dấu ngoặc kép trong "text".

## Đầu ra
Ghi file `bN_script.json` (UTF-8), mảng JSON, đúng số slide, theo thứ tự:
`[{"slide": 1, "text": "…"}, {"slide": 2, "text": "…"}, …]`
Kiểm tra: số phần tử = số slide; tổng `wc -w` trong khoảng trên; không còn chữ số Ả-rập (0–9) hay ký hiệu % ε ≥ → trong text (chạy kiểm tra bằng python trước khi xong).
Báo cáo lại: tổng âm tiết, ước lượng phút (÷ 210 âm tiết/phút), các slide bỏ qua, chỗ nội dung slide có vẻ sai/thiếu (nếu thấy).
