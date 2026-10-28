# Bài 8 – Hệ thống gợi ý: bản chỉnh sửa

- `AA6060_Bai08_Slides.pptx`: bản giảng viên (42 slide, có ghi chú và slide đáp án)
- `AA6060_Bai08_Slides_SinhVien.pptx`: bản sinh viên (41 slide, không có ghi chú và đáp án)
- `build.py`: script dựng lại cả hai bản. Chạy với thư mục `ppt/media` của bộ slide gốc:
  `python3 build.py <ppt/media gốc> <thư mục output>`

## Đã đổi những gì

**Mạch bài.** Bản cũ đi theo "6 phần của case Netflix". Bản mới đi theo 6 câu hỏi về hệ gợi ý
(bài toán, dữ liệu, phương pháp, đánh giá, khởi động lạnh, giá trị kinh doanh).
Netflix và MovieLens chỉ còn là ví dụ trả lời từng câu, ghi ở chú thích chân slide.
Ở những chỗ hợp lý có thêm ví dụ ngoài Netflix (sàn TMĐT).

**Tiêu đề.** Tiêu đề là câu kết luận ("Ma trận người dùng × sản phẩm gần như trống"),
không còn là nhãn chủ đề viết hoa ("MA TRẬN NGƯỜI DÙNG × PHIM").

**Bỏ các dấu hiệu AI slop** (theo anthropics/skills `frontend-design` và pbakaus/impeccable `craft-floor`, `distill`):
- bỏ nhãn "CASE NETFLIX" / "BÀI HỌC RÚT RA" trên mọi slide (eyebrow label)
- bỏ dải màu vàng ở cạnh trái các hộp câu hỏi
- bỏ bóng đổ mặc định trên khung
- slide "4 con số" (vòng tròn, biểu tượng $, mũi tên) thay bằng bảng có cột "Ý nghĩa"
- biểu tượng emoji (⏱ 🔍) và ký tự "▸" thay bằng gạch đầu dòng thường
- bớt chuỗi "A → B → C" và dấu "·" trong câu
- dòng "Đọc case → phân tích → rút ra khái niệm" lặp ở mọi slide chuyển phần được thay bằng một câu nói riêng nội dung của phần đó

**Vẽ lại dạng native (sửa được trong PowerPoint):** lộ trình, so sánh Hill 1995, hai loại phản hồi,
bốn loại dữ liệu, hai cách hiểu "giống", tách dữ liệu để đánh giá, sản phẩm mới, khởi động lạnh, giá trị kinh doanh, tổng kết.
Các hình có dữ liệu thật (ma trận, đường cong đuôi dài, biểu đồ MovieLens, bản đồ phân rã ma trận…) giữ nguyên.

**Giữ nguyên:** nền và nhận diện HaUI, màu navy/vàng, số liệu và trích dẫn, ghi chú giảng viên (cập nhật theo mạch mới).
