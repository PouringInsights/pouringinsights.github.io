# V13: Crema, phiên bản craft-book (theo nhận diện kênh)

- **File:** `crema-craft.mp4` (bản mới). Bản watercolor cũ giữ lại là `crema-tam-bien.mp4`.
- **Thông số:** khổ dọc 1080×1920, 30fps, dưới 60 giây.

## Phong cách: vintage, craft book, vẽ tay

Lấy từ logo kênh:
- Nền giấy kem có sọc dọc mờ, giống poster "xin chào mọi người".
- Mảng màu be lốm đốm hạt đặt sau hình minh họa, giống mảng be sau tách cà phê trong logo.
- Nét mực nâu đen dày, hơi run như vẽ tay, từng nét tự hiện ra.
- Quả địa cầu màu nước xanh dương và xanh lá: điểm nhấn duy nhất, mang ý nghĩa "toàn cầu".
- Chuyển cảnh kiểu lật trang sách.
- Toàn bộ chữ dùng **Anaktoria**.

| Vai trò | Mã | Nguồn |
|---|---|---|
| Giấy | `#FAF8F2` | Lấy mẫu từ logo |
| Sọc giấy | `#F1EADD` | Poster |
| Mảng be (latte) | `#E2D6C3` | Mảng sau tách cà phê |
| Mực vẽ | `#2F2B2A` | Nét vẽ trong logo |
| Cà phê / crema / espresso | `#6B4A33` / `#C58B4A` / `#3A2414` | Tông cà phê |
| Xanh Trái Đất | `#2F7DC4` | Địa cầu trong logo; dùng cho chữ đang đọc và điểm nhấn |
| Xanh lục địa | `#5BA544` | Địa cầu trong logo |

**Font:** Anaktoria thiếu glyph dựng sẵn cho các chữ có dấu nặng hoặc dấu hỏi (ạ, ả, ặ, ồ, ợ, ỷ…).
- Chromium tự ghép các chữ đó từ dấu rời có trong font. Đã kiểm tra trên khung hình: "ngoại", "đậm", "kỷ lục" hiển thị đúng.
- Nếu dùng font này ở công cụ khác (Canva, CapCut), cần kiểm tra lại các chữ có dấu nặng.

## Kịch bản v2: cho người đã rành cà phê

Mạch kể: lịch sử (Gaggia) → bản chất crema → Robusta → điểm nối với Việt Nam → mẹo của barista.

1. Lớp crema dày mà người Naples tự hào… có dính dáng tới hạt Robusta. Đúng loại hạt Việt Nam trồng nhiều nhất thế giới.
2. Lùi về năm 1938: máy espresso còn chạy bằng hơi nước, áp lực thấp, mặt ly gần như trơn.
3. Achille Gaggia ở Milan đăng ký sáng chế một hệ thống bỏ hẳn hơi nước. Năm 1948, máy cần gạt piston của ông ép nước mạnh hơn hẳn, và mặt ly nổi lên một lớp bọt vàng nâu.
4. Theo lời kể, khách ngờ đó là váng. Gaggia treo biển, gọi nó là kem cà phê tự nhiên. Từ váng thành kem, chỉ bằng một cái tên.
5. Về bản chất, crema là khí CO2 sinh ra lúc rang, bị ép tan vào nước, rồi bung thành bọt khi tụt áp. Dầu và melanoidin giữ bọt đứng lại.
6. Robusta thường cho lớp bọt ấy dày hơn Arabica. Thế nên blend kiểu Naples hay pha từ hai đến bốn phần Robusta.
7. Và năm 2025, Ý là một trong ba nước mua cà phê Việt nhiều nhất.
8. Nhưng crema dày chỉ nói hạt còn tươi, áp lực đủ, chứ không nói hộ vị. Thử nếm riêng một thìa crema, rồi khuấy đều và nếm lại.
9. Bạn có khuấy crema không? Comment có hoặc không.

### So với bản 1

| Tiêu chí | Bản 1 | Bản 2 |
|---|---|---|
| Hook | "Crema từng cần một tấm biển": chuyện vui, kiến thức nông | Nối crema Naples với Robusta Việt Nam: tạo khoảng trống tò mò cho người rành cà phê |
| Độ sâu | Chỉ có lịch sử | Thêm cơ chế CO2 → tụt áp → bọt, vai trò của dầu và melanoidin, tỉ lệ Robusta trong blend Naples |
| Mạch kể | Các ý rời nhau | Mỗi đoạn mở bằng một từ nối ("Lùi về", "Về bản chất", "Thế nên", "Và", "Nhưng") |
| Góc nhìn barista | Một câu nhận xét | Một bài thử 3 bước làm được ngay tại quầy |
| Vòng lặp | "Váng hay kem?" | Khung kết là logo kênh (tách cà phê + địa cầu): củng cố nhận diện |

## Dữ kiện mới và nguồn

- **Cơ chế crema** (CO2 từ lúc rang, bung khi tụt áp, được dầu và melanoidin giữ lại): [Coffee Chronicler](https://coffeechronicler.com/crema-explained/), [CoffeeGeek](https://coffeegeek.com/opinions/professionally-speaking/crema/).
  - Đã bỏ ý "Robusta nhiều hay ít dầu hơn" vì các nguồn mâu thuẫn nhau.
- **Robusta thường cho crema dày hơn; blend Naples khoảng 20–40% Robusta:** đây là thông tin từ nhà bán lẻ và diễn đàn ([Home-Barista](https://www.home-barista.com/coffees/espresso-napoletano-and-thoughts-t56243.html)), chỉ mang tính tham khảo. Video nói "hay pha từ hai đến bốn phần".
- **Ý nằm trong top 3 thị trường mua cà phê Việt năm 2025** (sau Đức, khoảng 7,8–7,9%): [Vietnam News](https://vietnamnews.vn/economy/1721184/2025-coffee-exports-hit-target-set-for-record-7-5-billion.html), [VietNamNet](https://vietnamnet.vn/en/vietnam-sets-new-coffee-export-record-with-5-45-billion-in-first-half-of-2025-2421779.html).
  - Video **không** nói Robusta trong blend Naples đến từ Việt Nam, vì chưa có nguồn xác nhận điều đó.
- **Gaggia 1938 và 1948, tấm biển "caffè crema":** xem nguồn ở `../README.md`.

## Gói đăng

- **Caption:** Crema kiểu Naples và hạt Robusta Việt Nam có liên quan gì? ☕🌍 Bạn có khuấy crema không?
- **Hashtag:** #crema #espresso #robusta #caphevietnam #baristasinhngoai #LearnOnTikTok
