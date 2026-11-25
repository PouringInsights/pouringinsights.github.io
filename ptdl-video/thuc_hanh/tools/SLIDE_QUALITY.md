# Bổ sung bắt buộc: chất lượng slide và ngôn ngữ (ppt-master / impeccable / taste / unslop)

## Quy trình (ppt-master)
1. Viết dàn ý luận điểm trước: mỗi slide một "việc" (page job) ghi 1 câu. Duyệt dàn ý rồi mới dựng.
2. Khoá "neo" toàn deck: chỉ dùng màu, cỡ chữ, khoảng cách của khuôn HaUI (kits.py). Không tự thêm màu, font, hiệu ứng.
3. Đối tượng gốc, sửa được: chữ là text box, bảng là bảng PowerPoint. Không dán ảnh chụp chữ/bảng.
4. Sau khi dựng: render toàn bộ slide thành ảnh, xem từng slide, sửa một vòng "polish" (bản đầu chưa phải bản cuối).

## Bố cục, mật độ (impeccable / taste)
- Một ý chính mỗi slide. Tối đa ~60–80 từ/slide (không kể bảng). ≤ 6 gạch đầu dòng, mỗi dòng ≤ 2 dòng hiển thị.
- Tiêu đề slide là câu nói rõ điều cần nhớ hoặc gọi đúng tên nội dung ("Chọn K bằng Elbow và Silhouette"), không chung chung ("Nội dung", "Phần 2").
- Bảng ≤ 6 cột × 8 hàng; chữ trong bảng không nhỏ hơn cỡ mặc định của khuôn; số căn phải, có đơn vị.
- Không slide trống, không khung rỗng, không chữ tràn khỏi khung, lề trái/phải đều. Kiểm bằng ảnh render.
- Không thêm hiệu ứng chuyển cảnh/animation, không gradient, không icon trang trí, không khung lồng khung.
- Không bịa số liệu, trích dẫn, tên doanh nghiệp thật. Số minh hoạ ghi rõ "ví dụ minh hoạ".

## Ngôn ngữ (unslop)
- Câu ngắn, một ý, chủ động, có chủ ngữ. Dùng số cụ thể thay trạng từ ("giảm 18%" thay "giảm đáng kể").
- Cấm: "vô cùng quan trọng", "then chốt", "toàn diện", "đóng vai trò", "không chỉ… mà còn…", "trong bối cảnh", "có thể nói", "hãy cùng khám phá", "hành trình", "bức tranh toàn cảnh", bộ ba tính từ ép vần, câu kết chung chung.
- Không gạch ngang dài (—, –) thay dấu phẩy; không ngoặc đơn thay dấu phẩy; dấu hai chấm chỉ trước danh sách hoặc ví dụ.
- Không in đậm tràn lan; chỉ in đậm thuật ngữ khi định nghĩa lần đầu.
- Thuật ngữ tiếng Anh giữ nguyên khi phổ biến, giải thích tiếng Việt lần đầu.
Áp dụng cho cả ĐCBG (docx) và slide. Trước khi xong, chạy một script grep các từ cấm và ký tự "—" trên toàn bộ văn bản và sửa hết.
