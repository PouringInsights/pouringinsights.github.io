# Barista sính ngoại: loạt video watercolor

Tất cả video:
- Khổ dọc 1080×1920, 30fps, dưới 60 giây, âm lượng −14 LUFS.
- Dựng bằng OpenMontage (Remotion, chế độ atelier) trên engine màu nước chung trong `_watercolor-engine/engine.tsx`.
- Giọng đọc: Edge TTS `vi-VN-NamMinhNeural` +30%, đã xử lý hậu kỳ (chi tiết ở `V01-geisha/README.md`). Khi đăng, bật nhãn AI trên TikTok.

| Thứ tự gợi ý | Thư mục | Mã kế hoạch | Thời lượng | Hook (2 giây đầu) |
|---|---|---|---|---|
| 1 | `V01-geisha` | V02 | 58,4s | 20 ký cà phê. Sáu trăm nghìn đô. |
| 2 | `V01-v60` | V01 | 52,0s | V60 bắt đầu từ phòng thí nghiệm hóa học |
| 3 | `V05-melitta` | V05 | 44,6s | Giấy lọc bắt đầu từ vở bài tập của một cậu bé |
| 4 | `V13-crema` | V13 | 49,8s | Crema từng cần cả một tấm biển để giải thích |
| 5 | `V14-bach` | V14 | 45,5s | Bach viết vở hài về một cô gái nghiện cà phê |
| 6 | `V16-sweden` | V16 | 52,6s | Năm 1794, đám tang cho bình pha cà phê |

## Vòng tự phản biện: "người xem có dừng lại không?"

Mỗi kịch bản được chấm theo 6 câu hỏi. Bản nào trượt thì sửa trước khi tạo giọng đọc.

1. Hai giây đầu có một hình ảnh hoặc con số lạ, cụ thể không?
2. Có khoảng trống tò mò khiến người xem muốn biết tiếp không?
3. Có nút thắt hoặc bước ngoặt không?
4. Phần payoff có thông tin mới, không lặp lại hook không?
5. Có góc nhìn riêng của barista không?
6. CTA trả lời được bằng một chữ, và khung cuối có quay về hook không?

| Video | Kết quả lần 1 | Đã sửa |
|---|---|---|
| Melitta | Đạt cả 6 | Không cần sửa. CTA "team phin hay team giấy" gần gũi với người Việt |
| Bach | Trượt câu 1: mở bằng năm "Khoảng năm 1734", người xem lướt qua | Mở bằng "Bach, thiên tài nhạc cổ điển, từng viết một vở hài…" |
| Thụy Điển | Đạt. Hook "đám tang bình pha cà phê" rất mạnh | Giai thoại sinh đôi được nói rõ là giai thoại, kèm câu "nhiều nhà sử học cho rằng là bịa" |
| Crema | Trượt câu 1 và rủi ro dữ kiện: hook khẳng định một giai thoại rồi mới rào | Hook đổi sang dữ kiện đã kiểm chứng (tấm biển). Giai thoại "khách ngờ là váng bẩn" chuyển vào giữa bài, ghi "theo lời kể" |
| V60 | Đạt | Bỏ chữ "thất bại" của phễu 1980: nguồn Hario không nói vậy, để dành cho video V07 |

## Dữ kiện và nguồn

### V60
- Hario thành lập năm 1921, ban đầu làm dụng cụ khoa học.
- V60 khởi nguồn từ việc pha cà phê bằng phễu Erlenmeyer và giấy lọc gấp tư.
- Năm 1980 Hario ra phễu hình nón đầu tiên; V60 ra đời năm **2005**. Kế hoạch ghi một số nguồn nói 2004, nhưng trang của Hario ghi 2005.
- Tên gọi: chữ V và góc 60°. Bên trong có gân xoắn, đáy một lỗ lớn. Rót nhanh cho vị nhẹ, rót chậm cho vị đậm.
- Nguồn: [Hario: The origin of the V60](https://global.hario.com/sp_v60series.html)

### Melitta
- Bà Melitta Bentz ở Dresden đục lỗ đáy nồi đồng thau và lót giấy thấm lấy từ vở của con trai.
- Ngày 20/6/1908, bà đăng ký bảo hộ với cơ quan sáng chế Đức. Đây là dạng bảo hộ "Gebrauchsmuster" (mẫu hữu ích), nên video nói "đăng ký bảo hộ phát minh", không nói "bằng sáng chế".
- Công ty được đăng ký ngày 15/12/1908 với vốn 72 Reichspfennig.
- Nguồn: [DPMA](https://www.dpma.de/english/our_office/publications/ingeniouswomen/110jahrekaffeefilter/index.html), [Europeana](https://www.europeana.eu/en/blog/melitta-bentz-the-woman-who-invented-the-coffee-filter), [Wikipedia](https://en.wikipedia.org/wiki/Melitta_Bentz)

### Bach (BWV 211)
- Lời do Picander viết, in năm 1732; Bach phổ nhạc khoảng 1732–35. Vở nhiều khả năng ra mắt ở quán Zimmermann, Leipzig.
- Hai nhân vật chính: ông bố Schlendrian và cô con gái Lieschen.
- Chi tiết hôn ước có điều khoản cà phê là phần Bach thêm vào; video nói "bản của Bach thêm một cú lừa".
- Lời trong video là diễn giải ngắn bằng tiếng Việt, không trích nguyên văn. Lời gốc năm 1732 đã thuộc phạm vi công cộng. Video không dùng bản thu âm nào.
- Nguồn: [Wikipedia BWV 211](https://en.wikipedia.org/wiki/Schweigt_stille,_plaudert_nicht,_BWV_211), [Opera Scotland](https://operascotland.org/opera/402/Coffee+Cantata), [bach.org](https://bach.org/?p=1276)

### Thụy Điển
- Năm giai đoạn cấm: 1756–61, 1766–69, 1794–96, 1799–1802 và 1817–23.
- Ngày 1/8/1794, người ta tổ chức "đám tang cho bình pha cà phê".
- Cảnh sát Stockholm còn lưu hồ sơ của các giai đoạn cấm.
- Thí nghiệm sinh đôi của vua Gustav III chỉ là **giai thoại**, có nhà nghiên cứu ở Umeå cho là bịa.
- Một số tài liệu coi năm 1766 là chuyển sang đánh thuế nặng, không cấm hẳn; video dùng cách đếm năm lần theo Wikipedia.
- Nguồn: [Wikipedia: Coffee in Sweden](https://en.wikipedia.org/wiki/Coffee_in_Sweden), [The Local](https://www.thelocal.se/20180702/why-coffee-was-banned-in-sweden-five-times), [Popular Science](https://www.popsci.com/health/coffee-ban-history/), [Wikipedia: Gustav III's coffee experiment](https://en.wikipedia.org/wiki/Gustav_III_of_Sweden%27s_coffee_experiment)

### Crema
- Năm 1938, Gaggia nộp bằng sáng chế cho hệ thống "Lampo" không dùng hơi nước.
- Năm 1948 ra máy cần gạt piston, và Gaggia treo biển "caffè crema di caffè naturale".
- Chuyện khách ngờ crema là váng bẩn chỉ là **lời kể**.
- Còn tranh cãi bằng sáng chế cần gạt là năm 1938 hay 1947; video chỉ nói "hệ thống không dùng hơi nước" cho năm 1938.
- Nguồn: [Gaggia: Our history](https://www.gaggia.com/our-history/), [Gaggia NA](https://www.gaggia-na.com/pages/history), [Home-Barista](https://www.home-barista.com/levers/gaggia-achille-t534.html)

## Gói đăng

| Video | Caption | Hashtag |
|---|---|---|
| V60 | V60 bắt đầu từ một cái phễu phòng lab 🧪 Bạn rót nhanh hay rót chậm? | #V60 #pourover #caphephatay #baristasinhngoai #LearnOnTikTok |
| Melitta | Giấy lọc cà phê ra đời từ vở bài tập của một cậu bé năm 1908. Team phin hay team giấy? | #giayloc #pourover #lichsucaphe #baristasinhngoai #LearnOnTikTok |
| Crema | Lớp crema bạn chụp ảnh từng cần cả một tấm biển để giải thích ☕ | #crema #espresso #lichsucaphe #baristasinhngoai #LearnOnTikTok |
| Bach | Bach từng viết vở hài về một cô gái nghiện cà phê 🎻 Bố mẹ bạn từng cấm chưa? | #Bach #CoffeeCantata #lichsucaphe #baristasinhngoai #LearnOnTikTok |
| Thụy Điển | Thụy Điển từng cấm cà phê 5 lần. Cấm năm lần, thua cả năm. | #fika #ThuyDien #lichsucaphe #baristasinhngoai #LearnOnTikTok |

## Cần quay thêm trước khi đăng

Theo Marketing 7.0, phần trải nghiệm cần cảnh thật:
- **V60:** cận tay rót nhanh và rót chậm.
- **Melitta:** tráng giấy lọc.
- **Crema:** cận chiết espresso, sau đó khuấy crema.
- **Bach, Thụy Điển:** barista nói câu kết nhìn thẳng camera.
